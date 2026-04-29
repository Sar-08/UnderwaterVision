import React, { useEffect, useState } from "react";
import "./AccountPage.css";
import { useNavigate } from "react-router-dom";

function AccountPage() {
  const [user, setUser] = useState(null);
  const navigate = useNavigate();

  useEffect(() => {
    const storedUser = localStorage.getItem("user");

    if (!storedUser) {
      navigate("/login"); // redirect if not logged in
    } else {
      setUser(JSON.parse(storedUser));
    }
  }, [navigate]);

  const handleLogout = () => {
    localStorage.removeItem("user");
    navigate("/login");
  };

  if (!user) return null;

  return (
    <div className="account-page">

      {/* Header */}
      <div className="account-header">
        <h2>My Account</h2>
        <p>Manage your personal information and settings</p>
      </div>

      <div className="account-container">

        {/* Profile */}
        <div className="profile-card card">
          <div className="avatar">👤</div>
          <h3>{user.username}</h3>
          <p>{user.email || "No email added"}</p>
        </div>

        {/* Details */}
        <div className="details-card card">
          <h3>Personal Details</h3>

          <div className="details-grid">

            <div className="detail-box">
              <label>Name</label>
              <p>{user.username}</p>
            </div>

            <div className="detail-box">
              <label>Email</label>
              <p>{user.email || "Not provided"}</p>
            </div>

            <div className="detail-box">
              <label>Contact</label>
              <p>{user.contact || "Not provided"}</p>
            </div>

            <div className="detail-box">
              <label>Date of Birth</label>
              <p>{user.dob || "Not provided"}</p>
            </div>

          </div>

          {/* Actions */}
          <div className="account-actions">
            <button className="btn logout-btn" onClick={handleLogout}>
              Logout
            </button>

            <button className="btn delete-btn">
              Delete Account
            </button>
          </div>
        </div>

      </div>
    </div>
  );
}

export default AccountPage;