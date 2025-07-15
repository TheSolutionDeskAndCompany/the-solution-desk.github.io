import React from "react";
import { Formik, Form, Field, ErrorMessage } from "formik";
import * as Yup from "yup";
import { useContext } from "react";
import { AuthContext } from "../context/AuthContext";
import { useNavigate } from "react-router-dom";
import { toast } from "react-toastify";
import "./Auth.css";

export default function Register() {
  const { register } = useContext(AuthContext);
  const navigate = useNavigate();

  const schema = Yup.object({
    name: Yup.string().required(),
    email: Yup.string().email().required(),
    password: Yup.string().min(6).required(),
  });

  return (
    <Formik
      initialValues={{ name: "", email: "", password: "" }}
      validationSchema={schema}
      onSubmit={async (values, { setSubmitting }) => {
        try {
          await register(values);
          toast.success("Registered!");
          navigate("/");
        } catch {
          toast.error("Registration failed");
        } finally {
          setSubmitting(false);
        }
      }}
    >
      {({ isSubmitting }) => (
        <Form className="cyberpunk-theme">
          <h2>Register</h2>
          <Field name="name" placeholder="Name" />
          <ErrorMessage name="name" component="div" className="error" />
          <Field name="email" placeholder="Email" />
          <ErrorMessage name="email" component="div" className="error" />
          <Field type="password" name="password" placeholder="Password" />
          <ErrorMessage name="password" component="div" className="error" />
          <button type="submit" disabled={isSubmitting}>
            {isSubmitting ? "Registering…" : "Register"}
          </button>
        </Form>
      )}
    </Formik>
  );
}
