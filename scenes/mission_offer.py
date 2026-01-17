# mission_offer.py
import pygame
from settings import TEXT_COLOR, FONT_NAME, FONT_SIZE, SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_MARGIN, FRAME_WIDTH
from utils.typewriter import TypewriterText
from scenes.mission2 import Mission2Scene
from scenes.main_menu import MainMenuScene

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

        self.typewriter = TypewriterText(self.text, typing_speed=35)

    # ---------------------------
    # INPUT
    # ---------------------------
    def handle_event(self, event):
        if event.type != pygame.KEYDOWN:
            return

        if not self.typewriter.finished:
            self.typewriter.skip()
        else:
            if event.key == pygame.K_a:  # Accept mission
                self.finished = True
                self._next_scene_name = "MISSION2"
            elif event.key == pygame.K_d:  # Decline mission
                self.finished = True
                self._next_scene_name = "MAIN_MENU"

    # ---------------------------
    # UPDATE
    # ---------------------------
    def update(self):
        self.typewriter.update()

    # ---------------------------
    # DRAW
    # ---------------------------
    def draw(self):
        self.screen.fill((0, 0, 0))
        pygame.draw.rect(self.screen, TEXT_COLOR, self.screen_rect, FRAME_WIDTH)

        visible_lines = self.typewriter.get_visible_lines()
        line_height = FONT_SIZE + 5

        frame_top = self.screen_rect.top + 20
        frame_bottom = self.screen_rect.bottom - 20
        total_text_height = len(visible_lines) * line_height
        y = frame_top + (frame_bottom - frame_top - total_text_height) // 2

        last_rect = None
        for line in visible_lines:
            rendered = self.font.render(line, True, TEXT_COLOR)
            rect = rendered.get_rect(centerx=self.screen.get_width() // 2, y=y)
            self.screen.blit(rendered, rect)
            last_rect = rect
            y += line_height

        # Blinking cursor
        cursor = self.typewriter.get_cursor(waiting_for_input=self.typewriter.finished)
        if cursor and last_rect:
            cursor_surface = self.font.render(cursor, True, TEXT_COLOR)
            self.screen.blit(cursor_surface, (last_rect.right + 2, last_rect.y))

    # ---------------------------
    # NEXT SCENE
    # ---------------------------
    def next_scene(self):
        if self._next_scene_name == "MISSION2":
            return Mission2Scene(self.screen, self.game_state)
        elif self._next_scene_name == "MAIN_MENU":
            return MainMenuScene(self.screen, self.game_state)
        return None
