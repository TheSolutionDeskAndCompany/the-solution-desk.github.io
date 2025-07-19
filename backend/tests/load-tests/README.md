# Performance and Load Testing

This directory contains performance and load tests for the backend API using [k6](https://k6.io/).

## Test Scripts

- `auth-performance.js`: Tests authentication flows (registration, login, protected endpoints)
- `api-performance.js`: Tests general API endpoints and performance
- `k6-config.js`: Configuration for different test scenarios (smoke, load, stress)

## Running Tests Locally

### Prerequisites

1. Install k6:

   ```bash
   # macOS
   brew install k6
   
   # Linux
   sudo apt-get update && sudo apt-get install k6
   
   # Windows (using Chocolatey)
   choco install k6
   ```

2. (Optional) Install jq for better test reporting:

   ```bash
   # macOS
   brew install jq
   
   # Linux
   sudo apt-get install jq
   ```

### Running Tests

Use the provided script to run tests:

```bash
# Navigate to project root
cd /path/to/the-solution-desk

# Run a quick smoke test (1 virtual user, 30 seconds)
./scripts/run-load-tests.sh smoke local

# Run a standard load test
./scripts/run-load-tests.sh load local

# Run a stress test
./scripts/run-load-tests.sh stress local
```

### Test Scenarios

- **smoke**: Quick verification with minimal load (1 VU, 30s)
- **ci**: Used in CI/CD pipeline (5 VUs, 1 minute)
- **load**: Standard load test (10-25 VUs, 5 minutes)
- **stress**: High load test (20-100 VUs, 10 minutes)

## Test Results

Test results are saved in the `test-results/load/` directory with timestamps. Each test run generates:

- JSON results file with detailed metrics
- Summary file with aggregated metrics
- HTML report with visualizations

## CI/CD Integration

Performance tests are automatically run in the GitHub Actions CI/CD pipeline on every push to `main` or `backend-main` branches, and on pull requests.

### Automated Bug Capture

When performance tests fail in CI:

1. **For Pull Requests**:
   - A detailed comment is added to the PR with test results
   - No GitHub issues are created to keep the main repository clean

2. **For Direct Pushes to Main/Backend-Main**:
   - A GitHub issue is automatically created with the failure details
   - The issue is labeled with `performance` and `automated`
   - The backend team is automatically assigned
   - If an open issue already exists for the same branch, a comment is added instead

3. **When Tests Pass**:
   - Any open performance issues for the branch are automatically closed
   - A resolution comment is added to the issue

### Performance Thresholds

Tests will fail if any of these thresholds are not met:

- 95% of requests must complete within 500ms
- Less than 5% of requests can fail
- Error rate must be below 5%

## Customizing Tests

### Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `K6_PUBLIC_API_URL` | Base URL of the API | `http://localhost:5000` |
| `K6_ENV` | Test environment/scenario | `load` |
| `K6_DURATION` | Test duration | Varies by scenario |
| `K6_VUS` | Number of virtual users | Varies by scenario |

### Adding New Tests

1. Create a new `.js` file in this directory
2. Import the `k6` library and any required modules
3. Define test logic in the `default` function
4. Add thresholds and options as needed
5. Update the `run-load-tests.sh` script if necessary

## Troubleshooting

### Tests are failing

1. Check the API is running and accessible
2. Verify environment variables are set correctly
3. Check for rate limiting or authentication issues
4. Review the generated report for specific error messages

### Performance Issues

1. Check server resource usage during tests
2. Review database query performance
3. Look for slow endpoints in the test results
4. Consider increasing server resources if consistently hitting limits

## License

This project is licensed under the MIT License - see the [LICENSE](../LICENSE) file for details.
