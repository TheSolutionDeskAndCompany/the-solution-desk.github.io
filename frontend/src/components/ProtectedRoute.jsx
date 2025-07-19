import React from "react";
import { Navigate } from "react-router-dom";
import { useAuth } from "../context/AuthContext";

// Loading spinner component
const LoadingSpinner = () => (
  <div className="loading-container">
    <div className="loading-spinner"></div>
    <p>Loading...</p>
  </div>
);

export default function ProtectedRoute({ children }) {
  const { isAuthenticated, loading } = useAuth();
  
  // Show loading spinner while checking authentication
  if (loading) {
    return <LoadingSpinner />;
  }
  
  // Redirect to login if not authenticated
  if (!isAuthenticated) {
    return <Navigate to="/login" replace />;
  }
  
  // Render children if authenticated
  return children;
}
