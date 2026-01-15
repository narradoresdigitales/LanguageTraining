import pygame
from settings import (
    TEXT_COLOR,
    FONT_NAME,
    FONT_SIZE,
    SCREEN_WIDTH,
    SCREEN_HEIGHT,
    SCREEN_MARGIN,
    FRAME_WIDTH,
)

class MissionOfferScene:
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

        self.text = [
            "== MENSAJE PRIORITARIO ==",
            "",
            "ORIGEN: COMANDO LINGÜÍSTICO",
            "",
            "Su desempeño en la misión anterior",
            "ha sido evaluado.",
            "",
            "RESULTADO: SATISFACTORIO",
            "",
            "Tenemos una segunda misión disponible.",
            "",
            "Nivel de riesgo: MODERADO",
            "Importancia estratégica: ALTA",
            "",
            "¿Acepta participar en la Misión 2?",
            "",
            "[A] ACEPTAR    [D] RECHAZAR"
        ]

    # ---------------------------
    # INPUT
    # ---------------------------
    def handle_event(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_a:
                self.finished = True
                self._next_scene_name = "MISSION2"
            elif event.key == pygame.K_d:
                self.finished = True
                self._next_scene_name = "MAIN_MENU"

    def update(self):
        pass

    # ---------------------------
    # DRAW
    # ---------------------------
    def draw(self):
        self.screen.fill((0, 0, 0))
        pygame.draw.rect(self.screen, TEXT_COLOR, self.screen_rect, FRAME_WIDTH)

        y = self.screen_rect.top + 30
        for line in self.text:
            rendered = self.font.render(line, True, TEXT_COLOR)
            rect = rendered.get_rect(centerx=SCREEN_WIDTH // 2, y=y)
            self.screen.blit(rendered, rect)
            y += FONT_SIZE + 8

    # ---------------------------
    # SCENE TRANSITION
    # ---------------------------
    def next_scene(self):
        if self._next_scene_name == "MISSION2":
            from scenes.mission2 import Mission2Scene  # create later
            return Mission2Scene(self.screen, self.game_state)

        if self._next_scene_name == "MAIN_MENU":
            from scenes.main_menu import MainMenuScene
            return MainMenuScene(self.screen, self.game_state)

        return None

