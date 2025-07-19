#!/usr/bin/env node
/**
 * Script to run Cypress E2E tests against staging environment
 */

const { execSync } = require('child_process');
const path = require('path');

// Configuration for staging environment
const STAGING_CONFIG = {
  frontendUrl: process.env.STAGING_FRONTEND_URL || 'https://your-netlify-domain.netlify.app',
  backendUrl: process.env.STAGING_BACKEND_URL || 'https://ow-backend.onrender.com',
};

console.log('🚀 Running E2E tests against staging environment...');
console.log(`Frontend URL: ${STAGING_CONFIG.frontendUrl}`);
console.log(`Backend URL: ${STAGING_CONFIG.backendUrl}`);

// Set environment variables for Cypress
const env = {
  ...process.env,
  CYPRESS_BASE_URL: STAGING_CONFIG.frontendUrl,
  CYPRESS_API_URL: STAGING_CONFIG.backendUrl,
  CYPRESS_STAGING_FRONTEND_URL: STAGING_CONFIG.frontendUrl,
  CYPRESS_STAGING_BACKEND_URL: STAGING_CONFIG.backendUrl,
};

try {
  // Run Cypress tests
  const cypressCommand = process.argv.includes('--headless') 
    ? 'npx cypress run --config-file cypress.config.cjs --spec "cypress/integration/auth-flow.spec.js"'
    : 'npx cypress open --config-file cypress.config.cjs';

  console.log(`\n📋 Running command: ${cypressCommand}\n`);
  
  execSync(cypressCommand, {
    stdio: 'inherit',
    cwd: path.resolve(__dirname, '..'),
    env: env,
  });

  console.log('\n✅ E2E tests completed successfully!');
} catch (error) {
  console.error('\n❌ E2E tests failed:', error.message);
  process.exit(1);
}
