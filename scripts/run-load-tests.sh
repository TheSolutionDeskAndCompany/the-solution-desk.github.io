#!/bin/bash

# k6 Load Testing Runner Script
# Usage: ./scripts/run-load-tests.sh [scenario] [environment]
# Example: ./scripts/run-load-tests.sh ci staging

set -e

# Default values
SCENARIO=${1:-ci}
ENVIRONMENT=${2:-local}
OUTPUT_DIR="test-results/load"

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
    export API_URL="http://localhost:5000"
    export FRONTEND_URL="http://localhost:3000"
    ;;
  "staging")
    export API_URL="${STAGING_BACKEND_URL:-https://ow-backend.onrender.com}"
    export FRONTEND_URL="${STAGING_FRONTEND_URL:-https://your-netlify-domain.netlify.app}"
    ;;
  "production")
    export API_URL="${PRODUCTION_BACKEND_URL:-https://api.thesolutiondesk.ca}"
    export FRONTEND_URL="${PRODUCTION_FRONTEND_URL:-https://thesolutiondesk.ca}"
    ;;
  *)
    echo -e "${RED}❌ Unknown environment: $ENVIRONMENT${NC}"
    echo "Valid environments: local, staging, production"
    exit 1
    ;;
esac

echo -e "${YELLOW}API URL: $API_URL${NC}"
echo -e "${YELLOW}Frontend URL: $FRONTEND_URL${NC}"

# Check if k6 is installed
if ! command -v k6 &> /dev/null; then
    echo -e "${RED}❌ k6 is not installed${NC}"
    echo "Install k6 from: https://k6.io/docs/getting-started/installation/"
    exit 1
fi

# Health check
echo -e "${BLUE}🔍 Performing health check...${NC}"
if ! curl -f -s "$API_URL/health" > /dev/null; then
    echo -e "${RED}❌ Backend health check failed at $API_URL/health${NC}"
    exit 1
fi
echo -e "${GREEN}✅ Backend is healthy${NC}"

# Run authentication performance test
echo -e "${BLUE}🔐 Running authentication performance test...${NC}"
TIMESTAMP=$(date +%Y%m%d_%H%M%S)
AUTH_RESULTS="$OUTPUT_DIR/auth-performance_${SCENARIO}_${ENVIRONMENT}_${TIMESTAMP}.json"

k6 run \
  --env SCENARIO="$SCENARIO" \
  --env API_URL="$API_URL" \
  --env FRONTEND_URL="$FRONTEND_URL" \
  --out json="$AUTH_RESULTS" \
  tests/load/auth-performance.js

AUTH_EXIT_CODE=$?

# Run API performance test
echo -e "${BLUE}🔧 Running API performance test...${NC}"
API_RESULTS="$OUTPUT_DIR/api-performance_${SCENARIO}_${ENVIRONMENT}_${TIMESTAMP}.json"

k6 run \
  --env SCENARIO="$SCENARIO" \
  --env API_URL="$API_URL" \
  --env FRONTEND_URL="$FRONTEND_URL" \
  --out json="$API_RESULTS" \
  tests/load/api-performance.js

API_EXIT_CODE=$?

# Generate summary report
echo -e "${BLUE}📊 Generating test report...${NC}"
REPORT_FILE="$OUTPUT_DIR/load-test-report_${SCENARIO}_${ENVIRONMENT}_${TIMESTAMP}.md"

cat > "$REPORT_FILE" << EOF
# Load Test Report

**Date:** $(date)
**Scenario:** $SCENARIO
**Environment:** $ENVIRONMENT
**API URL:** $API_URL
**Frontend URL:** $FRONTEND_URL

## Test Results

### Authentication Performance Test
- **Exit Code:** $AUTH_EXIT_CODE
- **Results File:** $AUTH_RESULTS
- **Status:** $([ $AUTH_EXIT_CODE -eq 0 ] && echo "✅ PASSED" || echo "❌ FAILED")

### API Performance Test
- **Exit Code:** $API_EXIT_CODE
- **Results File:** $API_RESULTS
- **Status:** $([ $API_EXIT_CODE -eq 0 ] && echo "✅ PASSED" || echo "❌ FAILED")

## Overall Status
$([ $AUTH_EXIT_CODE -eq 0 ] && [ $API_EXIT_CODE -eq 0 ] && echo "✅ ALL TESTS PASSED" || echo "❌ SOME TESTS FAILED")

## Files Generated
- Auth Results: \`$AUTH_RESULTS\`
- API Results: \`$API_RESULTS\`
- This Report: \`$REPORT_FILE\`

## Next Steps
$([ $AUTH_EXIT_CODE -eq 0 ] && [ $API_EXIT_CODE -eq 0 ] && echo "- Performance is within acceptable thresholds
- Consider running stress tests if needed
- Monitor these metrics in production" || echo "- Review failed test thresholds
- Investigate performance bottlenecks
- Optimize slow endpoints before deployment")
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
