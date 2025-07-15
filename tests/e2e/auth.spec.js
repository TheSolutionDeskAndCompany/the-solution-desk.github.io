// @ts-check
const { test, expect } = require('@playwright/test');

test.describe('Authentication', () => {
  test('should allow a user to login', async ({ page }) => {
    // Navigate to login page
    await page.goto('/auth/login');
    
    // Fill login form
    await page.fill('input[name="email"]', 'admin@example.com');
    await page.fill('input[name="password"]', 'password123');
    
    // Submit the form
    await page.click('button[type="submit"]');
    
    // Assert we are redirected to dashboard or home page
    await expect(page).toHaveURL(/dashboard|home/);
    
    // Assert that we see user-specific content
    await expect(page.locator('nav')).toContainText(/admin|logout/i);
  });
  
  test('should show error with invalid credentials', async ({ page }) => {
    // Navigate to login page
    await page.goto('/auth/login');
    
    // Fill form with invalid credentials
    await page.fill('input[name="email"]', 'invalid@example.com');
    await page.fill('input[name="password"]', 'wrongpassword');
    
    // Submit the form
    await page.click('button[type="submit"]');
    
    // Assert we stay on login page
    await expect(page).toHaveURL(/login/);
    
    // Assert error message is shown
    await expect(page.locator('.error-message, .alert-danger')).toBeVisible();
    await expect(page.locator('.error-message, .alert-danger')).toContainText(/invalid|failed/i);
  });
});

test.describe('Registration', () => {
  test('should allow a user to register', async ({ page }) => {
    // Generate unique email to avoid conflicts
    const uniqueEmail = `test.user.${Date.now()}@example.com`;
    
    // Navigate to register page
    await page.goto('/auth/register');
    
    // Fill registration form
    await page.fill('input[name="email"]', uniqueEmail);
    await page.fill('input[name="password"]', 'Password123!');
    await page.fill('input[name="confirm_password"]', 'Password123!');
    
    // Submit the form
    await page.click('button[type="submit"]');
    
    // Assert we are redirected to login or dashboard
    await expect(page).toHaveURL(/login|dashboard|home/);
    
    // If redirected to login page, we should see a success message
    if (page.url().includes('login')) {
      await expect(page.locator('.success-message, .alert-success')).toBeVisible();
    }
  });
  
  test('should validate password requirements', async ({ page }) => {
    // Navigate to register page
    await page.goto('/auth/register');
    
    // Fill registration form with weak password
    await page.fill('input[name="email"]', 'test@example.com');
    await page.fill('input[name="password"]', '123');
    await page.fill('input[name="confirm_password"]', '123');
    
    // Submit the form
    await page.click('button[type="submit"]');
    
    // Assert we stay on register page
    await expect(page).toHaveURL(/register/);
    
    // Assert error message about password requirements
    await expect(page.locator('.error-message, .alert-danger, .invalid-feedback')).toBeVisible();
  });
});
