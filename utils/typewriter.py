import pygame
import os

class TypewriterText:
    def __init__(self, lines, typing_speed=30, sound_path="assets/audio/typing.wav"):
        self.lines = lines
        self.typing_speed = typing_speed  # milliseconds per character

        # Combine all lines into one stream
        self.total_text = "\n".join(self.lines)

        self.visible_chars = 0
        self.finished = False

        self.last_update = pygame.time.get_ticks()

        # Optional typing sound
        self.typing_sound = None
        if sound_path and os.path.exists(sound_path):
            self.typing_sound = pygame.mixer.Sound(sound_path)
            self.typing_sound.set_volume(0.25)

    def update(self):
        if self.finished:
            return

        now = pygame.time.get_ticks()
        if now - self.last_update >= self.typing_speed:
            self.visible_chars += 1
            self.last_update = now

            if self.typing_sound:
                self.typing_sound.play()

            if self.visible_chars >= len(self.total_text):
                self.visible_chars = len(self.total_text)
                self.finished = True

    def skip(self):
        self.visible_chars = len(self.total_text)
        self.finished = True

    def get_visible_lines(self):
        visible_text = self.total_text[:self.visible_chars]
        return visible_text.split("\n")

    def get_cursor(self):
        if self.finished:
            return ""
        return "_" if (pygame.time.get_ticks() // 400) % 2 == 0 else ""
