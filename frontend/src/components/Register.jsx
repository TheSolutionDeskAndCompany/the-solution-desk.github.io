import React from "react";
import { Formik, Form, Field, ErrorMessage } from "formik";
import * as Yup from "yup";
import { useAuth } from "../context/AuthContext";
import { useNavigate, Link } from "react-router-dom";
import "./Auth.css";

export default function Register() {
  const { register, loading } = useAuth();
  const navigate = useNavigate();

  const schema = Yup.object({
    email: Yup.string()
      .email("Invalid email format")
      .required("Email is required"),
    password: Yup.string()
      .min(8, "Password must be at least 8 characters")
      .matches(/[A-Za-z]/, "Password must contain at least one letter")
      .matches(/[0-9]/, "Password must contain at least one number")
      .required("Password is required"),
    confirmPassword: Yup.string()
      .oneOf([Yup.ref("password"), null], "Passwords must match")
      .required("Please confirm your password"),
  });

  return (
    <div className="auth-container">
      <div className="auth-card">
        <Formik
          initialValues={{ email: "", password: "", confirmPassword: "" }}
          validationSchema={schema}
          onSubmit={async (values, { setSubmitting, setFieldError }) => {
            setSubmitting(true);
            const { confirmPassword, ...registerData } = values;
            const result = await register(registerData);
            
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
              <h2 className="auth-title">Create Account</h2>
              <p className="auth-subtitle">Sign up to get started</p>
              
              <div className="form-group">
                <Field 
                  name="email" 
                  type="email"
                  placeholder="Email address" 
                  className="form-input"
                  disabled={isSubmitting || loading}
                />
                <ErrorMessage name="email" component="div" className="error-message" />
              </div>
              
              <div className="form-group">
                <Field 
                  type="password" 
                  name="password" 
                  placeholder="Password" 
                  className="form-input"
                  disabled={isSubmitting || loading}
                />
                <ErrorMessage name="password" component="div" className="error-message" />
              </div>
              
              <div className="form-group">
                <Field 
                  type="password" 
                  name="confirmPassword" 
                  placeholder="Confirm Password" 
                  className="form-input"
                  disabled={isSubmitting || loading}
                />
                <ErrorMessage name="confirmPassword" component="div" className="error-message" />
              </div>
              
              <button 
                type="submit" 
                disabled={isSubmitting || loading}
                className="auth-button"
              >
                {isSubmitting ? "Creating account..." : "Sign Up"}
              </button>
              
              <div className="auth-links">
                <p>
                  Already have an account?{" "}
                  <Link to="/login" className="auth-link">
                    Sign in
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
