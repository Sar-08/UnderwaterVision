import React, { useEffect, useState } from "react";
import axios from "axios";
import "./History.css";

function History() {
  const [history, setHistory] = useState([]);

  useEffect(() => {
    axios
      .get("http://localhost:5000/api/history")
      .then((res) => setHistory(res.data))
      .catch((err) => console.error(err));
  }, []);

  const formatDate = (dateStr) => {
    if (!dateStr) return "No Date";
    const d = new Date(dateStr);
    return isNaN(d) ? "Invalid Date" : d.toLocaleString();
  };

  return (
    <div className="history-page">
      <h2>Detection History</h2>

      <div className="history-grid">
        {history.length === 0 && <p>No history found</p>}

        {history.map((item, index) => (
          <div className="history-card" key={index}>
            
            {/* IMAGE */}
            <img
              src={`http://localhost:5000/files/${item.detected}`}
              alt="result"
              className="history-img"
            />

            {/* INFO */}
            <div className="history-info">
              <p>📅 {formatDate(item.createdAt)}</p>

              <p>
                🎯 Objects: {item.summary?.total_objects || 0}
              </p>

              <p>
                📊 Types:{" "}
                {item.summary?.object_types
                  ? Object.keys(item.summary.object_types).join(", ")
                  : "None"}
              </p>

              {/* DOWNLOAD BUTTON */}
              <a
                href={`http://localhost:5000/files/${item.detected}`}
                download
                className="download-btn"
              >
                Download Report
              </a>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}

export default History;