from flask import Flask, send_from_directory, jsonify
from flask_cors import CORS
from urllib.parse import quote_plus
from extensions import mongo
import os


def create_app():
    app = Flask(__name__)

    BASE_DIR = os.path.abspath(os.path.dirname(__file__))

    app.config["UPLOAD_FOLDER"] = os.path.join(BASE_DIR, "uploads")
    app.config["OUTPUT_FOLDER"] = os.path.join(BASE_DIR, "outputs")
    app.config["MAX_CONTENT_LENGTH"] = 16 * 1024 * 1024

    username = quote_plus("sonamhussain2004_db_user")
    password = quote_plus("ciCRvsukNSo2ZZNN")   # ← your password from screenshot

    app.config["MONGO_URI"] = (
        f"mongodb+srv://{username}:{password}"
        "@cluster0.dcj2zyl.mongodb.net/myAppDB"
        "?retryWrites=true&w=majority"
    )

    mongo.init_app(app)

    os.makedirs(app.config["UPLOAD_FOLDER"], exist_ok=True)
    os.makedirs(app.config["OUTPUT_FOLDER"], exist_ok=True)

    CORS(app)

    from routes.auth import auth_bp
    from routes.detect import detect_bp
    from routes.history import history_bp

    app.register_blueprint(auth_bp, url_prefix="/api/auth")
    app.register_blueprint(detect_bp, url_prefix="/api/detect")
    app.register_blueprint(history_bp, url_prefix="/api/history")

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

    @app.route("/files/<path:filename>")
    def serve_file(filename):
        return send_from_directory(BASE_DIR, filename)

    @app.route("/test-db")
    def test_db():
        try:
            mongo.db.test.insert_one({"msg": "MongoDB is working"})
            return "MongoDB Connected Successfully ✅"
        except Exception as e:
            return f"Error: {str(e)}"

    @app.route("/api/health")
    def health():
        return jsonify({"status": "Backend running ✅"})

    return app


if __name__ == "__main__":
    app = create_app()
    app.run(host="0.0.0.0", port=5000, debug=True)