// Mock axios module for Jest tests
const mockData = {
  health: { status: 'ok' }
};

const axiosMock = {
  get: jest.fn((url) => {
    // Return a resolved promise with data based on the URL
    if (url.includes('/health')) {
      return Promise.resolve({ data: mockData.health });
    }
    return Promise.resolve({ data: {} });
  }),
  post: jest.fn(() => Promise.resolve({ data: {} })),
  put: jest.fn(() => Promise.resolve({ data: {} })),
  delete: jest.fn(() => Promise.resolve({ data: {} })),
  create: jest.fn(function() { return this; }),
  defaults: { headers: { common: {} } }
};

module.exports = axiosMock;
