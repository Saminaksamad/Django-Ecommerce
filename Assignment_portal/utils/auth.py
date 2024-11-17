import jwt
from functools import wraps
from flask import request, jsonify
from models.user import User
from config import SECRET_KEY

def token_required(f):
    """
    A decorator to protect routes with token-based authentication.

    Verifies that a valid JWT is provided in the 'Authorization' header of the request.
    Extracts and validates the token, retrieves the current user from the database,
    and passes the user object to the wrapped route function.

    Args:
        f (function): The route function to be wrapped.

    Returns:
        JSON response:
        - 401 Unauthorized: If the token is missing, expired, or invalid.
        - Function response: If the token is valid and user exists.
    """
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None

        # Extract token from Authorization header
        if "Authorization" in request.headers:
            auth_header = request.headers["Authorization"]
            if auth_header.startswith("Bearer "):
                token = auth_header.split(" ")[1]  # Remove "Bearer " prefix

        # If no token is provided, return an error
        if not token:
            return jsonify({"error": "Token is missing!"}), 401

        try:
            # Decode the token and extract payload
            data = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
            # Retrieve the current user from the database
            current_user = User.find_one({"_id": data["user_id"]})
            if not current_user:
                return jsonify({"error": "Invalid token!"}), 401
        except jwt.ExpiredSignatureError:
            # Handle expired token
            return jsonify({"error": "Token has expired!"}), 401
        except jwt.InvalidTokenError:
            # Handle invalid token
            return jsonify({"error": "Invalid token!"}), 401

        # Pass the current user to the wrapped function
        return f(current_user, *args, **kwargs)

    return decorated
