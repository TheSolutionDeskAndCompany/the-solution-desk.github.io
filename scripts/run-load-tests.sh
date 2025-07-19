#!/bin/bash

# k6 Load Testing Runner Script
# Usage: ./scripts/run-load-tests.sh [scenario] [environment]
# Example: ./scripts/run-load-tests.sh ci staging

set -e

# Default values
SCENARIO=${1:-ci}
ENVIRONMENT=${2:-local}
OUTPUT_DIR="test-results/load"
SCRIPT_DIR=$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)
ROOT_DIR="$SCRIPT_DIR/.."

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

echo -e "${BLUE}🚀 Starting k6 Load Tests${NC}"
echo -e "${BLUE}Scenario: ${SCENARIO}${NC}"
echo -e "${BLUE}Environment: ${ENVIRONMENT}${NC}"

# Create output directory
mkdir -p "$OUTPUT_DIR"

# Set environment variables based on environment
case $ENVIRONMENT in
  "local")
    export K6_PUBLIC_API_URL="http://localhost:5000"
    export K6_FRONTEND_URL="http://localhost:3000"
    ;;
  "staging")
    export K6_PUBLIC_API_URL="${STAGING_BACKEND_URL:-https://ow-backend.onrender.com}"
    export K6_FRONTEND_URL="${STAGING_FRONTEND_URL:-https://your-netlify-domain.netlify.app}"
    ;;
  "production")
    export K6_PUBLIC_API_URL="${PRODUCTION_BACKEND_URL:-https://api.thesolutiondesk.ca}"
    export K6_FRONTEND_URL="${PRODUCTION_FRONTEND_URL:-https://thesolutiondesk.ca}"
    ;;
  *)
    echo -e "${RED}❌ Unknown environment: $ENVIRONMENT${NC}"
    echo "Valid environments: local, staging, production"
    exit 1
    ;;
esac

echo -e "${YELLOW}API URL: $K6_PUBLIC_API_URL${NC}"
echo -e "${YELLOW}Frontend URL: $K6_FRONTEND_URL${NC}"

# Check if k6 is installed
if ! command -v k6 &> /dev/null; then
    echo -e "${RED}❌ k6 is not installed${NC}"
    echo "Install k6 from: https://k6.io/docs/getting-started/installation/"
    exit 1
fi

# Check if jq is installed (for JSON processing)
if ! command -v jq &> /dev/null; then
    echo -e "${YELLOW}⚠️ jq is not installed. Some features may be limited.${NC}"
    echo "Install jq with: brew install jq (macOS) or apt-get install jq (Linux)"
fi

# Health check
echo -e "${BLUE}🔍 Performing health check...${NC}"
if ! curl -f -s "$K6_PUBLIC_API_URL/health" > /dev/null; then
    echo -e "${RED}❌ Backend health check failed at $K6_PUBLIC_API_URL/health${NC}"
    echo -e "${YELLOW}⚠️  Attempting to continue anyway...${NC}"
else
    echo -e "${GREEN}✅ Backend is healthy${NC}"
fi

# Set k6 environment variables
export K6_ENV="$SCENARIO"

# Run authentication performance test
echo -e "${BLUE}🔐 Running authentication performance test...${NC}"
TIMESTAMP=$(date +%Y%m%d_%H%M%S)
AUTH_JSON_RESULTS="$OUTPUT_DIR/auth-performance_${SCENARIO}_${ENVIRONMENT}_${TIMESTAMP}.json"
AUTH_SUMMARY="$OUTPUT_DIR/auth-summary_${SCENARIO}_${ENVIRONMENT}_${TIMESTAMP}.json"

echo -e "${YELLOW}Running auth performance test with $SCENARIO scenario...${NC}"
k6 run \
  --env K6_ENV="$SCENARIO" \
  --env K6_PUBLIC_API_URL="$K6_PUBLIC_API_URL" \
  --out json="$AUTH_JSON_RESULTS" \
  --summary-export="$AUTH_SUMMARY" \
  --tag scenario="$SCENARIO" \
  --tag environment="$ENVIRONMENT" \
  --tag test_type="auth" \
  "$ROOT_DIR/backend/tests/load-tests/auth-performance.js"

AUTH_EXIT_CODE=$?

# Run API performance test
echo -e "${BLUE}🔧 Running API performance test...${NC}"
API_JSON_RESULTS="$OUTPUT_DIR/api-performance_${SCENARIO}_${ENVIRONMENT}_${TIMESTAMP}.json"
API_SUMMARY="$OUTPUT_DIR/api-summary_${SCENARIO}_${ENVIRONMENT}_${TIMESTAMP}.json"

