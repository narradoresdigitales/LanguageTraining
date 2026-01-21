# models/user_model.py
from dotenv import load_dotenv
import os
from pymongo import MongoClient
from hashlib import sha256
from datetime import datetime, timezone
from bson import ObjectId

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
            # Keep password hash in sync (simple approach for this project)
            if user.get("password_hash") != pw_hash:
                users_collection.update_one(
                    {"_id": user["_id"]},
                    {
                        "$set": {
                            "password_hash": pw_hash,
                            "updated_at": datetime.now(timezone.utc)
                        }
                    }
                )
            return {"username": username, "id": str(user["_id"])}

        # Create new user
        result = users_collection.insert_one({
            "username": username,
            "password_hash": pw_hash,
            "created_at": datetime.now(timezone.utc),
            "updated_at": datetime.now(timezone.utc) 
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

    @staticmethod
    def get_user_by_id(user_id: str):
        user = users_collection.find_one({"_id": ObjectId(user_id)})
        if user:
            return {"username": user["username"], "id": str(user["_id"])}
        return None

    @staticmethod
    def delete_user(user_id: str) -> bool:
        result = users_collection.delete_one(
            {"_id": ObjectId(user_id)}
        )
        return result.deleted_count == 1
