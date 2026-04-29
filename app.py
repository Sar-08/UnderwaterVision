from flask import Flask, render_template, request, jsonify
from ultralytics import YOLO
import torch, cv2, os
from datetime import datetime
import numpy as np
from enhancer_model import Enhancer
from pathlib import Path

app = Flask(__name__)

UPLOAD_DIR = "static/results"
os.makedirs(UPLOAD_DIR, exist_ok=True)

device = "cuda" if torch.cuda.is_available() else "cpu"

# Load Models
enhancer = Enhancer("models/funie_generator.pth")
detector = YOLO("models/yolov8s_trashcan.pt")
print("✅ YOLO model loaded successfully")


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/process", methods=["POST"])
def process():
    file = request.files.get("image")
    if file is None:
        return jsonify({"error": "No file uploaded"}), 400

    filename = datetime.now().strftime("%Y%m%d_%H%M%S_") + file.filename

    # ✅ ORIGINAL IMAGE SAVE
    original_path = os.path.join(UPLOAD_DIR, filename)
    file.save(original_path)

    # ✅ READ + RESIZE TO 256 FOR DISPLAY
    img = cv2.imread(original_path)
    resized_original = cv2.resize(img, (256, 256))
    original_256_path = os.path.join(UPLOAD_DIR, "raw256_" + filename)
    cv2.imwrite(original_256_path, resized_original)

    # ✅ ENHANCEMENT
    rgb = cv2.cvtColor(resized_original, cv2.COLOR_BGR2RGB)
    tensor = torch.tensor(rgb / 255.0).permute(2, 0, 1).unsqueeze(0).float()

    enhanced = enhancer.enhance_tensor(tensor)

    enhanced_np = (enhanced.squeeze().permute(1, 2, 0).cpu().numpy() * 255).astype(np.uint8)
    enhanced_bgr = cv2.cvtColor(enhanced_np, cv2.COLOR_RGB2BGR)

    enhanced_path = os.path.join(UPLOAD_DIR, "enhanced_" + filename)
    cv2.imwrite(enhanced_path, enhanced_bgr)

    # ✅ YOLO DETECTION — FORCE SAVE TO STATIC
    results = detector.predict(
        source=enhanced_path,
        imgsz=256,
        conf=0.25,
        save=True,
        project="static",
        name="detected",
        exist_ok=True
    )

    detected_dir = "static/detected"
    detected_image = os.listdir(detected_dir)[-1]
    detected_path = "/" + detected_dir + "/" + detected_image

    return jsonify({
        "original": "/" + original_256_path.replace("\\", "/"),
        "enhanced": "/" + enhanced_path.replace("\\", "/"),
        "detected": detected_path.replace("\\", "/")
    })

if __name__ == "__main__":
    app.run(debug=True)