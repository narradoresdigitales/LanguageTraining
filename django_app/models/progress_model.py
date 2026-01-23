import os
import json
from pymongo import MongoClient
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
MONGO_URI = os.getenv("MONGO_URI", "")
if not MONGO_URI:
    raise RuntimeError("MONGO_URI is not set in environment variables")

# Connect to MongoDB
client = MongoClient(MONGO_URI)
db = client["language_game"]
PROGRESS_COLLECTION = db["progress"]

# Path to JSON fallback
DATA_DIR = os.path.join(os.path.dirname(__file__), "..", "data")
if not os.path.exists(DATA_DIR):
    os.makedirs(DATA_DIR)
JSON_PATH = os.path.join(DATA_DIR, "progress.json")


class ProgressModel:
    @staticmethod
    def _load_json():
        if not os.path.exists(JSON_PATH):
            return {}
        with open(JSON_PATH, "r", encoding="utf-8") as f:
            return json.load(f)

    @staticmethod
    def _save_json(progress):
        with open(JSON_PATH, "w", encoding="utf-8") as f:
            json.dump(progress, f, indent=4)

    @staticmethod
    def create_progress(user_id: str):
        """Create a new progress entry if none exists."""
        # MongoDB
        if not PROGRESS_COLLECTION.find_one({"user_id": user_id}):
            PROGRESS_COLLECTION.insert_one({
                "user_id": user_id,
                "current_mission": 1,
                "missions_completed": []
            })

        # JSON fallback
        progress = ProgressModel._load_json()
        if user_id not in progress:
            progress[user_id] = {"current_mission": 1, "missions_completed": []}
            ProgressModel._save_json(progress)

        return ProgressModel.load_progress(user_id)

    @staticmethod
    def load_progress(user_id: str):
        """Load progress from MongoDB or JSON fallback."""
        record = PROGRESS_COLLECTION.find_one({"user_id": user_id})
        if record:
            return record
        # fallback to JSON
        progress = ProgressModel._load_json()
        return progress.get(user_id)

    @staticmethod
    def update_mission(user_id: str, mission_id: int):
        """Mark a mission as completed."""
        # MongoDB
        PROGRESS_COLLECTION.update_one(
            {"user_id": user_id},
            {
                "$set": {"current_mission": mission_id + 1},
                "$addToSet": {"missions_completed": mission_id}
            },
            upsert=True
        )

        # JSON fallback
        progress = ProgressModel._load_json()
        if user_id not in progress:
            progress[user_id] = {"current_mission": 1, "missions_completed": []}
        if mission_id not in progress[user_id]["missions_completed"]:
            progress[user_id]["missions_completed"].append(mission_id)
        progress[user_id]["current_mission"] = mission_id + 1
        ProgressModel._save_json(progress)

    @staticmethod
    def delete_progress(user_id: str):
        """Delete progress for a user."""
        # MongoDB
        PROGRESS_COLLECTION.delete_one({"user_id": user_id})
        # JSON fallback
        progress = ProgressModel._load_json()
        if user_id in progress:
            del progress[user_id]
            ProgressModel._save_json(progress)
