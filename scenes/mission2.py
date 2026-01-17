# mission2.py
import pygame
from settings import TEXT_COLOR, FONT_NAME, FONT_SIZE, SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_MARGIN, FRAME_WIDTH
from utils.typewriter import TypewriterText
from scenes.main_menu import MainMenuScene

class Mission2Scene:
    def __init__(self, screen, game_state, sprite_path="assets/images/fem_civ.png"):
        self.screen = screen
        self.game_state = game_state
        self.finished = False
        self._next_scene_name = None

        # Font and frame
        self.font = pygame.font.SysFont(FONT_NAME, FONT_SIZE)
        self.screen_rect = pygame.Rect(
            SCREEN_MARGIN,
            SCREEN_MARGIN,
            SCREEN_WIDTH - SCREEN_MARGIN * 2,
            SCREEN_HEIGHT - SCREEN_MARGIN * 2
        )

        # Typewriter text
        self.text = [
            "== MENSAJE PRIORITARIO ==",
            "",
            "ORIGEN: COMANDO LINGÜÍSTICO",
            "",
            "Su desempeño en la misión anterior ha sido evaluado.",
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

        # Sprite setup
        self.sprite = None
        if sprite_path:
            self.sprite = pygame.image.load(sprite_path).convert_alpha()
            self.sprite_rect = self.sprite.get_rect()
            self.sprite_target_x = SCREEN_WIDTH - self.sprite_rect.width - SCREEN_MARGIN
            self.sprite_rect.x = -self.sprite_rect.width  # start offscreen
            self.sprite_rect.y = SCREEN_HEIGHT // 2 - self.sprite_rect.height // 2
            self.sprite_speed = 5  # pixels per frame

    # ---------------------------
    # INPUT
    # ---------------------------
    def handle_event(self, event):
        if event.type != pygame.KEYDOWN:
            return

        if not self.typewriter.finished:
            self.typewriter.skip()
        else:
            # Accept / Decline
            if event.key == pygame.K_a:
                self.finished = True
                self._next_scene_name = "MISSION3"  # or next mission scene
            elif event.key == pygame.K_d:
                self.finished = True
                self._next_scene_name = "MAIN_MENU"

    # ---------------------------
    # UPDATE
    # ---------------------------
    def update(self):
        self.typewriter.update()
        # Move sprite toward target x
        if self.sprite and self.sprite_rect.x < self.sprite_target_x:
            self.sprite_rect.x += self.sprite_speed
            if self.sprite_rect.x > self.sprite_target_x:
                self.sprite_rect.x = self.sprite_target_x

    # ---------------------------
    # DRAW
    # ---------------------------
    def draw(self):
        # Background
        self.screen.fill((0, 0, 0))
        pygame.draw.rect(self.screen, TEXT_COLOR, self.screen_rect, FRAME_WIDTH)

        # Typewriter text
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

        # Draw sprite
        if self.sprite:
            self.screen.blit(self.sprite, self.sprite_rect)

    # ---------------------------
    # NEXT SCENE
    # ---------------------------
    def next_scene(self):
        if self._next_scene_name == "MISSION3":
            from scenes.mission3 import Mission3Scene
            return Mission3Scene(self.screen, self.game_state)
        elif self._next_scene_name == "MAIN_MENU":
            return MainMenuScene(self.screen, self.game_state)
        return None
