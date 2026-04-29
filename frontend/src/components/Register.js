import React, { useState } from "react";
import axios from "axios";
import "./Auth.css";
import { useNavigate } from "react-router-dom";

function Register() {
  const [username, setUsername] = useState("");
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [confirmPassword, setConfirmPassword] = useState("");
  const [loading, setLoading] = useState(false);
  const navigate = useNavigate();

  const handleRegister = async () => {
    // ✅ Validate fields
    if (!username || !email || !password || !confirmPassword) {
      alert("Please fill in all fields");
      return;
    }

    if (password !== confirmPassword) {
      alert("Passwords do not match");
      return;
    }

    setLoading(true);

    try {
      const response = await axios.post(
        "http://localhost:5000/api/auth/register",
        { username, email, password },
        { headers: { "Content-Type": "application/json" } }
      );

      console.log("Register response:", response.data);
      alert("Account created successfully ✅");
      navigate("/login");

    } catch (err) {
      console.error("Register error:", err);
      if (err.response) {
        alert(`Registration failed: ${err.response.data.error}`);
      } else {
        alert("Cannot connect to server. Is backend running on port 5000?");
      }
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="auth-wrapper">
      <div className="auth-card">
        <h2>Create New Account</h2>

        <input
          type="text"
          placeholder="Username"
          value={username}
          onChange={(e) => setUsername(e.target.value)}
        />

        <input
          type="email"
          placeholder="Email"
          value={email}
          onChange={(e) => setEmail(e.target.value)}
        />

        <input
          type="password"
          placeholder="Password"
          value={password}
          onChange={(e) => setPassword(e.target.value)}
        />

        <input
          type="password"
          placeholder="Confirm Password"
          value={confirmPassword}
          onChange={(e) => setConfirmPassword(e.target.value)}
        />

        <button onClick={handleRegister} disabled={loading}>
          {loading ? "Creating Account..." : "Sign Up"}
        </button>

        <a href="/login" className="auth-link">
          Already have an account? Log In
        </a>
      </div>
    </div>
  );
}

export default Register;