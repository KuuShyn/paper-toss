import pygame


class Bin(pygame.sprite.Sprite):
    def __init__(self, image_path, x, y, bin_type):
        super().__init__()
        self.image = pygame.image.load(image_path)
        self.rect = self.image.get_rect()
        self.bin_type = bin_type

        # Calculate the new height while keeping the aspect ratio
        aspect_ratio = self.rect.height / self.rect.width
        new_width = 100
        new_height = int(new_width * aspect_ratio)

        # Resize the image
        self.image = pygame.transform.scale(self.image, (new_width, new_height))

        self.rect = self.image.get_rect()  # Update the rectangle to match the new image size
        self.rect.topleft = (x, y)

        # Create a rectangle for the opening of the bin
        opening_width = self.rect.width * 0.6  # Make the opening 60% of the bin's width
        opening_x = x + self.rect.width * 0.2  # Center the opening on the bin
        self.opening = pygame.Rect(opening_x, 230, opening_width, 5)  # Adjust the size as needed
