import React, { createContext, useState, useEffect, useContext } from "react";
import axios from "axios";
import { toast } from "react-toastify";

export const AuthContext = createContext();

// Custom hook to use auth context
export const useAuth = () => {
  const context = useContext(AuthContext);
  if (!context) {
    throw new Error("useAuth must be used within an AuthProvider");
  }
  return context;
};

// Create axios instance with interceptors
const createAxiosInstance = () => {
  const instance = axios.create({
    baseURL: process.env.REACT_APP_API_URL || "http://localhost:5000",
    timeout: 10000,
    headers: {
      "Content-Type": "application/json",
    },
  });

  // Request interceptor to add auth token
  instance.interceptors.request.use(
    (config) => {
      const token = localStorage.getItem("token");
      if (token) {
        config.headers.Authorization = `Bearer ${token}`;
      }
      return config;
    },
    (error) => {
      return Promise.reject(error);
    }
  );

  // Response interceptor to handle 401 errors
  instance.interceptors.response.use(
    (response) => response,
    (error) => {
      if (error.response?.status === 401) {
        // Token is invalid or expired
        localStorage.removeItem("token");
        delete axios.defaults.headers.common["Authorization"];
        window.location.href = "/login";
        toast.error("Session expired. Please log in again.");
      }
      return Promise.reject(error);
    }
  );

  return instance;
};

export const api = createAxiosInstance();

export function AuthProvider({ children }) {
  const [user, setUser] = useState(null);
  const [loading, setLoading] = useState(true);
  const [isAuthenticated, setIsAuthenticated] = useState(false);

  // Check if user is authenticated on app load
  useEffect(() => {
    const initializeAuth = async () => {
      const token = localStorage.getItem("token");
      if (token) {
        try {
          // Verify token and get user data
          const response = await api.get("/api/auth/me");
          setUser(response.data.user);
          setIsAuthenticated(true);
        } catch (error) {
          console.error("Token verification failed:", error);
          localStorage.removeItem("token");
          setUser(null);
          setIsAuthenticated(false);
        }
      }
      setLoading(false);
    };

    initializeAuth();
  }, []);

  const login = async (credentials) => {
    try {
      setLoading(true);
      const response = await api.post("/api/auth/login", credentials);
      const { token, user: userData } = response.data;
      
      localStorage.setItem("token", token);
      setUser(userData);
      setIsAuthenticated(true);
      
      toast.success("Login successful!");
      return { success: true, user: userData };
    } catch (error) {
      const errorMessage = error.response?.data?.error || "Login failed";
      toast.error(errorMessage);
      return { success: false, error: errorMessage };
    } finally {
      setLoading(false);
    }
  };

  const register = async (details) => {
    try {
      setLoading(true);
      const response = await api.post("/api/auth/register", details);
      const { token, user: userData } = response.data;
      
      localStorage.setItem("token", token);
      setUser(userData);
      setIsAuthenticated(true);
      
      toast.success("Registration successful!");
      return { success: true, user: userData };
    } catch (error) {
      const errorMessage = error.response?.data?.error || "Registration failed";
      toast.error(errorMessage);
      return { success: false, error: errorMessage };
    } finally {
      setLoading(false);
    }
  };

  const logout = () => {
    localStorage.removeItem("token");
    setUser(null);
    setIsAuthenticated(false);
    toast.info("You have been logged out.");
  };

  const refreshToken = async () => {
    try {
      const response = await api.post("/api/auth/refresh");
      const { token } = response.data;
      localStorage.setItem("token", token);
      return true;
    } catch (error) {
      console.error("Token refresh failed:", error);
      logout();
      return false;
    }
  };

  const value = {
    user,
    loading,
    isAuthenticated,
    login,
    register,
    logout,
    refreshToken,
  };

  return (
    <AuthContext.Provider value={value}>
      {children}
    </AuthContext.Provider>
  );
}
