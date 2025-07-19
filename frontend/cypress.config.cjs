const { defineConfig } = require('cypress');

module.exports = defineConfig({
  e2e: {
    baseUrl: process.env.CYPRESS_BASE_URL || 'http://localhost:3000',
    specPattern: 'cypress/integration/**/*.spec.js',
    supportFile: 'cypress/support/commands.js',
    viewportWidth: 1280,
    viewportHeight: 800,
    video: true,
    videoUploadOnPasses: false,
    retries: {
      runMode: 2,
      openMode: 0
    },
    setupNodeEvents(on, config) {
      // implement node event listeners here if needed
      return config;
    },
  },
  env: {
    // Environment variables for testing
    CI: process.env.CI === 'true',
    apiUrl: process.env.CYPRESS_API_URL || process.env.REACT_APP_API_URL || 'http://localhost:5000',
    // Staging URLs (can be overridden via environment variables)
    stagingFrontendUrl: process.env.CYPRESS_STAGING_FRONTEND_URL || 'https://your-netlify-domain.netlify.app',
    stagingBackendUrl: process.env.CYPRESS_STAGING_BACKEND_URL || 'https://ow-backend.onrender.com',
  },
});
