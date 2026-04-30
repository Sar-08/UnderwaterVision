import React, { useEffect, useState } from "react";
import axios from "axios";
import "./History.css";
import API from "../api";

function History() {
  const [history, setHistory] = useState([]);

  useEffect(() => {
    axios.get(`${API}/api/history`)
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
            <img
              src={`${API}/files/${item.output_path}`}
              alt="result"
              className="history-img"
            />

            <div className="history-info">
              <p>📅 {formatDate(item.date)}</p>
              <p>🎯 Objects: {item.total_objects || 0}</p>
              <p>📊 Types: {item.types?.join(", ") || "None"}</p>

              <a
                href={`${API}/files/${item.output_path}`}
                download
                className="download-btn"
              >
                Download Image
              </a>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}

export default History;