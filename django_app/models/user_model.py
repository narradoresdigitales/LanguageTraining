from dotenv import load_dotenv
import os
from pymongo import MongoClient
from hashlib import sha256
from datetime import datetime, timezone
from bson import ObjectId

# Load environment variables
load_dotenv()
MONGO_URI = os.getenv("MONGO_URI")

if not MONGO_URI:
    raise RuntimeError("MONGO_URI is not set")

# MongoDB connection
client = MongoClient(MONGO_URI)
db = client["language_game"]
users_collection = db["users"]


class UserModel:
    @staticmethod
    def create_or_get_user(username: str, password: str):
        pw_hash = sha256(password.encode()).hexdigest()
        user = users_collection.find_one({"username": username})

        if user:
            return {"id": str(user["_id"]), "username": username}

        result = users_collection.insert_one({
            "username": username,
            "password_hash": pw_hash,
            "created_at": datetime.now(timezone.utc),
            "updated_at": datetime.now(timezone.utc)
        })

        return {"id": str(result.inserted_id), "username": username}

    @staticmethod
    def authenticate(username: str, password: str):
        pw_hash = sha256(password.encode()).hexdigest()
        user = users_collection.find_one({
            "username": username,
            "password_hash": pw_hash
        })

        if not user:
            return None

        return {"id": str(user["_id"]), "username": username}

    @staticmethod
    def delete_user(user_id: str) -> bool:
        result = users_collection.delete_one(
            {"_id": ObjectId(user_id)}
        )
        return result.deleted_count == 1
