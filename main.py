import pygame
import os
from settings import SCREEN_WIDTH, SCREEN_HEIGHT, FPS
from scenes.character_creation import CharacterCreationScene
from save.save_manager import save_game
from game.state.game_state import GameState
from models.progress_model import ProgressModel
from models.user_model import UserModel

def main():
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Spanish Language Training")
    clock = pygame.time.Clock()

    # --- Load and play background music ---
    music_path = os.path.join('assets', 'audio', 'retro_game.wav')
    if os.path.exists(music_path):
        pygame.mixer.music.load(music_path)
        pygame.mixer.music.set_volume(0.25)
        pygame.mixer.music.play(-1)

    # ---------------------------
    # Game state
    # ---------------------------
    game_state = GameState({})

    # Start with character creation
    scene = CharacterCreationScene(screen, game_state)

    # ---------------------------
    # USER AUTHENTICATION
    # ---------------------------
    # Wait for username/password input from CharacterCreationScene
    while scene and not scene.finished:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                save_game(game_state.to_dict())
                pygame.quit()
                return
            scene.handle_event(event)
        scene.update()
        scene.draw()
        pygame.display.flip()

    # After character creation
    username = game_state.username
    password = getattr(game_state, "password", "")  # password optional

    # Create or get user in MongoDB
    user = UserModel.create_or_get_user(username, password)
    print(f"User logged in: {user}")

    game_state.user_id = user["username"]

    # Load progress
    saved_progress = ProgressModel.load_progress(game_state.user_id)

    if saved_progress:
        game_state.current_mission = saved_progress.get("current_mission", 1)

        missions = saved_progress.get("missions_completed", [])

        # 🔑 Normalize old dict-based progress to list
        if isinstance(missions, dict):
            game_state.missions_completed = [
                int(k.split("_")[1])
                for k, v in missions.items()
                if v == "completed"
        ]
        else:
            game_state.missions_completed = missions
    else:
        game_state.missions_completed = []
        ProgressModel.create_progress(game_state.user_id)


    # ---------------------------
    # Main game loop
    # ---------------------------
    running = True
    while running:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                save_game(game_state.to_dict())
                running = False
            else:
                scene.handle_event(event)

        scene.update()

        if scene.finished and hasattr(scene, "next_scene"):
            next_scene_obj = scene.next_scene()
            if next_scene_obj:
                scene = next_scene_obj
            else:
                save_game(game_state.to_dict())
                running = False

        scene.draw()
        pygame.display.flip()

    pygame.quit()

if __name__ == "__main__":
    main()
