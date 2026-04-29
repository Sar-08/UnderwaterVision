import os
import uuid
import time
from datetime import datetime
from flask import current_app
from ultralytics import YOLO
from services.enhancer_service import enhance_image
from collections import Counter
from PIL import Image
import gdown


# ---------------- BASE PATH ----------------
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))

# 🔥 FINAL MODEL PATH
MODEL_PATH = os.path.join(BASE_DIR, "models", "best.pt")


# ---------------- DOWNLOAD MODEL ----------------
def download_model():
    os.makedirs(os.path.dirname(MODEL_PATH), exist_ok=True)

    # 🔥 👉 PASTE YOUR GOOGLE DRIVE FILE ID HERE
    file_id = "1xBwdl0ksWMvWzgQGw6uDySYmT_ADjWcb"

    url = f"https://drive.google.com/uc?id={file_id}"

    print("📥 Downloading model from Google Drive...")
    gdown.download(url, MODEL_PATH, quiet=False)


# ---------------- LOAD MODEL (SAFE) ----------------
if not os.path.exists(MODEL_PATH):
    download_model()

detector = YOLO(MODEL_PATH)


# ---------------- SEVERITY FUNCTION ----------------
def compute_severity(total_objects, object_counts):
    HIGH_RISK = {"plastic", "metal", "rubber", "chemical"}

    high_risk_count = sum(
        count for label, count in object_counts.items()
        if label.lower() in HIGH_RISK
    )

    if total_objects == 0:
        return {"score": 0, "level": "None", "color": "green"}
    elif total_objects <= 2 and high_risk_count == 0:
        return {"score": 1, "level": "Low", "color": "green"}
    elif total_objects <= 5 or high_risk_count <= 2:
        return {"score": 2, "level": "Moderate", "color": "orange"}
    elif total_objects <= 10 or high_risk_count <= 5:
        return {"score": 3, "level": "High", "color": "red"}
    else:
        return {"score": 4, "level": "Critical", "color": "darkred"}


# ---------------- MAIN PIPELINE ----------------
def process_image_pipeline(file):

    upload_folder = current_app.config["UPLOAD_FOLDER"]
    output_folder = current_app.config["OUTPUT_FOLDER"]

    # ---------- Generate filename ----------
    unique_name = datetime.now().strftime("%Y%m%d_%H%M%S_") + str(uuid.uuid4())[:8]
    original_filename = unique_name + "_" + file.filename
    upload_path = os.path.join(upload_folder, original_filename)
    file.save(upload_path)

    # ---------- Image Metadata ----------
    with Image.open(upload_path) as img:
        img_width, img_height = img.size
        img_format = img.format or os.path.splitext(file.filename)[-1].upper().strip(".")

    # ---------- Enhancement ----------
    enhanced_filename = "enhanced_" + original_filename
    enhanced_path = os.path.join(output_folder, enhanced_filename)
    enhance_image(upload_path, enhanced_path)

    # ---------- Detection ----------
    start_time = time.time()

    results = detector.predict(
        source=enhanced_path,
        imgsz=256,
        conf=0.25,
        save=True,
        project=output_folder,
        name="detected",
        exist_ok=True
    )

    processing_time_ms = round((time.time() - start_time) * 1000, 1)

    result = results[0]

    # ---------- Extract detections ----------
    detections = []

    if result.boxes is not None:
        for box in result.boxes:
            label = result.names[int(box.cls[0])]
            confidence = float(box.conf[0])
            x1, y1, x2, y2 = [round(float(v), 1) for v in box.xyxy[0]]

            detections.append({
                "label": label,
                "confidence": round(confidence, 4),
                "confidence_pct": f"{confidence * 100:.1f}%"
            })

    # ---------- Summary ----------
    labels = [d["label"] for d in detections]
    confidences = [d["confidence"] for d in detections]

    object_counts = dict(Counter(labels))
    total_objects = len(labels)

    avg_conf = round(sum(confidences) / total_objects, 4) if total_objects > 0 else 0
    most_frequent = max(object_counts, key=object_counts.get) if total_objects > 0 else "None"

    severity = compute_severity(total_objects, object_counts)

    summary = {
        "total_objects": total_objects,
        "object_counts": object_counts,
        "average_confidence": avg_conf,
        "most_frequent": most_frequent,
        "severity": severity,
        "processing_time_ms": processing_time_ms
    }

    # ---------- Output paths ----------
    detected_path = os.path.join(
        result.save_dir,
        os.path.basename(enhanced_path)
    )

    # ⚠️ IMPORTANT: dynamic base URL (for deployment)
    base_url = request_host_url()

    return {
        "message": "Detection successful",
        "original_image": f"{base_url}/files/uploads/{original_filename}",
        "enhanced_image": f"{base_url}/files/outputs/{enhanced_filename}",
        "detected_image": f"{base_url}/files/outputs/detected/{os.path.basename(detected_path)}",
        "detections": detections,
        "summary": summary
    }


# ---------------- HELPER ----------------
def request_host_url():
    from flask import request
    return request.host_url.rstrip("/")