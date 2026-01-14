import pygame
from settings import SCREEN_WIDTH, SCREEN_HEIGHT, FPS
from save.save_manager import create_new_save, load_game, save_exists, save_game
from game.state.game_state import GameState
from scenes.main_menu import MainMenuScene

def main():
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption('Spanish Language Training')
    clock = pygame.time.Clock()

    # --- Temporary username (replace with login later) ---
    username = "test_player"

    # --- Load or create save ---
    if save_exists(username):
        save_data = load_game(username)
    else:
        save_data = create_new_save(username)
        save_game(save_data)

    # --- Create game state ---
    game_state = GameState(save_data)

    # --- Start with Main Menu ---
    current_scene = MainMenuScene(screen, game_state)

    running = True
    while running:
        clock.tick(FPS)

        # --- Event handling ---
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                save_game(game_state.to_dict())
                running = False
            else:
                current_scene.handle_event(event)

        # --- Scene update ---
        current_scene.update()

        # --- Scene transitions ---
        if current_scene.finished:
            next_scene_obj = current_scene.next_scene()
            if next_scene_obj is None:
                # Quit selected
                save_game(game_state.to_dict())
                running = False
            else:
                current_scene = next_scene_obj

        # --- Draw ---
        current_scene.draw()
        pygame.display.flip()

    pygame.quit()

if __name__ == "__main__":
    main()
