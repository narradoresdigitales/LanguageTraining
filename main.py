import pygame
from settings import SCREEN_WIDTH, SCREEN_HEIGHT, FPS
from scenes.character_creation import CharacterCreationScene
from save.save_manager import save_game
from game.state.game_state import GameState

def main():
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Spanish Language Training")
    clock = pygame.time.Clock()

    # --- Start game state with defaults if empty ---
    initial_save = {
        "username": "Player1",
        "current_mission": None,
        "missions_completed": {},
        "last_updated": None,
        "game_version": "0.1"
    }
    game_state = GameState(initial_save)

    # --- Start with character creation ---
    scene = CharacterCreationScene(screen, game_state)

    running = True
    while running:
        clock.tick(FPS)

        # --- Event handling ---
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                save_game(game_state.to_dict())
                running = False
            else:
                scene.handle_event(event)

        # --- Update scene ---
        scene.update()

        # --- Handle scene transitions ---
        if scene.finished:
            if hasattr(scene, "next_scene") and callable(scene.next_scene):
                next_scene_obj = scene.next_scene()
                if next_scene_obj:
                    scene = next_scene_obj
                else:
                    running = False
            else:
                running = False

        # --- Draw scene ---
        scene.draw()
        pygame.display.flip()

    pygame.quit()


if __name__ == "__main__":
    main()
