import React from "react";
import { Link } from "react-router-dom";
import "../App.css";

function Home() {
  return (
    <div className="home-wrapper">
      
      {/* Header */}
      <header className="home-header">
        <div className="logo">
          🌊 UnderwaterVision
        </div>

        <nav className="nav-links">
          <Link to="/login" className="hero-btn secondary nav-login">Login</Link>
          <Link to="/register" className="nav-btn primary">Sign Up</Link>
        </nav>
      </header>

      {/* Hero Section */}
      <section className="hero">
        <h1>Underwater Detection Report Generator</h1>
        <p>
          AI-powered detection and enhancement system designed to
          identify underwater objects with precision and clarity.
        </p>

        <div className="hero-buttons">
          <Link to="/login" className="hero-btn primary">
            Get Started
          </Link>
          <Link to="/dashboard" className="hero-btn secondary">
            Try Demo
          </Link>
        </div>
      </section>

      {/* Features Section */}
      <section className="features">
        <div className="feature-card">
          <h3>Image Enhancement</h3>
          <p>Improves underwater visibility before detection.</p>
        </div>

        <div className="feature-card">
          <h3>Object Detection</h3>
          <p>Accurate trash detection using deep learning.</p>
        </div>

        <div className="feature-card">
          <h3>Downloadable Detection Report</h3>
          <p>Download the detection report generated.</p>
        </div>
      </section>

      {/* Footer */}
      <footer className="footer">
        © 2026 UnderwaterVision | Built for Marine Sustainability
      </footer>

    </div>
  );
}

export default Home;