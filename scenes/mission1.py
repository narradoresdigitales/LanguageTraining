import pygame
import json
import os
from settings import TEXT_COLOR, FONT_NAME, FONT_SIZE, LINE_SPACING
from utils.text import draw_centered_text
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

        self.questions = self.dialogue_data['questions']
        self.current_question_index = 0

        self.input_text = ''
        self.feedback = ''
        self.showing_transcript = True
        self.submitted = False

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
            elif self.input_text.strip() and not self.submitted:
                self.evaluate_response()
                self.submitted = True

        elif event.unicode.isprintable():
            self.input_text += event.unicode
            self.submitted = False

    def evaluate_response(self):
        response = self.input_text.lower()
        current_question = self.questions[self.current_question_index]
        required = current_question['required_keywords']

        missing = [word for word in required if word not in response]

        if not missing:
            self.feedback = current_question['npc_response_success']
        else:
            self.feedback = current_question['npc_response_failure'] + ' Faltan: ' + ', '.join(missing)

        self.input_text = ''

        if not missing:
            self.current_question_index += 1
            self.feedback = ''
            if self.current_question_index >= len(self.questions):
                self.feedback = '¡Misión completada!'
                self.game_state.current_mission = 'mission_1'
                self.game_state.missions_completed['mission_1'] = 'completed'
                save_game(self.game_state.to_dict())
                self.finished = True
                self._next_scene_name = "MISSION_OFFER"

    def update(self):
        pass

    def draw(self):
        self.screen.fill((0, 0, 0))
        margin = 40
        frame_rect = pygame.Rect(
            margin, margin,
            self.screen.get_width() - margin * 2,
            self.screen.get_height() - margin * 2
        )
        pygame.draw.rect(self.screen, TEXT_COLOR, frame_rect, 2)

        y_offset = frame_rect.top + 20

        if self.showing_transcript:
            for i in range(self.current_transcript_index + 1):
                line_height = draw_centered_text(self.screen, self.font, self.transcript[i], y_offset, TEXT_COLOR)
                y_offset += line_height + LINE_SPACING

            y_offset += 20
            prompt = self.font.render('(Presione ENTER para continuar la transcripción...)', True, TEXT_COLOR)
            prompt_rect = prompt.get_rect(centerx=self.screen.get_width() // 2)
            prompt_rect.y = y_offset
            self.screen.blit(prompt, prompt_rect)

        elif self.current_question_index < len(self.questions):
            question = self.questions[self.current_question_index]['prompt']
            line_height = draw_centered_text(self.screen, self.font, question, y_offset, TEXT_COLOR)
            y_offset += line_height + LINE_SPACING

            line_height = draw_centered_text(self.screen, self.font, 'Respuesta: ' + self.input_text, y_offset, TEXT_COLOR)
            y_offset += line_height + LINE_SPACING

            if self.feedback:
                draw_centered_text(self.screen, self.font, self.feedback, y_offset, TEXT_COLOR)
        else:
            draw_centered_text(self.screen, self.font, '¡Todas las preguntas completadas!', y_offset, TEXT_COLOR)

    def next_scene(self):
        """Return next scene based on finished mission."""
        if self._next_scene_name == "MISSION_OFFER":
            from scenes.mission_offer import MissionOfferScene
            return MissionOfferScene(self.screen, self.game_state)
        
        if self._next_scene_name == 'MAIN_MENU':
            from scenes.mission_offer import MainMenuScene
            return MainMenuScene(self.screen, self.game_state)
        
        return None
