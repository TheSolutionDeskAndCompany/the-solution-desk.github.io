import React from "react";
import ReactDOM from "react-dom/client";
import "./styles/design-system.css";
import "./index.css";
import App from "./App.js";
import reportWebVitals from "./reportWebVitals.js";
import * as Sentry from "@sentry/react";
import { BrowserTracing } from "@sentry/tracing";
import { ToastContainer } from "react-toastify";
import "react-toastify/dist/ReactToastify.css";
import { AuthProvider } from "./context/AuthContext.jsx";

// Initialize Sentry
Sentry.init({
  dsn: process.env.REACT_APP_SENTRY_DSN,
  integrations: [new BrowserTracing()],
  // Adjust to your sampling needs
  tracesSampleRate: 1.0,
});

// Wrap your App in an Error Boundary
const container = document.getElementById("root");
const root = ReactDOM.createRoot(container);
root.render(
  <React.StrictMode>
    <Sentry.ErrorBoundary fallback={"An unexpected error occurred"}>
      <AuthProvider>
        <App />
        <ToastContainer
          position="top-right"
          autoClose={3000}
          hideProgressBar
          newestOnTop
          closeOnClick
          pauseOnFocusLoss
          draggable
        />
      </AuthProvider>
    </Sentry.ErrorBoundary>
  </React.StrictMode>,
);

// If you want to start measuring performance in your app, pass a function
// to log results (for example: reportWebVitals(console.log))
// or send to an analytics endpoint. Learn more: https://bit.ly/CRA-vitals
reportWebVitals();
