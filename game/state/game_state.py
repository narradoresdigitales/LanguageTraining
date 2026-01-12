# game/state/game_state.py

class GameState:
    def __init__(self, save_data):
        self.username = save_data["username"]
        self.current_mission = save_data["current_mission"]
        self.missions_completed = save_data["missions_completed"]
        self.last_updated = save_data["last_updated"]
        self.game_version = save_data["game_version"]

    def to_dict(self):
        return {
            "username": self.username,
            "current_mission": self.current_mission,
            "missions_completed": self.missions_completed,
            "game_version": self.game_version
        }
    
    
    def complete_mission(self, mission_id, result):
        self.missions_completed[mission_id] = result
        self.current_mission = mission_id
