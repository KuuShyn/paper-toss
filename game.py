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
        """
         Initialize pygame and sound manager. This is called from __init__ and can be overridden to do other things
        """
        pygame.init()
        self.setup_display()
        self.setup_game_variables()
        self.setup_sound_manager()
        self.sound_manager.play_bgm("assets/sounds/bgm.mp3")

    def setup_display(self):
        """
         Sets up the pygame display to work with Paper Toss. This is called by __init__
        """
        pygame.display.set_caption("Paper Toss")
        self.display = pygame.display.set_mode((800, 600))
        self.background = pygame.image.load("assets/background.png").convert()
        self.background = pygame.transform.scale(self.background, (800, 600))
        self.grey_overlay = pygame.Surface((800, 600), pygame.SRCALPHA)
        self.grey_overlay.fill((128, 128, 128, 150))
        self.font = pygame.font.Font(None, 36)
        icon = pygame.image.load('assets/icon.png')  # Load the icon
        pygame.display.set_icon(icon)

    def setup_game_variables(self):
        """
         Sets up variables that are used to start the game. This should be called at the beginning of the
        """
        self.running = True
        self.menu = Menu()
        self.state = "menu"
        self.start_time = None
        self.spawn_bins()
        self.spawn_paper()
        self.score = 0
        self.throw_start = None
        self.level = 1
        self.level_times = {1: 14, 
                            2: 12, 
                            3: 10, 
                            4: 8, 
                            5: 6, 
                            6: 4,
                            7: 2,
                            }

    def setup_sound_manager(self):
        """
         Loads sounds and puts them in self. sound_manager for use in tests. @untestable - just draws
        """
        self.sound_manager = SoundManager()
        self.sound_manager.load_sound("gameover", "assets/sounds/gameover.mp3")
        self.sound_manager.load_sound("score", "assets/sounds/score.mp3")
        self.sound_manager.load_sound("throw", "assets/sounds/throw.mp3")

    def update_game_state(self):
        """
         Update the game state based on the time elapsed since the last call to this function. This is called every frame
        """
        current_time = pygame.time.get_ticks()
        remaining_time = (
            self.level_times[self.level] - (current_time - self.start_time) // 1000
        )
        # display the remaining time in seconds
        if remaining_time <= 0:
            self.state = "game_over"

        else:
            self.display_remaining_time(remaining_time)
            self.check_in_bins()

    def level_up(self):
        """
         Increases the level by one and sets the game state to game_over if the level is greater than 7
        """
        self.level += 1
        # Reset the game state if level 7.
        if self.level > 7:
            self.state = "game_over"
        else:
            self.reset_game()
            self.start_time = pygame.time.get_ticks()

    def run(self):
        """
         Run the game loop. This is the main loop of the game loop. It handles events updates the display and quits
        """
        # This method is called by the user when the user is running.
        while self.running:
            self.handle_events()
            self.update_display()
        pygame.quit()

    def handle_events(self):
        """
         Handle pygame events and move to the next state if it's a play or quit. This is called from the main loop
        """
        # This method is called by pygame. event. get to handle the events.
        for event in pygame.event.get():
            # This method is called when the game is running.
            if event.type == pygame.QUIT:
                self.running = False

            action = self.menu.handle_event(event)
            # If action is back then set state to menu
            if action == "back":
                self.state = "menu"
            # This method sets the state of the action.
            if action == "play":
                self.state = "play"
            elif action == "how-to-play":
                self.state = "how-to-play"
            elif action == "exit":
                self.running = False

            # Handle the events from the play state
            if self.state == "play":
                self.handle_play_events(event)

    def handle_play_events(self, event):
        """
         Handle events that occur when the player plays. This is a bit tricky because we don't want to play the throw sound every time we start and end on a mouse click
         
         @param event - The Pygame event that
        """
        # This method is called when the mouse is pressed.
        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = pygame.mouse.get_pos()
            # If the mouse is collide with the mouse position
            if self.paper.rect.collidepoint(mouse_pos):
                self.throw_start = mouse_pos
        elif event.type == pygame.MOUSEBUTTONUP:
            # This method will play the throw.
            if self.throw_start is not None:
                throw_end = pygame.mouse.get_pos()
                self.paper.throw(self.throw_start, throw_end)
                self.throw_start = None
                self.sound_manager.play_sound("throw")

    def display_remaining_time(self, remaining_time):
        """
         Display the remaining time in the text. This is used to determine how long the user has left the game.
         
         @param remaining_time - The remaining time in seconds since the start
        """
        self.display_text(str(max(remaining_time, 0)), (10, 10), 74, (255, 0, 0))

    def display_text(self, text, position, size, color):
        """
         Display text on the screen. This is a convenience method for using pygame. font. Font to render the text and blit it to the screen
         
         @param text - The text to display.
         @param position - The position to display the text at. If you want to display a position that is outside the display it is necessary to use a tuple ( x y
         @param size
         @param color
        """
        """Display text on the screen at the given position."""
        font = pygame.font.Font(None, size)
        text_surface = font.render(text, True, color)
        self.display.blit(text_surface, position)

    def update_display(self):
        """
         Update the display based on the state of the papers. This is called every frame to update the display
        """
        self.display.blit(self.background, (0, 0))
        self.display.blit(self.grey_overlay, (0, 0))

        # Draw the game and the game.
        if self.state == "menu":
            self.menu.draw(self.display)
        elif self.state == "play":
            self.play_game()
            self.display_text(
                f"Level: {self.level}", (10, 80), 30, (255, 255, 255)
            )  
        elif self.state == 'how-to-play':
            self.display.fill((0, 0, 0))  
            instructions = [
                'How to Play:',
                '1. Click on the paper to start throwing.',
                '2. Drag the mouse in the direction you want to throw.',
                '3. Release the mouse button to throw the paper.',
                '4. Level up by throwing the paper into the correct bin.',
                '5. The time to complete each level decreases as you level up.',
                '6. The game ends when the time runs out.',

            ]
            # Draws the instructions in the font.
            for i, instruction in enumerate(instructions):
                text = self.font.render(instruction, True, (255, 255, 255))
                self.display.blit(text, (50, 50 + 40 * i))
            self.menu.draw_back_button(self.display) 

        elif self.state == "game_over":
            self.game_over()

        pygame.display.flip()

    def throw_paper(self, throw_end):
        """
         Throw a paper from throw_start to throw_end. This is equivalent to calling paper. throw ( throw_start throw_end )
         
         @param throw_end - The time to throw the paper from
        """
        self.paper.throw(self.throw_start, throw_end)

    def reset_game(self):
        """
         Reset the game to a blank state. This is called when the game is reset and should not be used
        """
        self.score = 0
        self.spawn_paper()
        self.start_time = pygame.time.get_ticks()

    def game_over(self):
        """
         Called when the game is over. This is the function that is called every second to display the game
        """
        self.display.blit(self.grey_overlay, (0, 0))
        font = pygame.font.Font(None, 74)

        # Render the text of the game
        if self.level >= 7:
            text = font.render("Amazing!", 1, (255, 0, 0))
        else:
            text = font.render("Game Over", 1, (255, 0, 0))
        self.display.blit(text, (250, 250))
        pygame.display.flip()
        pygame.time.wait(1000)
        self.reset_game()
        self.level = 1

        self.state = "menu"

    def play_game(self):
        """
         Draw and update sprites and game state. This is called every frame from the event loop and should not be called directly
        """
        self.bins.draw(self.display)
        self.all_sprites.update()
        self.all_sprites.draw(self.display)
        self.update_game_state()
    
    def check_in_bins(self):
        """
         Checks if we are in a bin and increases score if so. If it's the same type it spawns a
        """
        # This method is called by the game_over loop.
        for bin in self.bins:
            # This method is called when the game is over.
            if bin.opening.colliderect(self.paper.rect) and self.paper.velocity.y > 0:
                # This method is called when the bin is over or over.
                if bin.bin_type == self.paper.paper_type:
                    self.score += 1
                    self.sound_manager.play_sound("score")
                    self.spawn_paper()
                    self.level_up()
                else:
                    self.state = "game_over"
                break

    
    def spawn_bins(self):
        """
        Spawn binning sprites for this game. We're going to have a lot of bins in the game but it's easier
        """

        bin_positions = [150, 350, 550]
        random.shuffle(bin_positions)

        bin_types = [
            ("assets/cans/green-trash-can.png", 1),
            ("assets/cans/blue-trash-can.png", 2),
            ("assets/cans/red-trash-can.png", 3),
        ]

        self.bins = pygame.sprite.Group(
            Bin(image, position, 180, bin_type)
            for (image, bin_type), position in zip(bin_types, bin_positions)
        )


    def spawn_paper(self):
        """
        Spawn a paper and all sprites in it. This is called at the beginning of the game
        """

        paperball_assets = {
            "assets\paper\paperball-1.png": 1,
            "assets\paper\paperball-3.png": 3,
            "assets\paper\paperball-ip.png": 2,
        }

        selected_paperball, paper_type = random.choice(list(paperball_assets.items()))

        spritesheet = SpriteSheet(selected_paperball, 50, 60)

        self.spawn_bins()
        self.paper = Paper(spritesheet, 0, 3, 380, 500, 800, 600, paper_type)
        self.all_sprites = pygame.sprite.Group(self.paper)
        self.start_time = pygame.time.get_ticks()


# Run the game
game = Game()
game.run()
