import pygame
import os
import json
from settings import TEXT_COLOR, FONT_NAME, FONT_SIZE, LINE_SPACING
from utils.text import draw_centered_text
from save.save_manager import save_game

class Mission1Scene:
    def __init__(self, screen, game_state):
        self.screen = screen
        self.game_state = game_state
        self.finished = False
        self.font = pygame.font.SysFont(FONT_NAME, FONT_SIZE)
        self.showing_transcript = True
        self.current_transcript_index = 0
        self.current_question_index = 0
        self.input_text = ''
        self.feedback = ''

        # Load dialogue
        path = os.path.join('data', 'npc_dialogue.json')
        with open(path, 'r', encoding='utf-8') as f:
            data = json.load(f)['mission1']
        self.transcript = data['transcript']
        self.questions = data['questions']

    def handle_event(self, event):
        if event.type != pygame.KEYDOWN:
            return
        if event.key == pygame.K_BACKSPACE:
            self.input_text = self.input_text[:-1]
        elif event.key == pygame.K_RETURN:
            if self.showing_transcript:
                self.current_transcript_index += 1
                if self.current_transcript_index >= len(self.transcript):
                    self.showing_transcript = False
            elif self.input_text.strip():
                self.evaluate_response()
        elif event.unicode.isprintable():
            self.input_text += event.unicode

    def evaluate_response(self):
        current = self.questions[self.current_question_index]
        response = self.input_text.lower()
        missing = [w for w in current['required_keywords'] if w not in response]

        if not missing:
            self.feedback = current['npc_response_success']
            self.current_question_index += 1
        else:
            self.feedback = current['npc_response_failure'] + " Faltan: " + ', '.join(missing)

        self.input_text = ''

        if self.current_question_index >= len(self.questions):
            self.feedback = "¡Misión completada!"
            self.game_state.current_mission = 'mission_1'
            self.game_state.missions_completed['mission_1'] = 'completed'
            save_game(self.game_state.to_dict())
            self.finished = True

    def update(self):
        pass

    def draw(self):
        self.screen.fill((0, 0, 0))
        y_offset = 40
        if self.showing_transcript:
            for i in range(self.current_transcript_index + 1):
                h = draw_centered_text(self.screen, self.font, self.transcript[i], y_offset, TEXT_COLOR)
                y_offset += h + LINE_SPACING
            y_offset += 20
            prompt = self.font.render("Press ENTER to continue transcript...", True, TEXT_COLOR)
            rect = prompt.get_rect(centerx=self.screen.get_width() // 2, y=y_offset)
            self.screen.blit(prompt, rect)
        elif self.current_question_index < len(self.questions):
            q = self.questions[self.current_question_index]['prompt']
            h = draw_centered_text(self.screen, self.font, q, y_offset, TEXT_COLOR)
            y_offset += h + LINE_SPACING
            h = draw_centered_text(self.screen, self.font, "Respuesta: " + self.input_text, y_offset, TEXT_COLOR)
            y_offset += h + LINE_SPACING
            if self.feedback:
                draw_centered_text(self.screen, self.font, self.feedback, y_offset, TEXT_COLOR)
        else:
            draw_centered_text(self.screen, self.font, "¡Todas las preguntas completadas!", y_offset, TEXT_COLOR)

    def next_scene(self):
        from scenes.main_menu import MainMenuScene
        return MainMenuScene(self.screen, self.game_state)
