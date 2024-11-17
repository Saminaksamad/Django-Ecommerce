import datetime
from flask import Blueprint, request, jsonify
from models.assignment import Assignment
from utils.auth import token_required

# Define a blueprint for user-related routes
user_bp = Blueprint("user", __name__)

@user_bp.route("/upload", methods=["POST"])
@token_required
def upload_assignment(current_user):
    """
    Allows a user to upload an assignment.

    Args:
        current_user (dict): The current authenticated user.

    Expected JSON data:
    {
        "task": "string",  # Description or details of the assignment
        "admin": "string"  # Username of the admin to whom the assignment is addressed
    }

    Returns:
        JSON response indicating success or error.
        Unauthorized response if the user is not a regular user.
    """
    # Ensure that only users with the 'user' role can access this endpoint
    if current_user["role"] != "user":
        return jsonify({"error": "Unauthorized"}), 403

    # Validate the input data
    data = request.json
    if not data or "task" not in data or "admin" not in data:
        return jsonify({"error": "Missing required fields"}), 400

    # Extract fields from the request
    task = data["task"]
    admin = data["admin"]

    # Insert the assignment into the database
    Assignment.insert_one({
        "user_id": current_user["_id"],  # The ID of the user uploading the assignment
        "task": task,                   # The task details
        "admin": admin,                 # The admin assigned to this task
        "status": "pending",            # Default status is 'pending'
        "timestamp": datetime.datetime.utcnow()  # Record the current UTC time
    })

    return jsonify({"message": "Assignment uploaded successfully"})
