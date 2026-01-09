import json 
import pygame
import os 
from settings import TEXT_COLOR, FONT_NAME, FONT_SIZE, LINE_SPACING, SCREEN_WIDTH, SCREEN_HEIGHT, FRAME_WIDTH
from utils.text import draw_centered_text


class Mission1Scene:
    def __init__(self, screen):
        self.screen = screen
        self.font = pygame.font.SysFont(FONT_NAME, FONT_SIZE)
        
        
        
        
        # Load NPC dialogue
        path = os.path.join('data', 'npc_dialogue.json')
        with open(path, 'r', encoding='utf-8') as f:
            self.dialogue_data = json.load(f)['mission1']
    
        self.transcript = self.dialogue_data['transcript']
        self.current_transcript_index = 0
        
        # Questions
        self.questions = self.dialogue_data['questions']
        self.current_question_index = 0
        
        self.input_text = ''
        self.feedback = ''
        self.showing_transcript = True 
        self.submitted = False 
        
    
    def handle_event(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_BACKSPACE:
                self.input_text = self.input_text[:-1]
                
            elif event.key == pygame.K_RETURN:
                if self.showing_transcript:
                    # Advance the transcript line
                    self.current_transcript_index += 1
                    if self.current_transcript_index >= len(self.transcript):
                        self.showing_transcript = False # Done with transcript
                elif self.input_text.strip() and not self.submitted:
                    # Evaluate player answer
                    self.evaluate_response()
                    self.submitted = True 
            
            elif event.unicode.isprintable():
                self.input_text += event.unicode
                self.submitted = False # Reset for typing 
    
    def evaluate_response(self):
        response = self.input_text.lower()
        current_question = self.questions[self.current_question_index]
        required = current_question['required_keywords']
        
        missing = [word for word in required if word not in response]
        
        if not missing:
            self.feedback = current_question['npc_response_success']
        else:
            self.feedback = current_question['npc_response_failure'] + ' Faltan: '  + ','  .join(missing)
        
        # Clear input after evaluation
        self.input_text = '' 
    
        # Move to next question if successful
        if not missing:
            self.current_question_index += 1
            self.feedback = '' # Clear feedback before next question
            if self.current_question_index >= len(self.questions):
                self.feedback = '¡Misión completada!'
    
    def update(self):
        pass
    
    def draw(self):
        
        self.screen.fill((0, 0, 0))  # Black background

        # Draw terminal frame
        margin = 40
        TEXT_COLOR = (0, 255, 0)
        frame_rect = pygame.Rect(
            margin,
            margin,
        self.screen.get_width() - margin * 2,
        self.screen.get_height() - margin * 2
        )
        pygame.draw.rect(self.screen, TEXT_COLOR, frame_rect, 2)

        # Text start position inside frame
        y_offset = frame_rect.top + 20
        text_x = frame_rect.left + 20
    

        # --- Display transcript ---
        if self.showing_transcript:
            for i in range(self.current_transcript_index + 1):
                line_height = draw_centered_text(
                    self.screen,
                    self.font,
                    self.transcript[i],
                    y_offset,
                    TEXT_COLOR
                )
                y_offset += line_height + LINE_SPACING
        
        # Add extra vertical space before the prompt
            y_offset += 20  # extra space in pixels 
            
            prompt = self.font.render(
            'Presione ENTER para continuar la transcripción...', True, TEXT_COLOR
            )
            
            prompt_rect = prompt.get_rect()
            prompt_rect.centerx = self.screen.get_width() // 2
            prompt_rect.y = y_offset
            
            self.screen.blit(prompt, prompt_rect)

        # --- Display "All questions completed" message ---
        elif self.current_question_index >= len(self.questions):
            
            draw_centered_text(
                self.screen,
                self.font,
                '¡Todas las preguntas completadas!',
                y_offset,
                TEXT_COLOR
            )
            

        # --- Display current question, input, and feedback ---
        else:
            # Display current question
            question = self.questions[self.current_question_index]['prompt']
            line_height = draw_centered_text(
                self.screen,
                self.font,
                question,
                y_offset,
                TEXT_COLOR
            )
            y_offset += line_height + LINE_SPACING

            # Display player input
            line_height = draw_centered_text(
                self.screen,
                self.font,
                'Respuesta: ' + self.input_text,
                y_offset,
                TEXT_COLOR
            )
            y_offset += line_height + LINE_SPACING


            # Display feedback if it exists
            if self.feedback:
                draw_centered_text(
                self.screen,
                self.font,
                self.feedback,
                y_offset,
                TEXT_COLOR
                )


        
        
        
        
