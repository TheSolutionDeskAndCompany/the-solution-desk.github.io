module.exports = {
  testEnvironment: 'jsdom',
  transform: {
    '^.+\\.[jt]sx?$': ['babel-jest', { configFile: './babel.config.js' }],
  },
  moduleFileExtensions: ['js', 'jsx', 'json'],
  extensionsToTreatAsEsm: ['.js', '.jsx'],
  transformIgnorePatterns: [
    // Transform axios to CommonJS
    '/node_modules/(?!axios).+\\.js$'
  ],
  // Setup a test environment that has React
  setupFilesAfterEnv: ['<rootDir>/src/setupTests.js']
};
