import pygame

class Bin(pygame.sprite.Sprite):
    def __init__(self, image_path, x, y, bin_type):
        super().__init__()  # Call the parent class (Sprite) constructor
        self.image = pygame.image.load(image_path)  # Load the image for the bin
        self.rect = self.image.get_rect()  # Get the rectangle for the image
        self.bin_type = bin_type  # Set the type of the bin

        # Calculate the aspect ratio of the image
        aspect_ratio = self.rect.height / self.rect.width
        new_width = 100  # Define the new width
        new_height = int(new_width * aspect_ratio)  # Calculate the new height based on the aspect ratio

        # Scale the image to the new width and height
        self.image = pygame.transform.scale(self.image, (new_width, new_height))

        self.rect = self.image.get_rect()  # Get the rectangle for the scaled image
        self.rect.topleft = (x, y)  # Position the rectangle at the given coordinates

        # Define the opening of the bin where the paper should go in
        opening_width = self.rect.width * 0.6  # The opening is 60% of the bin width
        opening_x = x + self.rect.width * 0.2  # The opening starts at 20% of the bin width
        self.opening = pygame.Rect(opening_x, 230, opening_width, 5)  # Create the rectangle for the opening