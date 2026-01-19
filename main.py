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
    # USER AUTHENTICATION
    # ---------------------------
    USERNAME = "player1"
    PASSWORD = "password"

    # Create user if it does not exist
    created_user = UserModel.create_user(USERNAME, PASSWORD)
    if created_user:
        print(f"Created new user: {USERNAME}")
    else:
        print(f"User {USERNAME} already exists, logging in.")

    # Authenticate user
    user = UserModel.authenticate(USERNAME, PASSWORD)
    if user is None:
        raise ValueError(
            "Authentication failed: check username/password or database connection."
        )

    # ---------------------------
    # GAME STATE INITIALIZATION
    # ---------------------------
    game_state = GameState({})
    game_state.user_id = user["username"]

    # Load or create progress
    saved_progress = ProgressModel.load_progress(game_state.user_id)

    if saved_progress:
        game_state.current_mission = saved_progress["current_mission"]
        game_state.missions_completed = saved_progress["missions_completed"]
    else:
        ProgressModel.create_progress(game_state.user_id)

    # ---------------------------
    # START FIRST SCENE
    # ---------------------------
    scene = CharacterCreationScene(screen, game_state)

    # ---------------------------
    # MAIN GAME LOOP
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

        # Scene transition
        if scene.finished:
            if hasattr(scene, "next_scene") and callable(scene.next_scene):
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
