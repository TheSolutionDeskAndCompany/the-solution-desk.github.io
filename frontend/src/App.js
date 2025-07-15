import React, { useEffect } from "react";
import axios from "axios";
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import logo from "./logo.svg";
import "./App.css";
import IdeaForm from "./components/IdeaForm";
import ProjectKanbanBoard from "./components/ProjectKanbanBoard";
import SOPViewerUploader from "./components/SOPViewerUploader";
import KPIDashboard from "./components/KPIDashboard";
import NotificationBell from "./components/NotificationBell";
import CommentsThreadWrapper from "./components/CommentsThreadWrapper";

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
    if (process.env.NODE_ENV === 'test') {
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
        <header className="App-header">
          <div className="header-content">
            <img src={logo} className="App-logo" alt="logo" />
            <div className="header-right">
              <NotificationBell />
            </div>
          </div>
        </header>
        <Routes>
          <Route path="/" element={
            <div>
              <h1>Welcome to The Solution Desk</h1>
              <div className="nav-links">
                <a href="/ideas/new" className="cyberpunk-link">Submit a New Idea</a>
                <a href="/kanban" className="cyberpunk-link">Project Kanban Board</a>
                <a href="/sop" className="cyberpunk-link">SOP Documents</a>
                <a href="/kpi" className="cyberpunk-link">KPI Dashboard</a>
              </div>
            </div>
          } />
          <Route path="/ideas/new" element={<IdeaForm />} />
          <Route path="/kanban" element={<ProjectKanbanBoard />} />
          <Route path="/sop" element={<SOPViewerUploader />} />
          <Route path="/kpi" element={<KPIDashboard />} />
          <Route path="/entities/:id/comments" element={<CommentsThreadWrapper />} />
        </Routes>
      </div>
    </Router>
  );
}

export default App;
