import pygame
import os 
from settings import TEXT_COLOR, FONT_NAME, FONT_SIZE, SCREEN_WIDTH, SCREEN_HEIGHT,SCREEN_MARGIN, FRAME_WIDTH

class IntroScene: 
    def __init__(self, screen):
        self.screen = screen 
        self.screen_rect = pygame.Rect(
            SCREEN_MARGIN,
            SCREEN_MARGIN,
            self.screen.get_width() - SCREEN_MARGIN * 2,
            self.screen.get_height() - SCREEN_MARGIN * 2
        )
        
        self.font = pygame.font.SysFont(FONT_NAME, FONT_SIZE)
        self.finished = False
        
        # Load and scale background image
        bg_path = os.path.join('assets', 'images', 'briefing room.png')  
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
        self.screen.fill((0,0,0))
        pygame.draw.rect(self.screen, TEXT_COLOR, self.screen_rect, FRAME_WIDTH)
        
        # Draw text on top
        y = 185
        for line in self.text:
            rendered = self.font.render(line, True, TEXT_COLOR)
            text_rect = rendered.get_rect(centerx=self.screen.get_width() //2)
            text_rect.y = y
            self.screen.blit(rendered, text_rect)
            y += 35