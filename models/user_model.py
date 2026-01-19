import os
import json
from hashlib import sha256
from pymongo import MongoClient
from bson.objectid import ObjectId
from dotenv import load_dotenv

DATA_PATH = "data/users.json"

load_dotenv()

# Get the URI
# Module-level MongoDB connection
MONGO_URI = os.getenv("MONGO_URI")
client = MongoClient(MONGO_URI) if MONGO_URI else None
db = client["language_game"] if client is not None else None
users_collection = db["users"] if db is not None else None


class UserModel:
    # MongoDB setup
    client = MongoClient(MONGO_URI) if MONGO_URI else None
    db = client["test"] 
    users_collection = db["users"] 
    
    # After creating client and db
    if db is not None:
        print("Mongo collections:", db.list_collection_names())
    else:
        print("MongoDB not connected")




    @staticmethod
    def _load_users():
        if not os.path.exists(DATA_PATH):
            return {}
        with open(DATA_PATH, "r", encoding="utf-8") as f:
            return json.load(f)

    @staticmethod
    def _save_users(users):
        with open(DATA_PATH, "w", encoding="utf-8") as f:
            json.dump(users, f, indent=4)

    @staticmethod
    def create_user(username: str, password: str):
        pw_hash = sha256(password.encode()).hexdigest()

        # MongoDB path
        if UserModel.users_collection is not None:
            existing = UserModel.users_collection.find_one({"username": username})
            if existing:
                return None  # user exists
            result = UserModel.users_collection.insert_one({
                "username": username,
                "password_hash": pw_hash
            })
            return {"id": str(result.inserted_id), "username": username}

        # JSON fallback
        users = UserModel._load_users()
        if username in users:
            return None
        users[username] = {"password_hash": pw_hash}
        UserModel._save_users(users)
        return {"id": username, "username": username}

    @staticmethod
    def authenticate(username: str, password: str):
        pw_hash = sha256(password.encode()).hexdigest()

        # --- MongoDB path ---
        if UserModel.users_collection is not None:
            mongo_user = UserModel.users_collection.find_one({"username": username})
            if mongo_user and mongo_user.get("password_hash") == pw_hash:
                return {
                "username": mongo_user["username"]
            }
            return None

        # --- JSON fallback path ---
        users = UserModel._load_users()
        json_user = users.get(username)

        if json_user and json_user.get("password_hash") == pw_hash:
            return {
            "username": username
        }

        return None


