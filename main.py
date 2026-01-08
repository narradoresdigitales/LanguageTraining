import pygame
from settings import SCREEN_WIDTH, SCREEN_HEIGHT, FPS
from scenes.intro_scene import IntroScene
from scenes.mission1 import Mission1Scene

def main():
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption('Spanish Language Training')
    
    clock = pygame.time.Clock()
        
    scene = IntroScene(screen)
    
    running  = True
    while running:
        clock.tick(FPS)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            else:
                scene.handle_event(event)
                
        scene.update()       
        
        if hasattr(scene, 'finished') and scene.finished:
            scene = Mission1Scene(screen)
    
        scene.draw()
        
        pygame.display.flip()
        
    pygame.quit()
if __name__ == '__main__':
    main()
    