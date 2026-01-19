# models/mongo_progress_model.py

from pymongo import MongoClient
from datetime import datetime
import uuid

class ProgressModelMongo:
    def __init__(self, uri="mongodb://localhost:27017", db_name="language_game"):
        self.client = MongoClient(uri)
        self.db = self.client[db_name]
        self.collection = self.db["user_progress"]

    def create_user(self, username):
        user_id = str(uuid.uuid4())
        doc = {
            "_id": user_id,
            "username": username,
            "current_mission": 1,
            "missions_completed": {},
            "last_updated": datetime.utcnow()
        }
        self.collection.insert_one(doc)
        return user_id

    def get_user(self, user_id):
        return self.collection.find_one({"_id": user_id})

    def update_progress(self, user_id, current_mission=None, missions_completed=None):
        update_doc = {}
        if current_mission is not None:
            update_doc["current_mission"] = current_mission
        if missions_completed is not None:
            update_doc["missions_completed"] = missions_completed
        update_doc["last_updated"] = datetime.utcnow()

        self.collection.update_one({"_id": user_id}, {"$set": update_doc})

    def delete_user(self, user_id):
        self.collection.delete_one({"_id": user_id})

    def list_users(self):
        return list(self.collection.find({}, {"_id": 1, "username": 1, "current_mission": 1}))
