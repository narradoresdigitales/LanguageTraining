# models/progress_model.py
from .db import db
import json
import os

JSON_PATH = "data/progress.json"
PROGRESS_COLLECTION = db.progress if db is not None else None


class ProgressModel:
    # ---------------------------
    # JSON FALLBACK HELPERS
    # ---------------------------
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

    # ---------------------------
    # CREATE
    # ---------------------------
    @staticmethod
    def create_progress(user_id: str):
        # MongoDB
        if PROGRESS_COLLECTION is not None:
            if not PROGRESS_COLLECTION.find_one({"user_id": user_id}):
                PROGRESS_COLLECTION.insert_one({
                    "user_id": user_id,
                    "current_mission": 1,
                    "missions_completed": []
                })

        # JSON fallback
        progress = ProgressModel._load_json()
        if user_id not in progress:
            progress[user_id] = {
                "current_mission": 1,
                "missions_completed": []
            }
            ProgressModel._save_json(progress)

        return ProgressModel.load_progress(user_id)

    # ---------------------------
    # READ
    # ---------------------------
    @staticmethod
    def load_progress(user_id: str):
        if PROGRESS_COLLECTION is not None:
            record = PROGRESS_COLLECTION.find_one({"user_id": user_id})
            if record:
                record.pop("_id", None)  # clean Mongo internals
                return record

        # JSON fallback
        progress = ProgressModel._load_json()
        return progress.get(user_id)

    # ---------------------------
    # UPDATE
    # ---------------------------
    @staticmethod
    def update_mission(user_id: str, mission_id: int):
        # MongoDB
        if PROGRESS_COLLECTION is not None:
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
            progress[user_id] = {
                "current_mission": 1,
                "missions_completed": []
            }

        if mission_id not in progress[user_id]["missions_completed"]:
            progress[user_id]["missions_completed"].append(mission_id)

        progress[user_id]["current_mission"] = mission_id + 1
        ProgressModel._save_json(progress)

    # ---------------------------
    # DELETE
    # ---------------------------
    @staticmethod
    def delete_progress(user_id: str) -> bool:
        deleted = False

        # MongoDB
        if PROGRESS_COLLECTION is not None:
            result = PROGRESS_COLLECTION.delete_one({"user_id": user_id})
            if result.deleted_count > 0:
                deleted = True

        # JSON fallback
        progress = ProgressModel._load_json()
        if user_id in progress:
            del progress[user_id]
            ProgressModel._save_json(progress)
            deleted = True

        return deleted
