import React, { useContext, useState } from "react";
import { Link } from "react-router-dom";
import { AuthContext } from "../context/AuthContext";
import NotificationBell from "./NotificationBell";
import Logo from "../assets/logo.svg";
import "./NavBar.css";

export default function NavBar() {
  const { user, logout } = useContext(AuthContext);
  const [isMobileMenuOpen, setIsMobileMenuOpen] = useState(false);

  const toggleMobileMenu = () => {
    setIsMobileMenuOpen(!isMobileMenuOpen);
  };

  const closeMobileMenu = () => {
    setIsMobileMenuOpen(false);
  };

  return (
    <nav className="navbar">
      <div className="navbar-container">
        {/* Logo */}
        <Link to="/" className="navbar-logo" onClick={closeMobileMenu}>
          <img src={Logo} alt="The Solution Desk" className="logo-image" />
        </Link>

        {/* Desktop Navigation */}
        <div className="navbar-menu">
          <div className="navbar-nav">
            <Link to="/ideas/new" className="nav-link">
              <span className="nav-icon">💡</span>
              New Idea
            </Link>
            <Link to="/kanban" className="nav-link">
              <span className="nav-icon">📋</span>
              Kanban
            </Link>
            <Link to="/sop" className="nav-link">
              <span className="nav-icon">📚</span>
              SOPs
            </Link>
            <Link to="/kpi" className="nav-link">
              <span className="nav-icon">📊</span>
              KPI
            </Link>
          </div>

          <div className="navbar-actions">
            {user ? (
              <>
                <NotificationBell />
                <div className="user-menu">
                  <span className="user-email">{user.email}</span>
                  <button onClick={logout} className="btn btn-ghost logout-btn">
                    Logout
                  </button>
                </div>
              </>
            ) : (
              <div className="auth-buttons">
                <Link to="/login" className="btn btn-ghost">
                  Login
                </Link>
                <Link to="/register" className="btn btn-primary">
                  Get Started
                </Link>
              </div>
            )}
          </div>
        </div>

        {/* Mobile Menu Button */}
        <button
          className={`mobile-menu-btn ${isMobileMenuOpen ? 'active' : ''}`}
          onClick={toggleMobileMenu}
          aria-label="Toggle navigation menu"
          aria-expanded={isMobileMenuOpen}
        >
          <span className="hamburger-line"></span>
          <span className="hamburger-line"></span>
          <span className="hamburger-line"></span>
        </button>
      </div>

      {/* Mobile Navigation */}
      <div className={`mobile-menu ${isMobileMenuOpen ? 'active' : ''}`}>
        <div className="mobile-nav">
          <Link to="/ideas/new" className="mobile-nav-link" onClick={closeMobileMenu}>
            <span className="nav-icon">💡</span>
            New Idea
          </Link>
          <Link to="/kanban" className="mobile-nav-link" onClick={closeMobileMenu}>
            <span className="nav-icon">📋</span>
            Kanban
          </Link>
          <Link to="/sop" className="mobile-nav-link" onClick={closeMobileMenu}>
            <span className="nav-icon">📚</span>
            SOPs
          </Link>
          <Link to="/kpi" className="mobile-nav-link" onClick={closeMobileMenu}>
            <span className="nav-icon">📊</span>
            KPI
          </Link>
        </div>

        <div className="mobile-actions">
          {user ? (
            <>
              <div className="mobile-user-info">
                <span className="user-email">{user.email}</span>
              </div>
              <button onClick={() => { logout(); closeMobileMenu(); }} className="btn btn-ghost logout-btn">
                Logout
              </button>
            </>
          ) : (
            <div className="mobile-auth-buttons">
              <Link to="/login" className="btn btn-ghost" onClick={closeMobileMenu}>
                Login
              </Link>
              <Link to="/register" className="btn btn-primary" onClick={closeMobileMenu}>
                Get Started
              </Link>
            </div>
          )}
        </div>
      </div>
    </nav>
  );
}
