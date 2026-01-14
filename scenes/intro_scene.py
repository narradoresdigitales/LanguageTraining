import pygame
import os
from settings import TEXT_COLOR, FONT_NAME, FONT_SIZE, SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_MARGIN, FRAME_WIDTH

class IntroScene:
    def __init__(self, screen, game_state):
        self.screen = screen
        self.game_state = game_state
        self.finished = False
        self.font = pygame.font.SysFont(FONT_NAME, FONT_SIZE)
        self.screen_rect = pygame.Rect(SCREEN_MARGIN, SCREEN_MARGIN,
                                       SCREEN_WIDTH - SCREEN_MARGIN * 2,
                                       SCREEN_HEIGHT - SCREEN_MARGIN * 2)
        bg_path = os.path.join('assets', 'images', 'briefing room.png')
        self.background = pygame.image.load(bg_path).convert()
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
        pygame.draw.rect(self.screen, TEXT_COLOR, self.screen_rect, FRAME_WIDTH)
        y = 185
        for line in self.text:
            rendered = self.font.render(line, True, TEXT_COLOR)
            rect = rendered.get_rect(centerx=SCREEN_WIDTH // 2, y=y)
            self.screen.blit(rendered, rect)
            y += 35

    def next_scene(self):
        from scenes.mission1 import Mission1Scene
        return Mission1Scene(self.screen, self.game_state)
