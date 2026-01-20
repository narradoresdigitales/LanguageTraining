# scenes/character_creation.py
import pygame
from settings import SCREEN_WIDTH, SCREEN_HEIGHT, TEXT_COLOR, FONT_NAME, FONT_SIZE, LINE_SPACING
from save.save_manager import save_game, create_new_save

class CharacterCreationScene:
    def __init__(self, screen, game_state):
        self.screen = screen
        self.game_state = game_state
        self.font = pygame.font.SysFont(FONT_NAME, FONT_SIZE)
        self.finished = False
        self.next_scene_obj = None

        # Input
        self.username = ""
        self.password = ""
        self.input_mode = "username"  # "username" or "password"
        self.message = "Enter your username:"

    def handle_event(self, event):
        if event.type != pygame.KEYDOWN:
            return

        if event.key == pygame.K_BACKSPACE:
            if self.input_mode == "username":
                self.username = self.username[:-1]
            else:
                self.password = self.password[:-1]

        elif event.key == pygame.K_RETURN:
            if self.input_mode == "username":
                if self.username.strip() == "":
                    self.message = "Username cannot be empty!"
                else:
                    self.input_mode = "password"
                    self.message = "Enter your password:"
            else:
                # User finished entering username/password
                self._create_player()
                self.finished = True

        elif event.unicode.isprintable():
            if self.input_mode == "username":
                self.username += event.unicode
            else:
                self.password += event.unicode

    def _create_player(self):
        """
        Save player locally (fallback) and set credentials in game_state.
        The MongoDB authentication in main.py will handle actual user creation/login.
        """
        # Create a local save for fallback and progress
        save_data = create_new_save(self.username)
        save_game(save_data)

        # Store credentials in game_state for main.py to authenticate
        self.game_state.username = self.username
        self.game_state.password = self.password
        self.game_state.current_mission = save_data["current_mission"]
        self.game_state.missions_completed = save_data["missions_completed"]
        self.game_state.game_version = save_data["game_version"]

        # Next scene is MainMenuScene
        from scenes.main_menu import MainMenuScene
        self.next_scene_obj = MainMenuScene(self.screen, self.game_state)

    def update(self):
        pass

    def draw(self):
        self.screen.fill((0, 0, 0))
        y = 150

        # Show message
        rendered = self.font.render(self.message, True, TEXT_COLOR)
        self.screen.blit(rendered, (SCREEN_WIDTH // 2 - rendered.get_width() // 2, y))
        y += 50

        # Show input (mask password)
        current_input = self.username if self.input_mode == "username" else "*" * len(self.password)
        rendered = self.font.render(current_input, True, TEXT_COLOR)
        self.screen.blit(rendered, (SCREEN_WIDTH // 2 - rendered.get_width() // 2, y))

    def next_scene(self):
        return self.next_scene_obj
