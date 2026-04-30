import React, { useState } from "react";
import axios from "axios";
import Result from "./Result";
import API from "../api";

function Upload() {
  const [image, setImage] = useState(null);
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);

  const handleUpload = async () => {
    if (!image) return;

    const formData = new FormData();
    formData.append("image", image);

    const user = JSON.parse(localStorage.getItem("user"));
    formData.append("username", user?.username || "guest");

    try {
      setLoading(true);

      const response = await axios.post(
        `${API}/api/detect/process`,
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
        <input type="file" onChange={(e) => setImage(e.target.files[0])} />
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