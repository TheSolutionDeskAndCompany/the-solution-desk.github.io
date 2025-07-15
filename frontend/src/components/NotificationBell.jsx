import React, { useEffect, useState, useRef } from "react";
import axios from "axios";
import "./NotificationBell.css";

export default function NotificationBell() {
  const [count, setCount] = useState(0);
  const [notifications, setNotifications] = useState([]);
  const [showDropdown, setShowDropdown] = useState(false);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const dropdownRef = useRef(null);

  useEffect(() => {
    const fetchCount = async () => {
      try {
        const res = await axios.get(
          `${process.env.REACT_APP_API_URL}/notifications/unread/count`,
        );
        setCount(res.data.count);
        setError(null);
      } catch (err) {
        console.error("Failed to fetch notification count:", err);
        setError("Could not load notifications");
      }
    };

    fetchCount();
    const interval = setInterval(fetchCount, 30000); // refresh every 30s

    return () => clearInterval(interval);
  }, []);

  useEffect(() => {
    // Close dropdown when clicking outside
    const handleClickOutside = (event) => {
      if (dropdownRef.current && !dropdownRef.current.contains(event.target)) {
        setShowDropdown(false);
      }
    };

    document.addEventListener("mousedown", handleClickOutside);
    return () => {
      document.removeEventListener("mousedown", handleClickOutside);
    };
  }, []);

  const handleToggleDropdown = async () => {
    const newShowDropdown = !showDropdown;
    setShowDropdown(newShowDropdown);

    // If opening dropdown, fetch notifications
    if (newShowDropdown && notifications.length === 0) {
      setLoading(true);
      try {
        const res = await axios.get(
          `${process.env.REACT_APP_API_URL}/notifications`,
        );
        setNotifications(res.data);
        setError(null);
      } catch (err) {
        console.error("Failed to fetch notifications:", err);
        setError("Could not load notifications");
      } finally {
        setLoading(false);
      }
    }
  };

  const handleMarkAsRead = async (notificationId) => {
    try {
      await axios.post(
        `${process.env.REACT_APP_API_URL}/notifications/${notificationId}/read`,
      );

      // Update local state
      setNotifications((prev) =>
        prev.map((notification) =>
          notification.id === notificationId
            ? { ...notification, read: true }
            : notification,
        ),
      );

      // Decrement count if it's greater than 0
      setCount((prev) => Math.max(0, prev - 1));
    } catch (err) {
      console.error("Failed to mark notification as read:", err);
    }
  };

  const formatDate = (dateString) => {
    const date = new Date(dateString);
    const now = new Date();

    // If today, just show time
    if (date.toDateString() === now.toDateString()) {
      return date.toLocaleTimeString([], {
        hour: "2-digit",
        minute: "2-digit",
      });
    }

    // If this year, show month and day
    if (date.getFullYear() === now.getFullYear()) {
      return date.toLocaleDateString([], { month: "short", day: "numeric" });
    }

    // Otherwise show full date
    return date.toLocaleDateString();
  };

  return (
    <div className="notification-bell-container" ref={dropdownRef}>
      <div
        className="notification-bell"
        onClick={handleToggleDropdown}
        aria-label={`Notifications: ${count} unread`}
      >
        <span className="bell-icon">🔔</span>
        {count > 0 && <span className="badge">{count}</span>}
      </div>

      {showDropdown && (
        <div className="notifications-dropdown">
          <h3 className="notifications-title">Notifications</h3>

          {loading ? (
            <div className="notifications-loading">Loading...</div>
          ) : error ? (
            <div className="notifications-error">{error}</div>
          ) : notifications.length === 0 ? (
            <div className="no-notifications">No new notifications</div>
          ) : (
            <ul className="notifications-list">
              {notifications.map((notification) => (
                <li
                  key={notification.id}
                  className={`notification-item ${notification.read ? "read" : "unread"}`}
                  onClick={() =>
                    !notification.read && handleMarkAsRead(notification.id)
                  }
                >
                  <div className="notification-content">
                    <div className="notification-text">
                      {notification.message}
                    </div>
                    <div className="notification-meta">
                      <span className="notification-time">
                        {formatDate(notification.timestamp || new Date())}
                      </span>
                      {!notification.read && (
                        <span className="unread-indicator">●</span>
                      )}
                    </div>
                  </div>
                </li>
              ))}
            </ul>
          )}
        </div>
      )}
    </div>
  );
}
