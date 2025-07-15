const { defineConfig } = require('cypress');

module.exports = defineConfig({
  e2e: {
    baseUrl: 'http://localhost:3000', // adjust if you're using a different port
    specPattern: 'cypress/e2e/**/*.cy.{js,jsx}',
    supportFile: false,
  },
});
