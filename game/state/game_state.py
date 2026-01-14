# game/state/game_state.py

class GameState:
    def __init__(self, save_data):
        # Use .get() to provide defaults for new players
        self.username = save_data.get("username", "")
        self.current_mission = save_data.get("current_mission", None)
        self.missions_completed = save_data.get("missions_completed", {})
        self.last_updated = save_data.get("last_updated", "")
        self.game_version = save_data.get("game_version", "0.1")  # default version

    def to_dict(self):
        return {
            "username": self.username,
            "current_mission": self.current_mission,
            "missions_completed": self.missions_completed,
            "last_updated": self.last_updated,
            "game_version": self.game_version
        }

    def complete_mission(self, mission_id, result):
        self.missions_completed[mission_id] = result
        self.current_mission = mission_id
