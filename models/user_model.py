import os
import json
from hashlib import sha256
from pymongo import MongoClient
from bson.objectid import ObjectId

DATA_PATH = "data/users.json"


class UserModel:
    # MongoDB setup
    MONGO_URI = "mongodb+srv://narradoresdigitales_db_user:Mimate9346@cluster0.2lla5ju.mongodb.net/language_game?retryWrites=true&w=majority"
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


