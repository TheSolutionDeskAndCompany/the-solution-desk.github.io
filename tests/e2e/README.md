# End-to-End Testing with Playwright

This directory contains the end-to-end (E2E) tests for The Solution Desk application.

## Setup

### Prerequisites

- Node.js (v14 or higher)
- npm or yarn

### Installation

```bash
# Install Playwright and dependencies
npm init -y
npm install @playwright/test
npx playwright install
```

## Test Structure

Tests should be organized by feature/flow and named with the `.spec.js` extension:

- `auth.spec.js` - Authentication flows
- `ideas.spec.js` - Idea creation, editing, and management
- `projects.spec.js` - Project management flows
- `kpis.spec.js` - KPI dashboard interactions

## Running Tests

```bash
# Run all tests
npx playwright test

# Run specific test file
npx playwright test tests/e2e/auth.spec.js

# Run tests in headed mode (visible browser)
npx playwright test --headed

# Run tests with specific browser
npx playwright test --project=chromium
```

## Configuration

The Playwright configuration is in `playwright.config.js` in the project root.

## Writing Tests

### Example Test Structure

```javascript
import { test, expect } from '@playwright/test';

test.describe('Authentication Flow', () => {
  test('should allow a user to log in', async ({ page }) => {
    // Navigate to the login page
    await page.goto('/auth/login');
    
    // Fill the login form
    await page.fill('#email', 'admin@example.com');
    await page.fill('#password', 'password123');
    
    // Submit the form
    await page.click('button[type="submit"]');
    
    // Assert that we are redirected to the dashboard
    await expect(page).toHaveURL(/dashboard/);
    
    // Assert that the user info is visible
    await expect(page.locator('.user-info')).toContainText('admin');
  });
});
```

## CI Integration

E2E tests can be integrated with GitLab CI as follows:

```yaml
e2e_tests:
  stage: test
  image: mcr.microsoft.com/playwright:v1.39.0-jammy
  script:
    - cd /path/to/e2e/tests
    - npm ci
    - npx playwright test
  artifacts:
    when: always
    paths:
      - playwright-report/
    expire_in: 1 week
```

## Best Practices

1. **Test isolation**: Each test should be independent and not rely on the state from previous tests
2. **Realistic user flows**: Tests should simulate real user interactions
3. **Meaningful assertions**: Assert on visible content, not implementation details
4. **Stable selectors**: Use data-testid attributes instead of classes or other styling attributes
5. **Parallel execution**: Design tests to run in parallel to speed up the test suite
6. **Screenshots and videos**: Configure Playwright to capture screenshots and videos on failure
7. **Retry failed tests**: Configure automatic retries for flaky tests
8. **Performance monitoring**: Track test execution time to identify bottlenecks
