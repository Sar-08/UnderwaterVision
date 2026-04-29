import React from "react";
import { Link } from "react-router-dom";
import { FaDownload, FaHome, FaUser, FaHistory, FaSignOutAlt } from "react-icons/fa";
import Upload from "../components/Upload";
import "../App.css";

function Dashboard() {
  return (
    <div className="dashboard-layout">

      {/* Sidebar */}
      <aside className="sidebar">

        <nav className="sidebar-menu">
          <Link to="/" className="menu-item">
            <FaHome /> <span>Home</span>
          </Link>

          <Link to="/account" className="menu-item">
            <FaUser /> <span>Account</span>
          </Link>

          <Link to="/login" className="menu-item logout">
            <FaSignOutAlt /> <span>Logout</span>
          </Link>
        </nav>
      </aside>

      {/* Main Content */}
      <div className="main-content">

        {/* Header (Home-style) */}
        <header className="home-header">
          <div className="logo">🌊 AquaDetect</div>
        </header>

        {/* Content */}
        <div className="dashboard-container">
          <Upload />
        </div>

        {/* Footer */}
        <footer className="dashboard-footer">
          <p>© 2026 AquaDetect | Built for Smart Underwater Detection</p>
        </footer>

      </div>
    </div>
  );
}

export default Dashboard;