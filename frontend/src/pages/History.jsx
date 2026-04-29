import React, { useEffect, useState } from "react";
import axios from "axios";
import "./History.css";
import { useNavigate } from "react-router-dom";

function History() {
  const [history, setHistory] = useState([]);
  const navigate = useNavigate();

  useEffect(() => {
    const user = JSON.parse(localStorage.getItem("user"));

    if (!user) {
      navigate("/login");
      return;
    }

    fetchHistory(user.username);
  }, [navigate]);

  const fetchHistory = async (username) => {
    try {
      const res = await axios.get(
        `http://localhost:5000/api/history/${username}`
      );
      setHistory(res.data.history);
    } catch (err) {
      console.error(err);
      alert("Failed to load history");
    }
  };

  return (
    <div className="history-page">
      <h2 className="history-title">Detection History</h2>

      {history.length === 0 ? (
        <p className="empty-text">No detections yet</p>
      ) : (
        <div className="history-grid">
          {history.map((item, index) => (
            <div className="history-card" key={index}>
              
              <img
                src={`http://localhost:5000/files/${item.output_path}`}
                alt="result"
              />

              <div className="history-content">
                <h4>{item.title || "Detection Result"}</h4>

                <p>📅 {new Date(item.date).toLocaleString()}</p>

                <p>🧠 Objects: {item.total_objects}</p>

                <p>📊 Types: {item.types?.join(", ")}</p>

                <a
                  href={`http://localhost:5000/files/${item.report_path}`}
                  className="download-btn"
                  target="_blank"
                  rel="noreferrer"
                >
                  Download Report
                </a>

              </div>
            </div>
          ))}
        </div>
      )}
    </div>
  );
}

export default History;