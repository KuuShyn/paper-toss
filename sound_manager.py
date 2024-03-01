import pygame

class SoundManager:
    def __init__(self):
        pygame.mixer.init()  # Initialize the mixer module for Sound loading and playback
        self.sounds = {}  # Dictionary to store sounds

    def load_sound(self, name, file_path):
        """
        Load a sound from a file and store it in the sounds dictionary.
        :param name: The name to associate with the sound
        :param file_path: The path to the sound file
        """
        self.sounds[name] = pygame.mixer.Sound(file_path)  # Load the sound and store it in the dictionary

    def play_sound(self, name):
        """
        Play a sound by its name.
        :param name: The name of the sound to play
        """
        if name in self.sounds:  # Check if the sound is in the dictionary
            self.sounds[name].play()  # Play the sound

    def play_bgm(self, file_path):
        """
        Play a BGM (Background Music) from a file.
        :param file_path: The path to the music file
        """
        pygame.mixer.music.load(file_path)  # Load the music
        pygame.mixer.music.play(-1)  # Play the music indefinitely