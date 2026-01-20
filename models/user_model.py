# models/user_model.py
from dotenv import load_dotenv
import os
from pymongo import MongoClient
from hashlib import sha256
from datetime import datetime

# -----------------------------
# Load environment variables
# -----------------------------
load_dotenv()
MONGO_URI = os.getenv("MONGO_URI", "")
if not MONGO_URI:
    raise RuntimeError("MONGO_URI is not set in environment variables")

# -----------------------------
# MongoDB connection
# -----------------------------
client = MongoClient(MONGO_URI)
db = client["language_game"]
users_collection = db["users"]

class UserModel:
    @staticmethod
    def create_or_get_user(username: str, password: str):
        """Create a new user if it does not exist, else return existing user."""
        pw_hash = sha256(password.encode()).hexdigest()
        user = users_collection.find_one({"username": username})

        if user:
            # Update password hash in case it changed locally
            if user.get("password_hash") != pw_hash:
                users_collection.update_one(
                    {"_id": user["_id"]},
                    {"$set": {"password_hash": pw_hash, "updated_at": datetime.utcnow()}}
                )
            return {"username": username, "id": str(user["_id"])}

        # User does not exist: create
        result = users_collection.insert_one({
            "username": username,
            "password_hash": pw_hash,
            "created_at": datetime.utcnow(),
            "updated_at": datetime.utcnow()
        })
        return {"username": username, "id": str(result.inserted_id)}

    @staticmethod
    def authenticate(username: str, password: str):
        """Authenticate a user. Returns user dict or None."""
        pw_hash = sha256(password.encode()).hexdigest()
        user = users_collection.find_one({"username": username})
        if user and user.get("password_hash") == pw_hash:
            return {"username": username, "id": str(user["_id"])}
        return None
