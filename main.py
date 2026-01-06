import pygame
from settings import SCREEN_WIDTH, SCREEN_HEIGHT, FPS, WHITE, BLACK, FONT_NAME, FONT_SIZE

def main():
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption('Spanish Language Training')
    
    clock = pygame.time.Clock()
    font = pygame.font.SysFont(FONT_NAME, FONT_SIZE)
    
    briefing_text = [
        "Mission 1: Initial Contact",
        "",
        "You are conducting a field interview.",
        "Your objective is to gather information",
        "using appropriate Spanish register.",
        "",
        "Press any key to begin."
    ]
    
    
    
    running  = True
    while running:
        clock.tick(FPS)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                running = False
                
        screen.fill(WHITE)
        
        y = 50
        for line in briefing_text:
            rendered = font.render(line, True, BLACK)
            screen.blit(rendered, (50, y))
            y += 35
        
       
        
        pygame.display.flip()
        
    pygame.quit()
if __name__ == '__main__':
    main()
    