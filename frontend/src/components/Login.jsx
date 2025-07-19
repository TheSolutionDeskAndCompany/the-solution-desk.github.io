import React from "react";
import { Formik, Form, Field, ErrorMessage } from "formik";
import * as Yup from "yup";
import { useAuth } from "../context/AuthContext";
import { useNavigate, Link } from "react-router-dom";
import "./Auth.css";

export default function Login() {
  const { login, loading } = useAuth();
  const navigate = useNavigate();

  const schema = Yup.object({
    email: Yup.string()
      .email("Invalid email format")
      .required("Email is required"),
    password: Yup.string()
      .min(8, "Password must be at least 8 characters")
      .required("Password is required"),
  });

  return (
    <div className="auth-container">
      <div className="auth-card">
        <Formik
          initialValues={{ email: "", password: "" }}
          validationSchema={schema}
          onSubmit={async (values, { setSubmitting, setFieldError }) => {
            setSubmitting(true);
            const result = await login(values);

            if (result.success) {
              navigate("/dashboard");
            } else {
              // Handle specific field errors if needed
              if (result.error.includes("email")) {
                setFieldError("email", result.error);
              } else if (result.error.includes("password")) {
                setFieldError("password", result.error);
              }
            }
            setSubmitting(false);
          }}
        >
          {({ isSubmitting }) => (
            <Form className="auth-form">
              <h2 className="auth-title">Welcome Back</h2>
              <p className="auth-subtitle">Sign in to your account</p>

              <div className="form-group">
                <Field
                  name="email"
                  type="email"
                  placeholder="Email address"
                  className="form-input"
                  disabled={isSubmitting || loading}
                />
                <ErrorMessage
                  name="email"
                  component="div"
                  className="error-message"
                />
              </div>

              <div className="form-group">
                <Field
                  type="password"
                  name="password"
                  placeholder="Password"
                  className="form-input"
                  disabled={isSubmitting || loading}
                />
                <ErrorMessage
                  name="password"
                  component="div"
                  className="error-message"
                />
              </div>

              <button
                type="submit"
                disabled={isSubmitting || loading}
                className="auth-button"
              >
                {isSubmitting ? "Signing in..." : "Sign In"}
              </button>

              <div className="auth-links">
                <p>
                  Don't have an account?{" "}
                  <Link to="/register" className="auth-link">
                    Sign up
                  </Link>
                </p>
              </div>
            </Form>
          )}
        </Formik>
      </div>
    </div>
  );
}
