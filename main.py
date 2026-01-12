import pygame
from settings import SCREEN_WIDTH, SCREEN_HEIGHT, FPS
from scenes.intro_scene import IntroScene
from scenes.mission1 import Mission1Scene
from save.save_manager import create_new_save, load_game, save_exists, save_game
from game.state.game_state import GameState


def main():
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption('Spanish Language Training')    
    clock = pygame.time.Clock()
    
    username = "test_player"  # temporary (Step 3 = login scene)
    if save_exists(username):
        save_data = load_game(username)
    else:
        save_data = create_new_save(username)
        save_game(save_data)

    game_state = GameState(save_data)
    
    # Start with IntroScene        
    scene = IntroScene(screen, game_state)
    
    running  = True
    while running:
        clock.tick(FPS)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            else:
                scene.handle_event(event)
                
        scene.update()       
        scene.draw()
        pygame.display.flip()
        
        if hasattr(scene, 'finished') and scene.finished:
            if isinstance(scene, IntroScene):
                scene = Mission1Scene(screen, game_state)
            else:
                # Future scenes here
                running = False # Exit after last scene
            # Save at end
            save_game(game_state.to_dict())
 
        
    pygame.quit()
if __name__ == '__main__':
    main()
    