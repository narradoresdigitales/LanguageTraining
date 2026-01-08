import json 
import pygame
import os 
from settings import WHITE, BLACK, FONT_NAME, FONT_SIZE, LINE_SPACING


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
        self.screen.fill(WHITE)
        y_offset = 20

        # --- Display transcript ---
        if self.showing_transcript:
            for i in range(self.current_transcript_index + 1):
                line = self.font.render(self.transcript[i], True, BLACK)
                self.screen.blit(line, (50, y_offset))
                y_offset += FONT_SIZE + LINE_SPACING
        
        # Add extra vertical space before the prompt
            y_offset += 20  # extra space in pixels 
            
            prompt = self.font.render(
            'Presione ENTER para continuar la transcripción...', True, BLACK
            )
            self.screen.blit(prompt, (50, y_offset))

        # --- Display "All questions completed" message ---
        elif self.current_question_index >= len(self.questions):
            end_surface = self.font.render('¡Todas las preguntas completadas!', True, BLACK)
            self.screen.blit(end_surface, (50, y_offset))

        # --- Display current question, input, and feedback ---
        else:
            # Display current question
            question = self.questions[self.current_question_index]['prompt']
            q_surface = self.font.render(question, True, BLACK)
            self.screen.blit(q_surface, (50, y_offset))
            y_offset += FONT_SIZE + 20

            # Display player input
            input_surface = self.font.render('Respuesta: ' + self.input_text, True, BLACK)
            self.screen.blit(input_surface, (50, y_offset))
            y_offset += FONT_SIZE + 20

            # Display feedback if it exists
            if self.feedback:
                feedback_surface = self.font.render(self.feedback, True, BLACK)
                self.screen.blit(feedback_surface, (50, y_offset))


        
        
        
        
