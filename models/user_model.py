"""
user_model.py
Handles user-related data operations using a local JSON fallback.
"""

import json
import os
import uuid

DATA_PATH = "data/users.json"


class UserModel:
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
        users = UserModel._load_users()

        if username in users:
            return None  # user already exists

        user_id = str(uuid.uuid4())
        users[username] = {
            "id": user_id,
            "password": password
        }

        UserModel._save_users(users)
        return users[username]

    @staticmethod
    def authenticate(username: str, password: str):
        users = UserModel._load_users()

        if username not in users:
            return None

        if users[username]["password"] != password:
            return None

        return users[username]

    @staticmethod
    def delete_user(username: str):
        users = UserModel._load_users()

        if username in users:
            del users[username]
            UserModel._save_users(users)
            return True

        return False