echo -e "${YELLOW}Running API performance test with $SCENARIO scenario...${NC}"
k6 run \
  --env K6_ENV="$SCENARIO" \
  --env K6_PUBLIC_API_URL="$K6_PUBLIC_API_URL" \
  --out json="$API_JSON_RESULTS" \
  --summary-export="$API_SUMMARY" \
  --tag scenario="$SCENARIO" \
  --tag environment="$ENVIRONMENT" \
  --tag test_type="api" \
  "$ROOT_DIR/backend/tests/load-tests/api-performance.js"

API_EXIT_CODE=$?

# Generate summary report
echo -e "${BLUE}📊 Generating test report...${NC}"
REPORT_FILE="$OUTPUT_DIR/load-test-report_${SCENARIO}_${ENVIRONMENT}_${TIMESTAMP}.md"

# Function to format metrics for the report
format_metrics() {
    local summary_file="$1"
    local prefix="$2"
    
    if [ ! -f "$summary_file" ]; then
        echo "  - No metrics available"
        return
    fi
    
    if command -v jq &> /dev/null; then
        jq -r '.metrics | to_entries[] | "  - \(.key): \(.value.values.rate | round(2)) reqs/s (p95: \(.value.values["p(95)"] | round(2))ms, failures: \(.value.values["http_req_failed"] * 100 | round(2))%)"' "$summary_file"
    else
        echo "  - Install jq for detailed metrics"
    fi
}

# Create the report
cat > "$REPORT_FILE" << EOF
# Load Test Report

**Date:** $(date)
**Scenario:** $SCENARIO
**Environment:** $ENVIRONMENT
**API URL:** $K6_PUBLIC_API_URL
**Frontend URL:** $K6_FRONTEND_URL

## Test Results

### Authentication Performance Test
- **Status:** $([ $AUTH_EXIT_CODE -eq 0 ] && echo "✅ PASSED" || echo "❌ FAILED")
- **Exit Code:** $AUTH_EXIT_CODE
- **Results File:** $AUTH_JSON_RESULTS
- **Summary File:** $AUTH_SUMMARY

**Metrics:**
$(format_metrics "$AUTH_SUMMARY")

### API Performance Test
- **Status:** $([ $API_EXIT_CODE -eq 0 ] && echo "✅ PASSED" || echo "❌ FAILED")
- **Exit Code:** $API_EXIT_CODE
- **Results File:** $API_JSON_RESULTS
- **Summary File:** $API_SUMMARY

**Metrics:**
$(format_metrics "$API_SUMMARY")

## Overall Status
$([ $AUTH_EXIT_CODE -eq 0 ] && [ $API_EXIT_CODE -eq 0 ] && echo "✅ ALL TESTS PASSED" || echo "❌ SOME TESTS FAILED")

## Files Generated
- **Auth Test Results:** \`$AUTH_JSON_RESULTS\`
- **Auth Test Summary:** \`$AUTH_SUMMARY\`
- **API Test Results:** \`$API_JSON_RESULTS\`
- **API Test Summary:** \`$API_SUMMARY\`
- **This Report:** \`$REPORT_FILE\`

## Next Steps
$([ $AUTH_EXIT_CODE -eq 0 ] && [ $API_EXIT_CODE -eq 0 ] && echo "- ✅ Performance is within acceptable thresholds
- 🔍 Consider running stress tests if needed
- 📈 Monitor these metrics in production" || echo "- 🔍 Review failed test thresholds
- ⚡ Investigate performance bottlenecks
- 🛠️  Optimize slow endpoints before deployment")

## How to Run Tests Locally

1. Start your backend server:
   \`\`\`bash
   cd $ROOT_DIR/backend
   python app.py
   \`\`\`

2. In a new terminal, run the tests:
   \`\`\`bash
   # Quick smoke test
   ./scripts/run-load-tests.sh smoke local
   
   # Full load test
   ./scripts/run-load-tests.sh load local
   
   # Stress test
   ./scripts/run-load-tests.sh stress local
   \`\`\`

3. View the generated report in your browser:
   \`\`\`bash
   open "$REPORT_FILE"
   \`\`\`

EOF

echo -e "${GREEN}📋 Report generated: $REPORT_FILE${NC}"

# Final status
if [ $AUTH_EXIT_CODE -eq 0 ] && [ $API_EXIT_CODE -eq 0 ]; then
    echo -e "${GREEN}🎉 All load tests passed!${NC}"
    exit 0
else
    echo -e "${RED}❌ Some load tests failed${NC}"
    echo -e "${YELLOW}Check the detailed results in: $OUTPUT_DIR${NC}"
    exit 1
fi
