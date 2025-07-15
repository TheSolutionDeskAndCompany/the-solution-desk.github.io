import React, { useContext } from 'react';
import { Link } from 'react-router-dom';
import { AuthContext } from '../context/AuthContext';
import NotificationBell from './NotificationBell';
import './NavBar.css';

export default function NavBar() {
  const { user, logout } = useContext(AuthContext);

  return (
    <nav className="navbar cyberpunk-theme">
      <Link to="/" className="nav-logo">YourLogo</Link>
      <div className="nav-links">
        <Link to="/ideas/new">New Idea</Link>
        <Link to="/kanban">Kanban</Link>
        <Link to="/sop">SOPs</Link>
        <Link to="/kpi">KPI</Link>
        {user ? (
          <>
            <NotificationBell />
            <button onClick={logout} className="nav-logout">Logout</button>
          </>
        ) : (
          <>
            <Link to="/login">Login</Link>
            <Link to="/register">Register</Link>
          </>
        )}
      </div>
    </nav>
  );
}
