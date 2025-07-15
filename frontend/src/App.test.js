import { render, screen } from "@testing-library/react";
import App from "./App";

// Mock axios before importing App
jest.mock('axios', () => ({
  get: jest.fn(() => Promise.resolve({ data: { status: 'ok' } })),
  post: jest.fn(() => Promise.resolve({ data: {} })),
  put: jest.fn(() => Promise.resolve({ data: {} })),
  delete: jest.fn(() => Promise.resolve({ data: {} })),
}));

// Mock Sentry
jest.mock('@sentry/react', () => ({
  init: jest.fn(),
  ErrorBoundary: ({ children }) => children,
}));

// Set NODE_ENV to 'test' to disable the error throw in App.js
process.env.NODE_ENV = 'test';

// Mock setTimeout to prevent test errors
jest.spyOn(global, 'setTimeout').mockImplementation(() => 123);

test("renders learn react link", () => {
  render(<App />);
  const linkElement = screen.getByText(/learn react/i);
  expect(linkElement).toBeInTheDocument();
});
