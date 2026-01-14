# scenes/character_creation.py
import pygame
import json
from settings import SCREEN_WIDTH, SCREEN_HEIGHT, TEXT_COLOR, FONT_NAME, FONT_SIZE, LINE_SPACING
from save.save_manager import save_game

class CharacterCreationScene:
    def __init__(self, screen, game_state):
        self.screen = screen
        self.game_state = game_state
        self.font = pygame.font.SysFont(FONT_NAME, FONT_SIZE)
        self.finished = False
        self.next_scene_obj = None  # This will hold the next scene
        self.step = 0  # 0 = enter username, 1 = enter password
        self.input_text = ""
        self.username = ""
        self.password = ""
        self.message = "Enter a username:"

    def handle_event(self, event):
        if event.type != pygame.KEYDOWN:
            return

        if event.key == pygame.K_BACKSPACE:
            self.input_text = self.input_text[:-1]
        elif event.key == pygame.K_RETURN:
            if self.step == 0:
                self.username = self.input_text.strip()
                self.input_text = ""
                self.step = 1
                self.message = "Enter a password:"
            elif self.step == 1:
                self.password = self.input_text.strip()
                self.input_text = ""
                self.finished = True
                # Save character data
                self.game_state.username = self.username
                save_data = {
                    "username": self.username,
                    "password": self.password,
                    "current_mission": None,
                    "missions_completed": {},
                    "last_updated": "",
                    "game_version": "0.1"
                }
                save_game(save_data)
        elif event.unicode.isprintable():
            self.input_text += event.unicode

    def update(self):
        pass

    def draw(self):
        self.screen.fill((0, 0, 0))
        y = 200
        rendered = self.font.render(self.message, True, TEXT_COLOR)
        rect = rendered.get_rect(centerx=SCREEN_WIDTH//2, y=y)
        self.screen.blit(rendered, rect)

        y += 50
        rendered = self.font.render(self.input_text, True, TEXT_COLOR)
        rect = rendered.get_rect(centerx=SCREEN_WIDTH//2, y=y)
        self.screen.blit(rendered, rect)

    def next_scene(self):
        """Return the next scene after character creation, e.g., MainMenuScene."""
        from scenes.main_menu import MainMenuScene
        return MainMenuScene(self.screen, self.game_state)
