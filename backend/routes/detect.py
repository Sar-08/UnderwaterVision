from flask import Blueprint, request, jsonify
from services.pipeline_service import process_image_pipeline
from extensions import mongo
from datetime import datetime

detect_bp = Blueprint("detect", __name__)


@detect_bp.route("/process", methods=["POST"])
def process_image():
    try:
        if "image" not in request.files:
            return jsonify({"error": "No image file provided"}), 400

        file = request.files["image"]

        if file.filename == "":
            return jsonify({"error": "Empty filename"}), 400

        # 🔥 Get username from frontend
        username = request.form.get("username")

        # Run pipeline
        result = process_image_pipeline(file)

        # 🔥 Save to MongoDB
        mongo.db.history.insert_one({
            "username": username,
            "date": datetime.now(),
            "output_path": result.get("output_path"),
            "report_path": result.get("report_path"),
            "total_objects": result.get("total_objects", 0),
            "types": result.get("detected_classes", [])
        })

        return jsonify(result)

    except Exception as e:
        return jsonify({"error": str(e)}), 500