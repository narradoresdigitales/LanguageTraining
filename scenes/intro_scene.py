import pygame
from settings import WHITE, BLACK, FONT_NAME, FONT_SIZE

class IntroScene: 
    def __init__(self, screen):
        self.screen = screen
        self.font = pygame.font.SysFont(FONT_NAME, FONT_SIZE)
        self.finished = False
        
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
        self.screen.fill(WHITE)
        y = 50
        for line in self.text:
            rendered = self.font.render(line, True, BLACK)
            self.screen.blit(rendered, (50, y))
            y += 35