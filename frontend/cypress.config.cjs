const { defineConfig } = require('cypress');

module.exports = defineConfig({
  e2e: {
    baseUrl: 'http://localhost:3000',
    specPattern: 'cypress/integration/**/*.spec.js',
    supportFile: 'cypress/support/commands.js',
    viewportWidth: 1280,
    viewportHeight: 800,
    setupNodeEvents() {
      // implement node event listeners here if needed
      return null;
    },
  },
  env: {
    // Add any environment variables here
  },
});
