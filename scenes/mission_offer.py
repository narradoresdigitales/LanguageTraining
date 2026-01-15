import pygame
from settings import SCREEN_WIDTH, SCREEN_HEIGHT, TEXT_COLOR, FONT_NAME, FONT_SIZE, LINE_SPACING
from save.save_manager import save_game

class MissionOfferScene:
    def __init__(self, screen, game_state):
        self.screen = screen
        self.game_state = game_state
        self.font = pygame.font.SysFont(FONT_NAME, FONT_SIZE)

        self.finished = False
        self._next_scene_name = None

        # Text message in Spanish
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
        if event.type != pygame.KEYDOWN:
            return

        if event.key == pygame.K_a:
            self._accept()
        elif event.key == pygame.K_d:
            self._decline()

    def _accept(self):
        self.game_state.mission2_accepted = True
        self._next_scene_name = "MISSION2"
        self.finished = True
        save_game(self.game_state.to_dict())

    def _decline(self):
        self.game_state.mission2_accepted = False
        self._next_scene_name = "MAIN_MENU"
        self.finished = True
        save_game(self.game_state.to_dict())

    # ---------------------------
    # UPDATE
    # ---------------------------
    def update(self):
        pass

    # ---------------------------
    # DRAW
    # ---------------------------
    def draw(self):
        self.screen.fill((0, 0, 0))
        y = 50

        # Draw text in green
        for line in self.text:
            rendered = self.font.render(line, True, (0, 255, 0))
            rect = rendered.get_rect(centerx=SCREEN_WIDTH // 2, y=y)
            self.screen.blit(rendered, rect)
            y += FONT_SIZE + LINE_SPACING

    # ---------------------------
    # SCENE TRANSITION
    # ---------------------------
    def next_scene(self):
        if self._next_scene_name == "MISSION2":
            from scenes.mission2 import Mission2Scene  # stub for now
            return Mission2Scene(self.screen, self.game_state)
        elif self._next_scene_name == "MAIN_MENU":
            from scenes.main_menu import MainMenuScene
            return MainMenuScene(self.screen, self.game_state)
        return None
