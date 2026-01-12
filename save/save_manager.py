# save/save_manager.py
import json
import os
from datetime import datetime, timezone

GAME_VERSION = "0.2"
SAVE_DIR = 'saves'

def create_new_save(username):
    return {
        "username": username,
        "current_mission": "mission_1",
        "missions_completed": {},
        "last_updated": datetime.now(timezone.utc).isoformat(),
        "game_version": GAME_VERSION
    }

def save_game(save_data):
    if not os.path.exists(SAVE_DIR):
        os.makedirs(SAVE_DIR)

    save_data["last_updated"] = datetime.now(timezone.utc).isoformat()

    filepath = os.path.join(SAVE_DIR, f"{save_data['username']}.json")
    with open(filepath, "w", encoding="utf-8") as f:
        json.dump(save_data, f, indent=4)


def save_exists(username):
    return os.path.exists(os.path.join(SAVE_DIR, f"{username}.json"))

    
def load_game(username):
    filepath = os.path.join(SAVE_DIR, f"{username}.json")
    if not os.path.exists(filepath):
        return None

    with open(filepath, "r", encoding="utf-8") as f:
        return json.load(f)