# scenes/mission2.py
import pygame
from settings import TEXT_COLOR, FONT_NAME, FONT_SIZE, SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_MARGIN, FRAME_WIDTH
from save.save_manager import save_game

class Mission2Scene:
    def __init__(self, screen, game_state):
        self.screen = screen
        self.game_state = game_state
        self.finished = False
        self._next_scene_name = None
        self.font = pygame.font.SysFont(FONT_NAME, FONT_SIZE)

        self.screen_rect = pygame.Rect(
            SCREEN_MARGIN,
            SCREEN_MARGIN,
            SCREEN_WIDTH - SCREEN_MARGIN * 2,
            SCREEN_HEIGHT - SCREEN_MARGIN * 2
        )

        # Temporary text for now
        self.text = [
            "== MISION 2 ==",
            "",
            "Bienvenido a la segunda misión.",
            "Pronto tendrás tus instrucciones.",
            "",
            "Presiona cualquier tecla para continuar..."
        ]

    def handle_event(self, event):
        if event.type == pygame.KEYDOWN:
            self.finished = True
            self._next_scene_name = "MAIN_MENU"  # For now, go back to main menu

    def update(self):
        pass

    def draw(self):
        self.screen.fill((0, 0, 0))
        pygame.draw.rect(self.screen, TEXT_COLOR, self.screen_rect, FRAME_WIDTH)

        y = 100
        for line in self.text:
            rendered = self.font.render(line, True, TEXT_COLOR)
            rect = rendered.get_rect(centerx=SCREEN_WIDTH // 2)
            rect.y = y
            self.screen.blit(rendered, rect)
            y += 35

    def next_scene(self):
        if self._next_scene_name == "MAIN_MENU":
            from scenes.main_menu import MainMenuScene
            return MainMenuScene(self.screen, self.game_state)
        return None
