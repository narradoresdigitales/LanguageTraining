import pygame

from settings import WHITE, BLACK, FONT_NAME, FONT_SIZE

class Mission1Scene:
    def __init__(self, screen):
        self.screen = screen
        self.font = pygame.font.SysFont(FONT_NAME, FONT_SIZE)
        
    def handle_event(self, event):
        pass
    
    def update(self):
        pass
    
    def draw(self):
        self.screen.fill(WHITE)
        text = self.font.render('Mission 1: Interview in Progress ...', True, BLACK)
        self.screen.blit(text,(50, 50))