import pygame


class Menu:
    def __init__(self):
        self.font = pygame.font.Font(None, 36)  # Use the default font, size 36
        self.play_text = self.font.render('Play', True, (255, 255, 255))  # White text
        self.exit_text = self.font.render('Exit', True, (255, 255, 255))  # White text
        self.play_rect = self.play_text.get_rect(center=(200, 200))  # Position the 'Play' text
        self.exit_rect = self.exit_text.get_rect(center=(200, 250))  # Position the 'Exit' text

    def draw(self, display):
        display.blit(self.play_text, self.play_rect)
        display.blit(self.exit_text, self.exit_rect)

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.play_rect.collidepoint(event.pos):
                return 'play'
            elif self.exit_rect.collidepoint(event.pos):
                return 'exit'