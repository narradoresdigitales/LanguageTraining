import pygame
from settings import TEXT_COLOR, FONT_NAME, FONT_SIZE, SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_MARGIN, FRAME_WIDTH

class IntroScene:
    def __init__(self, screen, game_state):
        self.screen = screen
        self.game_state = game_state
        self.finished = False
        self._next_scene_name = None

        self.screen_rect = pygame.Rect(
            SCREEN_MARGIN,
            SCREEN_MARGIN,
            self.screen.get_width() - SCREEN_MARGIN * 2,
            self.screen.get_height() - SCREEN_MARGIN * 2
        )
        self.font = pygame.font.SysFont(FONT_NAME, FONT_SIZE)

        self.text = [
            'Mission 1: Initial Contact',
            '',
            'You are conducting a field interview',
            'Your objective is to gather information',
            'using appropriate Spanish register.',
            '',
            'Press any key to begin.'
        ]

    def handle_event(self, event):
        if event.type == pygame.KEYDOWN:
            # Any key press advances to Mission1
            self.finished = True
            self._next_scene_name = "MISSION1"

    def update(self):
        pass

    def draw(self):
        # Black background (Matrix terminal style)
        self.screen.fill((0, 0, 0))

        # Terminal frame
        pygame.draw.rect(
            self.screen,
            TEXT_COLOR,
            self.screen_rect,
            FRAME_WIDTH
        )

        # Draw text
        y = self.screen_rect.top + 80
        for line in self.text:
            rendered = self.font.render(line, True, TEXT_COLOR)
            rect = rendered.get_rect(centerx=self.screen.get_width() // 2)
            rect.y = y
            self.screen.blit(rendered, rect)
            y += 35


    def next_scene(self):
        """Return the next scene object based on next_scene_name."""
        if self._next_scene_name == "MISSION1":
            from scenes.mission1 import Mission1Scene
            return Mission1Scene(self.screen, self.game_state)
        return None
