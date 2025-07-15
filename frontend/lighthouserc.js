module.exports = {
  ci: {
    collect: {
      url: ['http://localhost:3000'],
      startServerCommand: 'npm start',
      numberOfRuns: 3,
    },
    assert: {
      preset: 'lighthouse:recommended',
    },
    upload: {
      target: 'temporary-public-storage',
    },
  },
};
