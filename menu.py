import pygame

class Menu:
    def __init__(self):
        self.font = pygame.font.Font(None, 36)  
        self.hover_color = (255, 255, 0)  # Color when mouse is over the option
        
        # Render the text for each menu option
        self.play_text = self.font.render('Play', True, (255, 255, 255))
        self.how_to_play_text = self.font.render('How to Play', True, (255, 255, 255))  
        self.exit_text = self.font.render('Exit', True, (255, 255, 255))  
        self.back_text = self.font.render('Back', True, (255, 255, 255))  

        # Define the rectangles for each menu option
        self.play_rect = pygame.Rect(0, 0, 200, 50)  
        self.play_rect.center = (200, 200)
        self.how_to_play_rect = pygame.Rect(0, 0, 200, 50)  
        self.how_to_play_rect.center = (200, 250)
        self.exit_rect = pygame.Rect(0, 0, 200, 50)  
        self.exit_rect.center = (200, 300)
        self.back_rect = pygame.Rect(0, 0, 200, 50)  
        self.back_rect.center = (200, 400)  

    def draw_back_button(self, display):
        mouse_pos = pygame.mouse.get_pos() 

        # Change the color of the "Back" button if the mouse is over it
        back_color = self.hover_color if self.back_rect.collidepoint(mouse_pos) else (255, 255, 255)
        
        # Render the text with the new color
        back_text = self.font.render('Back', True, back_color)
        
        # Draw the back button
        display.blit(back_text, self.back_rect)

    def draw(self, display):
        mouse_pos = pygame.mouse.get_pos() 

        # Change the color of the menu options if the mouse is over them
        play_color = self.hover_color if self.play_rect.collidepoint(mouse_pos) else (255, 255, 255)
        how_to_play_color = self.hover_color if self.how_to_play_rect.collidepoint(mouse_pos) else (255, 255, 255)
        exit_color = self.hover_color if self.exit_rect.collidepoint(mouse_pos) else (255, 255, 255)

        # Render the text with the new color
        play_text = self.font.render('Play', True, play_color)
        how_to_play_text = self.font.render('How to Play', True, how_to_play_color)
        exit_text = self.font.render('Exit', True, exit_color)

        # Draw the menu options
        display.blit(play_text, self.play_rect)
        display.blit(how_to_play_text, self.how_to_play_rect)
        display.blit(exit_text, self.exit_rect)
        

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.back_rect.collidepoint(event.pos):
                return 'back'
            if self.play_rect.collidepoint(event.pos):
                return 'play'
            elif self.how_to_play_rect.collidepoint(event.pos):
                return 'how-to-play'
            elif self.exit_rect.collidepoint(event.pos):
                return 'exit'