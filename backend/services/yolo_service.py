import os
import uuid
from datetime import datetime
from ultralytics import YOLO
from services.enhancer_service import enhance_image
from flask import current_app

# Load YOLO once
detector = YOLO("models/yolov8s_trashcan.pt")


def process_image_pipeline(file):

    upload_folder = current_app.config["UPLOAD_FOLDER"]
    output_folder = current_app.config["OUTPUT_FOLDER"]

    unique_name = datetime.now().strftime("%Y%m%d_%H%M%S_") + str(uuid.uuid4())[:8]

    # -------- Save Original --------
    original_filename = unique_name + "_" + file.filename
    original_path = os.path.join(upload_folder, original_filename)
    file.save(original_path)

    # -------- Enhance --------
    enhanced_filename = "enhanced_" + original_filename
    enhanced_path = os.path.join(output_folder, enhanced_filename)

    enhance_image(original_path, enhanced_path)

    # -------- Detect --------
    results = detector.predict(
        source=enhanced_path,
        imgsz=256,
        conf=0.25,
        save=True,
        project=output_folder,
        name="detected",
        exist_ok=True
    )

    detected_path = os.path.join(
        results[0].save_dir,
        os.path.basename(enhanced_path)
    )

    # -------- Convert to PUBLIC URLs --------
    base_url = "http://localhost:5000/files/"

    return {
        "original_url": base_url + "uploads/" + original_filename,
        "enhanced_url": base_url + "outputs/" + enhanced_filename,
        "detected_url": base_url + "outputs/detected/" + os.path.basename(detected_path)
    }
