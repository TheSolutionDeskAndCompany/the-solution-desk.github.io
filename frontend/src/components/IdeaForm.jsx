import React, { useState } from "react";
import axios from "axios";
import { Formik, Form, Field, ErrorMessage } from "formik";
import * as Yup from "yup";
import { toast } from "react-toastify";
import "./IdeaForm.css"; // we'll add theme styles here

export default function IdeaForm() {
  const [submitError, setSubmitError] = useState(null);

  const initialValues = { title: "", description: "" };
  const validationSchema = Yup.object({
    title: Yup.string().required("Required"),
    description: Yup.string().min(10, "Too short").required("Required"),
  });

  const handleSubmit = async (values, { setSubmitting, resetForm }) => {
    setSubmitError(null);
    try {
      await axios.post(`${process.env.REACT_APP_API_URL}/ideas`, values);
      resetForm();
      toast.success("Idea submitted successfully!");
      // you can navigate or show success here
    } catch (err) {
      const msg = err.response?.data?.error || "Submission failed";
      toast.error(msg);
      setSubmitError(msg);
    } finally {
      setSubmitting(false);
    }
  };

  return (
    <div className="idea-form-container cyberpunk-theme">
      {/* Using React logo as a temporary placeholder */}
      <img
        src="/logo192.png"
        alt="Solution Desk Logo"
        className="idea-form-logo"
      />

      <h2>Submit a New Idea</h2>
      <Formik
        initialValues={initialValues}
        validationSchema={validationSchema}
        onSubmit={handleSubmit}
      >
        {({ isSubmitting, touched, errors }) => (
          <Form className="idea-form">
            <label htmlFor="title">Title</label>
            <Field
              name="title"
              placeholder="Idea title"
              aria-invalid={touched.title && errors.title ? "true" : "false"}
            />
            <ErrorMessage
              name="title"
              component="div"
              className="error"
              aria-live="assertive"
            />

            <label htmlFor="description">Description</label>
            <Field
              as="textarea"
              name="description"
              placeholder="Describe your idea"
              aria-invalid={
                touched.description && errors.description ? "true" : "false"
              }
            />
            <ErrorMessage
              name="description"
              component="div"
              className="error"
              aria-live="assertive"
            />

            {submitError && <div className="error">{submitError}</div>}

            <button type="submit" disabled={isSubmitting}>
              {isSubmitting ? (
                <span className="spinner" aria-label="Loading…"></span>
              ) : (
                "Submit"
              )}
            </button>
          </Form>
        )}
      </Formik>
    </div>
  );
}
