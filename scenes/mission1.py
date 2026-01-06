import pygame
from settings import WHITE, BLACK, FONT_NAME, FONT_SIZE

class Mission1Scene:
    def __init__(self, screen):
        self.screen = screen
        self.font = pygame.font.SysFont(FONT_NAME, FONT_SIZE)
        self.input_text = ''
        
    def handle_event(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_BACKSPACE:
                self.input_text = self.input_text[:-1]
            elif event.key == pygame.K_RETURN:
                print('Player submitted:', self.input_text)
                self.input_text = '' 
            else:
                self.input_text += event.unicode
    
    def update(self):
        pass
    
    def draw(self):
        self.screen.fill(WHITE)
        
        #Mission text
        text = self.font.render('Mission 1: Interview in Progress ...', True, BLACK)
        self.screen.blit(text,(50, 50))
        
        # Input prompt
        prompt = self.font.render('Your Response: ' + self.input_text, True, BLACK)
        self.screen.blit(prompt, (50, 150))