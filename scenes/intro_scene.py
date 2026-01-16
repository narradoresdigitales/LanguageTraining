# intro_scene.py
import pygame
from settings import TEXT_COLOR, FONT_NAME, FONT_SIZE, SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_MARGIN, FRAME_WIDTH
from utils.typewriter import TypewriterText
from scenes.mission1 import Mission1Scene

class IntroScene:
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
            "== CANAL SEGURO ESTABLECIDO ==",
            "",
            "ORIGEN: COMANDO LINGÜÍSTICO",
            "DESTINO: OPERADOR",
            "",
            "Hemos interceptado un mensaje cifrado.",
            "",
            "Usted ha sido seleccionado para",
            "una misión de contacto inicial.",
            "",
            "OBJETIVO:",
            "Obtener información clave.",
            "",
            "IDIOMA OPERATIVO: ESPAÑOL",
            "",
            "Presione cualquier tecla para continuar..."
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
            self.finished = True
            self._next_scene_name = "MISSION1"

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
        cursor = self.typewriter.get_cursor()
        if cursor and last_rect and not self.typewriter.finished:
            cursor_surface = self.font.render(cursor, True, TEXT_COLOR)
            self.screen.blit(cursor_surface, (last_rect.right + 5, last_rect.y))

    # ---------------------------
    # NEXT SCENE
    # ---------------------------
    def next_scene(self):
        if self._next_scene_name == "MISSION1":
            return Mission1Scene(self.screen, self.game_state)
        return None
