import React, { useState } from "react";
import axios from "axios";
import Result from "./Result";
import { useNavigate } from "react-router-dom";

function Upload() {
  const [image, setImage] = useState(null);
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);

  const navigate = useNavigate();

  const handleUpload = async () => {
  if (!image) return;

  const formData = new FormData();
  formData.append("image", image);

  // ✅ Send username
  const user = JSON.parse(localStorage.getItem("user"));
  formData.append("username", user?.username || "guest");

  try {
    setLoading(true);

    const response = await axios.post(
      "http://localhost:5000/api/detect/process",
      formData,
      { headers: { "Content-Type": "multipart/form-data" } }
    );

    setResult(response.data);
  } catch (error) {
    console.error(error);
  } finally {
    setLoading(false);
  }
};

  return (
    <div>
      <h1>Underwater Trash Detection</h1>

      <div className="upload-box">
        <input
          type="file"
          onChange={(e) => setImage(e.target.files[0])}
        />
        <br /><br />
        <button onClick={handleUpload}>
          {loading ? "Processing..." : "Upload & Detect"}
        </button>
      </div>

      {result && <Result data={result} />}
    </div>
  );
}

export default Upload;