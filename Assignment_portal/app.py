from flask import Flask
from pymongo import MongoClient
from config import MONGO_URI
from routes.user_routes import user_bp
from routes.admin_routes import admin_bp
from routes.auth_routes import auth_bp

# Initialize the Flask application
app = Flask(__name__)

# Set the secret key for session management and JWT
app.config["SECRET_KEY"] = "your_secret_key"

# MongoDB connection
# Connect to MongoDB using the URI provided in the config
client = MongoClient(MONGO_URI)
db = client.get_database()

# Register blueprints for modular route management
app.register_blueprint(user_bp, url_prefix="/user")  # Routes related to user functionality
app.register_blueprint(admin_bp, url_prefix="/admins")  # Routes related to admin functionality
app.register_blueprint(auth_bp, url_prefix="/auth")  # Routes related to authentication

# Run the application
if __name__ == "__main__":
    app.run(debug=True)
