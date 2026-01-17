# scenes/mission3.py
import pygame
from settings import TEXT_COLOR, FONT_NAME, FONT_SIZE, SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_MARGIN, FRAME_WIDTH
from scenes.main_menu import MainMenuScene

class Mission3Scene:
    def __init__(self, screen, game_state):
        self.screen = screen
        self.game_state = game_state
        self.finished = False
        self._next_scene_name = None
        self.font = pygame.font.SysFont(FONT_NAME, FONT_SIZE)
        self.text = ["Misión 3 (en construcción)"]

    def handle_event(self, event):
        if event.type == pygame.KEYDOWN:
            self.finished = True
            self._next_scene_name = "MAIN_MENU"

    def update(self):
        pass

    def draw(self):
        self.screen.fill((0, 0, 0))
        for i, line in enumerate(self.text):
            rendered = self.font.render(line, True, TEXT_COLOR)
            rect = rendered.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + i * 40))
            self.screen.blit(rendered, rect)

    def next_scene(self):
        if self._next_scene_name == "MAIN_MENU":
            return MainMenuScene(self.screen, self.game_state)
        return None
