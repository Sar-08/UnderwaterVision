from flask import Blueprint, jsonify
from extensions import mongo
from datetime import datetime

history_bp = Blueprint("history", __name__)

@history_bp.route("/", methods=["GET"])
def get_history():
    try:
        history = list(mongo.db.history.find().sort("date", -1))

        for item in history:
            item["_id"] = str(item["_id"])
            item["date"] = item.get("date", datetime.utcnow()).isoformat()

        return jsonify(history)

    except Exception as e:
        return jsonify({"error": str(e)}), 500