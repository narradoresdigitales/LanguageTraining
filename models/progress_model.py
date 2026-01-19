"""
progress_model.py
Handles gameplay progress using a local JSON fallback.
"""

import json
import os

DATA_PATH = "data/progress.json"


class ProgressModel:
    @staticmethod
    def _load_progress():
        if not os.path.exists(DATA_PATH):
            return {}
        with open(DATA_PATH, "r", encoding="utf-8") as f:
            return json.load(f)

    @staticmethod
    def _save_progress(progress):
        with open(DATA_PATH, "w", encoding="utf-8") as f:
            json.dump(progress, f, indent=4)

    @staticmethod
    def create_progress(user_id: str):
        progress = ProgressModel._load_progress()

        if user_id not in progress:
            progress[user_id] = {
                "current_mission": 1,
                "missions_completed": []
            }

        ProgressModel._save_progress(progress)
        return progress[user_id]

    @staticmethod
    def load_progress(user_id: str):
        progress = ProgressModel._load_progress()
        return progress.get(user_id)

    @staticmethod
    def update_mission(user_id: str, mission_id: int):
        progress = ProgressModel._load_progress()

        if user_id not in progress:
            ProgressModel.create_progress(user_id)

        if mission_id not in progress[user_id]["missions_completed"]:
            progress[user_id]["missions_completed"].append(mission_id)

        progress[user_id]["current_mission"] = mission_id + 1
        ProgressModel._save_progress(progress)

    @staticmethod
    def delete_progress(user_id: str):
        progress = ProgressModel._load_progress()

        if user_id in progress:
            del progress[user_id]
            ProgressModel._save_progress(progress)
            return True

        return False
