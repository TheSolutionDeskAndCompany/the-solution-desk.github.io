import { render, screen, fireEvent, waitFor } from "@testing-library/react";
import IdeaForm from "../IdeaForm";
import { ToastContainer } from "react-toastify";
import { act } from "react-dom/test-utils";

// Mock axios for the API calls
jest.mock("axios", () => ({
  post: jest.fn(() => Promise.resolve({ data: { success: true } })),
}));

// Mock the environment variables
beforeEach(() => {
  process.env = {
    ...process.env,
    REACT_APP_API_URL: "http://test-api.example.com",
  };
});

test("renders IdeaForm and submits successfully", async () => {
  render(
    <div>
      <IdeaForm />
      <ToastContainer />
    </div>,
  );

  // Check if form fields are present
  expect(screen.getByPlaceholderText("Idea title")).toBeInTheDocument();
  expect(screen.getByPlaceholderText("Describe your idea")).toBeInTheDocument();

  // Simulate user input and submit
  fireEvent.change(screen.getByPlaceholderText("Idea title"), {
    target: { value: "Test Idea" },
  });
  fireEvent.change(screen.getByPlaceholderText("Describe your idea"), {
    target: { value: "This is a description of the test idea." },
  });

  fireEvent.click(screen.getByText("Submit"));

  // Wait for the success toast (replace with real success after API is connected)
  await waitFor(() => screen.getByText("Idea submitted successfully!"));
});

test("shows error message for invalid form submission", async () => {
  render(
    <div>
      <IdeaForm />
      <ToastContainer />
    </div>,
  );

  fireEvent.click(screen.getByText("Submit"));

  // Check for validation errors (using getAllByText since there are multiple fields with 'Required')
  await waitFor(() => {
    const errorMessages = screen.getAllByText("Required");
    expect(errorMessages.length).toBeGreaterThanOrEqual(1);
  });
});
