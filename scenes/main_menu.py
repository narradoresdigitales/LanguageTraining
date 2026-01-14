# scenes/main_menu.py
import pygame
from settings import SCREEN_WIDTH, SCREEN_HEIGHT, TEXT_COLOR, FONT_NAME, FONT_SIZE, LINE_SPACING

class MainMenuScene:
    def __init__(self, screen, game_state):
        self.screen = screen
        self.game_state = game_state
        self.font = pygame.font.SysFont(FONT_NAME, FONT_SIZE)
        self.finished = False
        self.next_scene_obj = None

        # Menu options and mapping to scenes
        self.options = [
            "Start Mission 1",
            "Replay Mission 1",
            "Quit"
        ]
        self.option_to_scene = {
            "Start Mission 1": "INTRO",
            "Replay Mission 1": "MISSION1"
        }

        self.selected_index = 0

    def handle_event(self, event):
        if event.type != pygame.KEYDOWN:
            return

        if event.key == pygame.K_DOWN:
            self.selected_index = (self.selected_index + 1) % len(self.options)
        elif event.key == pygame.K_UP:
            self.selected_index = (self.selected_index - 1) % len(self.options)
        elif event.key == pygame.K_RETURN:
            self._activate_selection()
        elif event.key == pygame.K_1:
            self.selected_index = 0
            self._activate_selection()
        elif event.key == pygame.K_2:
            self.selected_index = 1
            self._activate_selection()
        elif event.key == pygame.K_q:
            self.finished = True

    def _activate_selection(self):
        choice = self.options[self.selected_index]
        if choice == "Quit":
            self.finished = True
        else:
            # Dynamically import scene to avoid circular imports
            if self.option_to_scene[choice] == "INTRO":
                from scenes.intro_scene import IntroScene
                self.next_scene_obj = IntroScene(self.screen, self.game_state)
            elif self.option_to_scene[choice] == "MISSION1":
                from scenes.mission1 import Mission1Scene
                self.next_scene_obj = Mission1Scene(self.screen, self.game_state)
            self.finished = True

    def update(self):
        pass

    def draw(self):
        self.screen.fill((0, 0, 0))
        y = 120

        # Player info
        info = f"Player: {self.game_state.username}"
        self._draw_centered(info, y)
        y += 40

        completed = ", ".join(self.game_state.missions_completed.keys()) or "None"
        self._draw_centered(f"Missions Completed: {completed}", y)
        y += 80

        # Menu options
        for i, option in enumerate(self.options):
            color = (255, 255, 0) if i == self.selected_index else TEXT_COLOR
            self._draw_centered(option, y, color)
            y += FONT_SIZE + LINE_SPACING

        # Hint
        y += 30
        self._draw_centered("Use ↑ ↓ or 1–2, ENTER to select, Q to quit", y, (150, 150, 150))

    def _draw_centered(self, text, y, color=TEXT_COLOR):
        rendered = self.font.render(text, True, color)
        rect = rendered.get_rect(centerx=SCREEN_WIDTH // 2, y=y)
        self.screen.blit(rendered, rect)

    def next_scene(self):
        return self.next_scene_obj
