import random
import sys
import pygame

from bin import Bin
from menu import Menu
from paper import Paper
from sound_manager import SoundManager
from spritesheet import SpriteSheet


class Game:
    def __init__(self):
        pygame.init()
        self.setup_display()
        self.setup_game_variables()
        self.setup_sound_manager()
        self.sound_manager.play_bgm('assets/sounds/bgm.mp3')
        

    def setup_display(self):
        self.display = pygame.display.set_mode((800, 600))
        self.background = pygame.image.load('assets/background.png').convert()
        self.background = pygame.transform.scale(self.background, (800, 600))
        self.grey_overlay = pygame.Surface((800, 600), pygame.SRCALPHA)
        self.grey_overlay.fill((128, 128, 128, 150))

    def setup_game_variables(self):
        self.running = True
        self.menu = Menu()
        self.state = 'menu'
        self.start_time = None
        self.spawn_bins()
        self.spawn_paper()
        self.score = 0
        self.throw_start = None
        self.level = 1
        self.level_times = {1: 10, 2: 8, 3: 6, 4: 4, 5: 2, 6: 1}

    def setup_sound_manager(self):
        self.sound_manager = SoundManager()
        self.sound_manager.load_sound('gameover', 'assets/sounds/gameover.mp3')
        self.sound_manager.load_sound('score', 'assets/sounds/score.mp3')
        self.sound_manager.load_sound('throw', 'assets/sounds/throw.mp3')
    
    def update_game_state(self):
        current_time = pygame.time.get_ticks()
        remaining_time = self.level_times[self.level] - (current_time - self.start_time) // 1000
        if remaining_time <= 0:
            self.state = 'game_over'
            
        else:
            self.display_remaining_time(remaining_time)
            self.check_in_bins()
           
    def level_up(self):
        self.level += 1
        if self.level > 6:
            self.state = 'game_over'
        else:
            self.reset_game()
            self.start_time = pygame.time.get_ticks()  # Reset the start time for the new level
        
    def run(self):
        while self.running:
            self.handle_events()
            self.update_display()
        pygame.quit()

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False

            action = self.menu.handle_event(event)
            if action == 'play':
                self.state = 'play'
            elif action == 'exit':
                self.running = False

            if self.state == 'play':
                self.handle_play_events(event)

    def handle_play_events(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = pygame.mouse.get_pos()
            if self.paper.rect.collidepoint(mouse_pos):
                self.throw_start = mouse_pos
        elif event.type == pygame.MOUSEBUTTONUP:
            if self.throw_start is not None:
                throw_end = pygame.mouse.get_pos()
                self.paper.throw(self.throw_start, throw_end)
                self.throw_start = None
                self.sound_manager.play_sound('throw')
    
    def display_remaining_time(self, remaining_time):
        self.display_text(str(max(remaining_time, 0)), (10, 10), 74, (255, 0, 0))


    def display_text(self, text, position, size, color):
        """Display text on the screen at the given position."""
        font = pygame.font.Font(None, size)
        text_surface = font.render(text, True, color)
        self.display.blit(text_surface, position)

    def update_display(self):
        self.display.blit(self.background, (0, 0))
        self.display.blit(self.grey_overlay, (0, 0))

        if self.state == 'menu':
            self.menu.draw(self.display)
        elif self.state == 'play':
            self.play_game()
            # self.display_text(f'Score: {self.score}', (10, 50), 30, (255, 255, 255))  # Display the score
            self.display_text(f'Level: {self.level}', (10, 80), 30, (255, 255, 255))  # Display the level
        elif self.state == 'game_over':
            self.game_over()

        pygame.display.flip()

    def throw_paper(self, throw_end):
        self.paper.throw(self.throw_start, throw_end)

    def reset_game(self):
        self.score = 0  # Reset the score
        self.spawn_paper()  # Spawn a new paper
        self.start_time = pygame.time.get_ticks()  # Reset the start time


    def game_over(self):
        self.display.blit(self.grey_overlay, (0, 0))  # Draw the grey overlay
        font = pygame.font.Font(None, 74)
        text = font.render('Game Over', 1, (255, 0, 0))
        self.display.blit(text, (250, 250))
        pygame.display.flip()  # Update the display
        pygame.time.wait(1000)  # Wait for 1 second
        self.reset_game()  # Reset the game
        self.level = 1

        self.state = 'menu'  # Change the state back to 'menu'

    def play_game(self):
        self.bins.draw(self.display)  # Draw the bins
        self.all_sprites.update()  # Update all sprites
        self.all_sprites.draw(self.display)  # Draw all sprites
        self.update_game_state()
        
        
    def check_in_bins(self):
        for bin in self.bins:
            if bin.opening.colliderect(self.paper.rect) and self.paper.velocity.y > 0:
                if bin.bin_type == self.paper.paper_type:
                    self.score += 1
                    self.sound_manager.play_sound('score')
                    self.spawn_paper()
                    self.level_up()  # Increase the level and decrease the countdown
                else:
                    self.state = 'game_over'
                break

    def spawn_bins(self):
        # List of bin positions
        bin_positions = [150, 350, 550]
        random.shuffle(bin_positions)  # Shuffle the positions

        # List of bin types
        bin_types = [
            ('assets/cans/green-trash-can.png', 1),
            ('assets/cans/blue-trash-can.png', 2),
            ('assets/cans/red-trash-can.png', 3)
        ]

        # Create a group of bins with random positions
        self.bins = pygame.sprite.Group(
            Bin(image, position, 180, bin_type)
            for (image, bin_type), position in zip(bin_types, bin_positions)
        )
    def spawn_paper(self):
        # Define a dictionary of paperball assets and their corresponding types
        paperball_assets = {
            'assets\paper\paperball-1.png': 1,
            'assets\paper\paperball-3.png': 3,
            'assets\paper\paperball-ip.png': 2
        }

        # Randomly select a paperball asset and its corresponding type
        selected_paperball, paper_type = random.choice(list(paperball_assets.items()))

        spritesheet = SpriteSheet(selected_paperball, 50, 60)  # Create a SpriteSheet instance with the selected paperball

        self.spawn_bins()  # Randomly select a paper type
        self.paper = Paper(spritesheet, 0, 3, 380, 500, 800, 600, paper_type)  # Create a Paper instance with 3 sprites
        self.all_sprites = pygame.sprite.Group(self.paper)  # Add the paper to a sprite group
        self.start_time = pygame.time.get_ticks()
# Run the game
game = Game()
game.run()