import React, { useEffect } from "react";
import axios from "axios";
import { BrowserRouter as Router, Routes, Route } from "react-router-dom";
import "./App.css";
import IdeaForm from "./components/IdeaForm";
import ProjectKanbanBoard from "./components/ProjectKanbanBoard";
import SOPViewerUploader from "./components/SOPViewerUploader";
import KPIDashboard from "./components/KPIDashboard";
import NotificationBell from "./components/NotificationBell";
import CommentsThreadWrapper from "./components/CommentsThreadWrapper";
import NavBar from "./components/NavBar";
import Login from "./components/Login";
import Register from "./components/Register";
import ProtectedRoute from "./components/ProtectedRoute";
import Footer from "./components/Footer";

// Temporarily commenting out problematic imports for testing environment variables
// import { Formik } from 'formik';
// import * as Yup from 'yup';
// import { BarChart } from 'recharts';
// import { DragDropContext } from 'react-beautiful-dnd';

function App() {
  console.log("API URL:", process.env.REACT_APP_API_URL);
  console.log("Sentry DSN:", process.env.REACT_APP_SENTRY_DSN);

  useEffect(() => {
    // Skip all side effects during testing
    if (process.env.NODE_ENV === "test") {
      return;
    }

    // Make API call if we have the API URL
    if (process.env.REACT_APP_API_URL) {
      axios
        .get(`${process.env.REACT_APP_API_URL}/health`)
        .then((res) => console.log("Health:", res.data))
        .catch((err) => console.error("Health-check failed:", err));
    }
  }, []);

  return (
    <Router>
      <div className="App">
        <NavBar />
        <main className="main-content">
          <Routes>
            <Route
              path="/"
              element={
                <div className="welcome-container">
                  <h1>Welcome to The Solution Desk</h1>
                </div>
              }
            />
            <Route path="/login" element={<Login />} />
            <Route path="/register" element={<Register />} />

            {/* Protected Routes */}
            <Route
              path="/ideas/new"
              element={
                <ProtectedRoute>
                  <IdeaForm />
                </ProtectedRoute>
              }
            />
            <Route
              path="/kanban"
              element={
                <ProtectedRoute>
                  <ProjectKanbanBoard />
                </ProtectedRoute>
              }
            />
            <Route
              path="/sop"
              element={
                <ProtectedRoute>
                  <SOPViewerUploader />
                </ProtectedRoute>
              }
            />
            <Route
              path="/kpi"
              element={
                <ProtectedRoute>
                  <KPIDashboard />
                </ProtectedRoute>
              }
            />
            <Route
              path="/entities/:id/comments"
              element={
                <ProtectedRoute>
                  <CommentsThreadWrapper />
                </ProtectedRoute>
              }
            />
          </Routes>
        </main>
        <Footer />
      </div>
    </Router>
  );
}

export default App;
