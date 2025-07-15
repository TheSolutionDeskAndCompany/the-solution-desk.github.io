#!/bin/bash
# Security testing script for The Solution Desk
# This script runs security checks using Bandit for code security and Safety for dependency vulnerability scanning

set -e  # Exit immediately if a command exits with a non-zero status

# Text formatting
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

echo -e "${YELLOW}Starting security tests for The Solution Desk...${NC}"

# Create directory for reports if it doesn't exist
mkdir -p reports

# Run Bandit for security scanning
echo -e "\n${YELLOW}Running Bandit security scanner...${NC}"
bandit -r . -f json -o reports/bandit-report.json || {
    echo -e "${RED}Bandit found security issues! Check reports/bandit-report.json for details.${NC}"
    bandit -r . -f txt -o reports/bandit-report.txt
    cat reports/bandit-report.txt
    exit_code=1
}

if [ $? -eq 0 ]; then
    echo -e "${GREEN}Bandit security scan passed!${NC}"
fi

# Run Safety to check for vulnerable dependencies
echo -e "\n${YELLOW}Checking dependencies for security vulnerabilities...${NC}"
safety check -r requirements.txt --output json --save-json reports/safety-report.json || {
    echo -e "${RED}Safety found vulnerable dependencies! Check reports/safety-report.json for details.${NC}"
    safety check -r requirements.txt --output text
    exit_code=1
}

if [ $? -eq 0 ]; then
    echo -e "${GREEN}Safety dependency check passed!${NC}"
fi

# Run additional validation checks for API
echo -e "\n${YELLOW}Validating API endpoints and responses...${NC}"
python -m pytest tests/test_api_validation.py -v || {
    echo -e "${RED}API validation tests failed!${NC}"
    exit_code=1
}

# Output summary
if [ -z "$exit_code" ]; then
    echo -e "\n${GREEN}All security tests passed!${NC}"
    exit 0
else
    echo -e "\n${RED}Some security tests failed. Please review the reports.${NC}"
    exit 1
fi
