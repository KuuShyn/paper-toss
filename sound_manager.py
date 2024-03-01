import pygame

class SoundManager:
    def __init__(self):
        pygame.mixer.init()  
        self.sounds = {}

    def load_sound(self, name, file_path):
        """Load a sound from a file and store it in the sounds dictionary."""
        self.sounds[name] = pygame.mixer.Sound(file_path)

    def play_sound(self, name):
        """Play a sound by its name."""
        if name in self.sounds:
            self.sounds[name].play()

    def play_bgm(self, file_path):
        """Play a BGM from a file."""
        pygame.mixer.music.load(file_path)
        pygame.mixer.music.play(-1) 