import pygame
import os

class TypewriterText:
    def __init__(self, lines, typing_speed=30, sound_path="assets/audio/typing.wav"):
        """
        lines: list of strings to display
        typing_speed: milliseconds per character
        sound_path: optional typing sound
        """
        self.lines = lines
        self.typing_speed = typing_speed  # milliseconds per character

        # Combine all lines into one stream
        self.total_text = "\n".join(self.lines)
        self.visible_chars = 0
        self.finished = False

        # Timing
        self.last_update = pygame.time.get_ticks()

        # Blinking cursor
        self.cursor_visible = True
        self.last_blink_time = pygame.time.get_ticks()
        self.blink_interval = 500  # milliseconds

        # Optional typing sound
        self.typing_sound = None
        if sound_path and os.path.exists(sound_path):
            self.typing_sound = pygame.mixer.Sound(sound_path)
            self.typing_sound.set_volume(0.25)

    # ---------------------------
    # Update per frame
    # ---------------------------
    def update(self):
        now = pygame.time.get_ticks()

        # Update typing effect
        if not self.finished and now - self.last_update >= self.typing_speed:
            self.visible_chars += 1
            self.last_update = now

            if self.typing_sound:
                self.typing_sound.play()

            if self.visible_chars >= len(self.total_text):
                self.visible_chars = len(self.total_text)
                self.finished = True

        # Update blinking cursor
        if now - self.last_blink_time >= self.blink_interval:
            self.cursor_visible = not self.cursor_visible
            self.last_blink_time = now

    # ---------------------------
    # Skip typing
    # ---------------------------
    def skip(self):
        self.visible_chars = len(self.total_text)
        self.finished = True

    # ---------------------------
    # Get visible lines
    # ---------------------------
    def get_visible_lines(self):
        visible_text = self.total_text[:self.visible_chars]
        return visible_text.split("\n")

    # ---------------------------
    # Get blinking cursor
    # ---------------------------
    def get_cursor(self, waiting_for_input=False):
        """
        Returns the blinking block cursor if not finished or waiting for input.
        """
        if self.finished and not waiting_for_input:
            return ""
        # Solid block cursor that blinks every 400ms
        return "█" if (pygame.time.get_ticks() // 400) % 2 == 0 else ""


