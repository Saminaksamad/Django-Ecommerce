from flask import Blueprint, jsonify, request
from models.assignment import Assignment
from utils.auth import token_required

# Define a blueprint for admin-related routes
admin_bp = Blueprint("admin", __name__)

@admin_bp.route("/assignments", methods=["GET"])
@token_required
def view_assignments(current_user):
    """
    View all assignments assigned to the current admin.

    Args:
        current_user (dict): The current authenticated admin user.

    Returns:
        JSON response containing a list of assignments assigned to the admin.
        Unauthorized response if the user is not an admin.
    """
    if current_user["role"] != "admin":
        return jsonify({"error": "Unauthorized"}), 403

    # Fetch assignments assigned to the current admin
    assignments = Assignment.find({"admin": current_user["username"]})

    # Convert MongoDB ObjectId to string for JSON serialization
    for a in assignments:
        a["_id"] = str(a["_id"])

    return jsonify(assignments)

@admin_bp.route("/assignments/<assignment_id>/accept", methods=["POST"])
@token_required
def accept_assignment(current_user, assignment_id):
    """
    Accept an assignment by updating its status to 'Accepted'.

    Args:
        current_user (dict): The current authenticated admin user.
        assignment_id (str): The ID of the assignment to accept.

    Returns:
        JSON response confirming the acceptance of the assignment.
        Unauthorized response if the user is not an admin.
    """
    if current_user["role"] != "admin":
        return jsonify({"error": "Unauthorized!"}), 403

    # Update the assignment status to 'Accepted'
    Assignment.update_one({"_id": assignment_id}, {"$set": {"status": "Accepted"}})
    return jsonify({"message": "Assignment accepted!"})

@admin_bp.route("/assignments/<assignment_id>/reject", methods=["POST"])
@token_required
def reject_assignment(current_user, assignment_id):
    """
    Reject an assignment by updating its status to 'Rejected'.

    Args:
        current_user (dict): The current authenticated admin user.
        assignment_id (str): The ID of the assignment to reject.

    Returns:
        JSON response confirming the rejection of the assignment.
        Unauthorized response if the user is not an admin.
    """
    if current_user["role"] != "admin":
        return jsonify({"error": "Unauthorized!"}), 403

    # Update the assignment status to 'Rejected'
    Assignment.update_one({"_id": assignment_id}, {"$set": {"status": "Rejected"}})
    return jsonify({"message": "Assignment rejected!"})
