from flask import Flask, send_from_directory, jsonify
from flask_cors import CORS
from extensions import mongo
import os


def create_app():
    app = Flask(__name__)

    BASE_DIR = os.path.abspath(os.path.dirname(__file__))

    # ---------------- CONFIG ----------------
    app.config["UPLOAD_FOLDER"] = os.path.join(BASE_DIR, "uploads")
    app.config["OUTPUT_FOLDER"] = os.path.join(BASE_DIR, "outputs")
    app.config["MAX_CONTENT_LENGTH"] = 16 * 1024 * 1024

    # 🔥 MongoDB URI from ENV (SECURE)
    app.config["MONGO_URI"] = os.environ.get(
        "MONGO_URI",
        "mongodb://localhost:27017/myAppDB"  # fallback for local use
    )

    # Initialize MongoDB
    mongo.init_app(app)

    # Create folders
    os.makedirs(app.config["UPLOAD_FOLDER"], exist_ok=True)
    os.makedirs(app.config["OUTPUT_FOLDER"], exist_ok=True)

    # ---------------- CORS ----------------
    CORS(app)

    # ---------------- ROUTES ----------------
    from routes.auth import auth_bp
    from routes.detect import detect_bp
    from routes.history import history_bp

    app.register_blueprint(auth_bp, url_prefix="/api/auth")
    app.register_blueprint(detect_bp, url_prefix="/api/detect")
    app.register_blueprint(history_bp, url_prefix="/api/history")

    # ---------------- ROOT ----------------
    @app.route("/")
    def home():
        return jsonify({
            "message": "Backend is running ✅",
            "routes": [
                "/api/health",
                "/api/auth/register",
                "/api/auth/login",
                "/api/detect/process",
                "/api/history"
            ]
        })

    # ---------------- FILE SERVING ----------------
    @app.route("/files/<path:filename>")
    def serve_file(filename):
        return send_from_directory(BASE_DIR, filename)

    # ---------------- TEST DB ----------------
    @app.route("/test-db")
    def test_db():
        try:
            mongo.db.test.insert_one({"msg": "MongoDB is working"})
            return "MongoDB Connected Successfully ✅"
        except Exception as e:
            return f"Error: {str(e)}"

    # ---------------- HEALTH ----------------
    @app.route("/api/health")
    def health():
        return jsonify({"status": "Backend running ✅"})

    return app


if __name__ == "__main__":
    app = create_app()

    # 🔥 IMPORTANT FOR DEPLOYMENT (Render, etc.)
    port = int(os.environ.get("PORT", 5000))

    app.run(host="0.0.0.0", port=port, debug=True)