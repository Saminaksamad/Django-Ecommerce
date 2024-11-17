import jwt
from datetime import datetime, timezone, timedelta
from flask import Blueprint, request, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
from config import SECRET_KEY
from models.user import User

# Define a blueprint for authentication-related routes
auth_bp = Blueprint("auth", __name__)

@auth_bp.route("/register", methods=["POST"])
def register():
    """
    Registers a new user by creating an entry in the database.

    Expected JSON data:
    {
        "username": "string",
        "password": "string",
        "role": "string"  # e.g., "user" or "admin"
    }

    Returns:
        JSON response indicating success or error.
    """
    data = request.json

    # Validate required fields
    if not data or "username" not in data or "password" not in data or "role" not in data:
        return jsonify({"error": "Missing required fields"}), 400

    username = data["username"]
    password = data["password"]
    role = data["role"]

    # Check if username already exists
    if User.find_one({"username": username}):
        return jsonify({"error": "Username already exists"}), 400

    # Hash the password and insert the new user into the database
    hashed_password = generate_password_hash(password)
    User.insert_one({
        "username": username,
        "password": hashed_password,
        "role": role
    })

    return jsonify({"message": "User registered successfully"})

@auth_bp.route("/login", methods=["POST"])
def login():
    """
    Authenticates a user and generates a JWT token upon successful login.

    Expected JSON data:
    {
        "username": "string",
        "password": "string"
    }

    Returns:
        JSON response containing a JWT token or an error message.
    """
    data = request.json

    # Validate required fields
    if not data or "username" not in data or "password" not in data:
        return jsonify({"error": "Missing required fields"}), 400

    username = data["username"]
    password = data["password"]

    # Fetch the user from the database
    user = User.find_one({"username": username})
    if user and check_password_hash(user["password"], password):
        # Generate JWT token with 1-hour expiration
        token = jwt.encode(
            {
                "user_id": str(user["_id"]),
                "role": user["role"],
                "exp": datetime.now(timezone.utc) + timedelta(hours=1)
            },
            SECRET_KEY,
            algorithm="HS256"
        )

        return jsonify({"token": token})
    
    # Invalid username or password
    return jsonify({"error": "Invalid username or password!"}), 401
