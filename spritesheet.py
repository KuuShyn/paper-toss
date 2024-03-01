import pygame

class SpriteSheet:
    def __init__(self, filename, sprite_width, sprite_height):
        # Load the spritesheet image and convert it to a format suitable for fast blitting
        self.spritesheet = pygame.image.load(filename).convert_alpha()
        # Store the width and height of each sprite
        self.sprite_width = sprite_width
        self.sprite_height = sprite_height

    def get_image(self, row, col):
        # Calculate the x and y coordinates for the sprite based on its row and column
        x = col * self.sprite_width
        y = row * self.sprite_height
        # Return the sprite at the calculated coordinates
        return self.get_sprite(x, y, self.sprite_width, self.sprite_height)

    def get_sprite(self, x, y, width, height):
        # Create a new surface with the same dimensions as the sprite
        sprite = pygame.Surface((width, height), pygame.SRCALPHA)
        # Blit the sprite from the spritesheet onto the new surface
        sprite.blit(self.spritesheet, (0, 0), (x, y, width, height))
        # Return the new surface containing the sprite
        return sprite