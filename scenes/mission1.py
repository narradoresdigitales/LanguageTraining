import pygame
import json
import os
from settings import TEXT_COLOR, FONT_NAME, FONT_SIZE, LINE_SPACING
from utils.text import draw_centered_text
from utils.typewriter import TypewriterText
from save.save_manager import save_game

class Mission1Scene:
    def __init__(self, screen, game_state):
        self.screen = screen
        self.game_state = game_state
        self.finished = False
        self._next_scene_name = None

        self.font = pygame.font.SysFont(FONT_NAME, FONT_SIZE)

        # Load NPC dialogue
        path = os.path.join('data', 'npc_dialogue.json')
        with open(path, 'r', encoding='utf-8') as f:
            self.dialogue_data = json.load(f)['mission1']

        self.transcript = self.dialogue_data['transcript']
        self.current_transcript_index = 0
        self.showing_transcript = True
        self.typewriter = TypewriterText([self.transcript[0]], typing_speed=35)

        # Questions
        self.questions = self.dialogue_data['questions']
        self.current_question_index = 0
        self.input_text = ''
        self.feedback = ''
        self.submitted = False

    # ---------------------------
    # INPUT
    # ---------------------------
    def handle_event(self, event):
        if event.type != pygame.KEYDOWN:
            return

        if self.showing_transcript:
            if not self.typewriter.finished:
                self.typewriter.skip()
            else:
                # Move to next transcript line
                self.current_transcript_index += 1
                if self.current_transcript_index < len(self.transcript):
                    self.typewriter = TypewriterText(
                        [self.transcript[self.current_transcript_index]],
                        typing_speed=35
                    )
                else:
                    self.showing_transcript = False

        else:  # Question mode
            if event.key == pygame.K_BACKSPACE:
                self.input_text = self.input_text[:-1]
            elif event.key == pygame.K_RETURN:
                if self.input_text.strip() and not self.submitted:
                    self.evaluate_response()
                    self.submitted = True
            elif event.unicode.isprintable():
                self.input_text += event.unicode
                self.submitted = False  # reset after typing

    # ---------------------------
    # LOGIC
    # ---------------------------
    def evaluate_response(self):
        response = self.input_text.lower()
        current_question = self.questions[self.current_question_index]
        required = current_question['required_keywords']

        missing = [word for word in required if word not in response]

        if not missing:
            self.feedback = current_question['npc_response_success']
            self.current_question_index += 1
            self.input_text = ''
            self.submitted = False
            if self.current_question_index >= len(self.questions):
                self.game_state.current_mission = 'mission_1'
                self.game_state.missions_completed['mission_1'] = 'completed'
                save_game(self.game_state.to_dict())
                self.finished = True
                self._next_scene_name = "MISSION_OFFER"
        else:
            self.feedback = current_question['npc_response_failure'] + ' Faltan: ' + ', '.join(missing)
            self.input_text = ''
            self.submitted = False

    # ---------------------------
    # UPDATE
    # ---------------------------
    def update(self):
        if self.showing_transcript and self.typewriter:
            self.typewriter.update()

    # ---------------------------
    # DRAW
    # ---------------------------
    def draw(self):
        self.screen.fill((0, 0, 0))
        margin = 40
        frame_rect = pygame.Rect(
            margin, margin,
            self.screen.get_width() - margin * 2,
            self.screen.get_height() - margin * 2
        )
        pygame.draw.rect(self.screen, TEXT_COLOR, frame_rect, 2)

        y = frame_rect.top + 40

        if self.showing_transcript:
            visible_lines = self.typewriter.get_visible_lines()
            last_rect = None

            for line in visible_lines:
                rendered = self.font.render(line, True, TEXT_COLOR)
                rect = rendered.get_rect(centerx=self.screen.get_width() // 2, y=y)
                self.screen.blit(rendered, rect)
                last_rect = rect
                y += FONT_SIZE + LINE_SPACING

            # Cursor
            cursor = self.typewriter.get_cursor()
            if cursor and last_rect and not self.typewriter.finished:
                cursor_surface = self.font.render(cursor, True, TEXT_COLOR)
                self.screen.blit(
                    cursor_surface,
                    (last_rect.right + 5, last_rect.y)
                )

            # Hint to press ENTER
            if self.typewriter.finished:
                hint = self.font.render(
                    "(ENTER para continuar)",
                    True,
                    TEXT_COLOR
                )
                hint_rect = hint.get_rect(centerx=self.screen.get_width() // 2, y=y + 10)
                self.screen.blit(hint, hint_rect)

        else:  # Questions
            question = self.questions[self.current_question_index]['prompt']
            draw_centered_text(self.screen, self.font, question, y, TEXT_COLOR)
            y += FONT_SIZE + LINE_SPACING
            draw_centered_text(
                self.screen,
                self.font,
                "Respuesta: " + self.input_text,
                y,
                TEXT_COLOR
            )
            y += FONT_SIZE + LINE_SPACING

            if self.feedback:
                draw_centered_text(self.screen, self.font, self.feedback, y, TEXT_COLOR)

    # ---------------------------
    # SCENE TRANSITION
    # ---------------------------
    def next_scene(self):
        if self._next_scene_name == "MISSION_OFFER":
            from scenes.mission_offer import MissionOfferScene
            return MissionOfferScene(self.screen, self.game_state)
        return None
