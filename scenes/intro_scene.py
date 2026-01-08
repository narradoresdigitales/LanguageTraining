import pygame
import os 
from settings import WHITE, BLACK, FONT_NAME, FONT_SIZE, SCREEN_WIDTH, SCREEN_HEIGHT

class IntroScene: 
    def __init__(self, screen):
        self.screen = screen
        self.font = pygame.font.SysFont(FONT_NAME, FONT_SIZE)
        self.finished = False
        
        # Load and scale background image
        bg_path = os.path.join('assets', 'images', 'briefing room.png')  # Update path if needed
        self.background = pygame.image.load(bg_path).convert()  # Use convert_alpha() if image has transparency
        self.background = pygame.transform.scale(self.background, (SCREEN_WIDTH, SCREEN_HEIGHT))
        
        self.text = [
            'Mission 1: Initial Contact', 
            '',
            'You are conducting a field interview',
            'Your objective is to gather information',
            'using appropriate Spanish register.',
            '',
            'Press any key to begin.'
        ]
        
    def handle_event(self, event):
        if event.type == pygame.KEYDOWN:
            self.finished = True
            
    def update(self):
        pass
    
    def draw(self):
        self.screen.blit(self.background, (0, 0))
        
        # Draw text on top
        y = 50
        for line in self.text:
            rendered = self.font.render(line, True, BLACK)
            self.screen.blit(rendered, (50, y))
            y += 35