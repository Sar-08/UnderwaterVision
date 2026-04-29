from flask import Blueprint, request, jsonify
from extensions import mongo
from werkzeug.security import generate_password_hash, check_password_hash

auth_bp = Blueprint("auth", __name__)


@auth_bp.route("/register", methods=["POST"])
def register():
    data = request.json

    if not data or "username" not in data or "password" not in data:
        return jsonify({"error": "Missing username or password"}), 400

    existing_user = mongo.db.users.find_one({"username": data["username"]})
    if existing_user:
        return jsonify({"error": "Username already exists"}), 409

    hashed_pw = generate_password_hash(data["password"])
    mongo.db.users.insert_one({
        "username": data["username"],
        "email": data.get("email", ""),   # ✅ email is optional
        "password": hashed_pw
    })

    return jsonify({"message": "User registered successfully", "username": data["username"]}), 201


@auth_bp.route("/login", methods=["POST"])
def login():
    data = request.json

    if not data or "username" not in data or "password" not in data:
        return jsonify({"error": "Missing username or password"}), 400

    user = mongo.db.users.find_one({"username": data["username"]})

    if not user or not check_password_hash(user["password"], data["password"]):
        return jsonify({"error": "Invalid username or password"}), 401

    return jsonify({
        "message": "Login successful",
        "user": {
            "username": user["username"],
            "email": user.get("email", ""),
            "contact": user.get("contact", ""),
            "dob": user.get("dob", "")
        }
    }), 200