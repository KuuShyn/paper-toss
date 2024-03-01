import pygame


class SpriteSheet:
    def __init__(self, filename, sprite_width, sprite_height):
        self.spritesheet = pygame.image.load(filename).convert_alpha()  # Use convert_alpha() instead of convert()
        self.sprite_width = sprite_width
        self.sprite_height = sprite_height

    def get_image(self, row, col):
        x = col * self.sprite_width
        y = row * self.sprite_height
        return self.get_sprite(x, y, self.sprite_width, self.sprite_height)

    def get_sprite(self, x, y, width, height):
        sprite = pygame.Surface((width, height), pygame.SRCALPHA)  # Create a surface with an alpha channel
        sprite.blit(self.spritesheet, (0, 0), (x, y, width, height))
        return sprite