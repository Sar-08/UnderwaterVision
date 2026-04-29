import os
import uuid
import time
from datetime import datetime
from flask import current_app
from ultralytics import YOLO
from services.enhancer_service import enhance_image
from collections import Counter
from PIL import Image


# Load YOLO model only once
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
MODEL_PATH = os.path.join(BASE_DIR, "models", "yolov8s_trashcan.pt")

detector = YOLO(MODEL_PATH)


def compute_severity(total_objects, object_counts):
    """
    Compute a pollution severity score and label.
    Based on total object count and high-risk categories.
    """
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


def process_image_pipeline(file):
    """
    Complete pipeline:
    1. Save uploaded image
    2. Enhance image
    3. Run YOLO detection
    4. Generate enriched summary
    5. Return URLs + summary
    """

    upload_folder = current_app.config["UPLOAD_FOLDER"]
    output_folder = current_app.config["OUTPUT_FOLDER"]

    # ---------- Generate unique filename ----------
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

    # ---------- Detection (timed) ----------
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

    # ---------- Extract detections with bounding boxes ----------
    detections = []

    if result.boxes is not None:
        for box in result.boxes:
            label = result.names[int(box.cls[0])]
            confidence = float(box.conf[0])
            x1, y1, x2, y2 = [round(float(v), 1) for v in box.xyxy[0]]
            width = round(x2 - x1, 1)
            height = round(y2 - y1, 1)

            detections.append({
                "label": label,
                "confidence": round(confidence, 4),
                "confidence_pct": f"{confidence * 100:.1f}%",
                "bbox": {
                    "x1": x1, "y1": y1,
                    "x2": x2, "y2": y2,
                    "width": width, "height": height
                }
            })

    # ---------- Summary Logic ----------
    labels = [d["label"] for d in detections]
    confidences = [d["confidence"] for d in detections]

    object_counts = dict(Counter(labels))
    total_objects = len(labels)

    avg_conf = round(sum(confidences) / total_objects, 4) if total_objects > 0 else 0
    max_conf = round(max(confidences), 4) if confidences else 0
    min_conf = round(min(confidences), 4) if confidences else 0
    most_frequent = max(object_counts, key=object_counts.get) if total_objects > 0 else "None"

    severity = compute_severity(total_objects, object_counts)

    # ---------- Per-class confidence averages ----------
    class_confidences = {}
    for d in detections:
        lbl = d["label"]
        class_confidences.setdefault(lbl, []).append(d["confidence"])

    class_avg_confidence = {
        lbl: round(sum(vals) / len(vals) * 100, 1)
        for lbl, vals in class_confidences.items()
    }

    summary = {
        "total_objects": total_objects,
        "object_counts": object_counts,
        "average_confidence": avg_conf,
        "max_confidence": max_conf,
        "min_confidence": min_conf,
        "most_frequent": most_frequent,
        "class_avg_confidence": class_avg_confidence,
        "severity": severity,
        "processing_time_ms": processing_time_ms,
        "image_metadata": {
            "filename": file.filename,
            "resolution": f"{img_width} x {img_height}",
            "format": img_format,
            "processed_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
    }

    # ---------- Get detected image path ----------
    detected_path = os.path.join(
        result.save_dir,
        os.path.basename(enhanced_path)
    )

    # ---------- Convert paths to frontend URLs ----------
    original_url = f"http://localhost:5000/files/uploads/{original_filename}"
    enhanced_url = f"http://localhost:5000/files/outputs/{enhanced_filename}"
    detected_url = f"http://localhost:5000/files/outputs/detected/{os.path.basename(detected_path)}"

    return {
        "message": "Detection successful",
        "original_image": original_url,
        "enhanced_image": enhanced_url,
        "detected_image": detected_url,
        "detections": detections,
        "summary": summary
    }