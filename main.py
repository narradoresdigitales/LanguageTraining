import pygame
from settings import SCREEN_WIDTH, SCREEN_HEIGHT, FPS
from scenes.character_creation import CharacterCreationScene
from save.save_manager import save_game
from game.state.game_state import GameState
import os

def main():
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Spanish Language Training")
    clock = pygame.time.Clock()

    # --- Load and play background music ---
    music_path = os.path.join('assets', 'audio', 'retro_game.wav')
    if os.path.exists(music_path):
        pygame.mixer.music.load(music_path)
        pygame.mixer.music.set_volume(0.25)  # Adjust volume (0.0 to 1.0)
        pygame.mixer.music.play(-1)  # Loop indefinitely
    
    
    
    
    
    # Start with empty game state; CharacterCreationScene will populate it
    game_state = GameState({})

    # Start with character creation
    scene = CharacterCreationScene(screen, game_state)

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
                    # No next scene returned, quit
                    save_game(game_state.to_dict())
                    running = False

        # Draw current scene
        scene.draw()
        pygame.display.flip()

    pygame.quit()

if __name__ == "__main__":
    main()
