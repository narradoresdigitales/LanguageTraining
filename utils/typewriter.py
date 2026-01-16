import pygame

class TypewriterText:
    def __init__(self, lines, typing_speed=30):
        self.lines = lines
        self.typing_speed = typing_speed

        self.current_line = 0
        self.current_char = 0
        self.finished = False

        self.last_update = pygame.time.get_ticks()
        self.cursor_visible = True
        self.cursor_timer = pygame.time.get_ticks()

    def update(self):
        if self.finished:
            return

        now = pygame.time.get_ticks()
        if now - self.last_update > self.typing_speed:
            self.last_update = now
            self.current_char += 1

            if self.current_char > len(self.lines[self.current_line]):
                self.current_char = 0
                self.current_line += 1

                if self.current_line >= len(self.lines):
                    self.finished = True

    def skip(self):
        self.current_line = len(self.lines)
        self.finished = True

    def get_visible_lines(self):
        visible = []

        for i in range(self.current_line):
            visible.append(self.lines[i])

        if not self.finished and self.current_line < len(self.lines):
            visible.append(self.lines[self.current_line][:self.current_char])

        return visible

    def get_cursor(self):
        if self.finished:
            return ""

        now = pygame.time.get_ticks()
        if now - self.cursor_timer > 500:
            self.cursor_visible = not self.cursor_visible
            self.cursor_timer = now

        return "█" if self.cursor_visible else ""
