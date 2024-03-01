import pygame


class Bin(pygame.sprite.Sprite):
    def __init__(self, image_path, x, y, bin_type):
        super().__init__()
        self.image = pygame.image.load(image_path)
        self.rect = self.image.get_rect()
        self.bin_type = bin_type

        aspect_ratio = self.rect.height / self.rect.width
        new_width = 100
        new_height = int(new_width * aspect_ratio)

        self.image = pygame.transform.scale(self.image, (new_width, new_height))

        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)

        opening_width = self.rect.width * 0.6
        opening_x = x + self.rect.width * 0.2
        self.opening = pygame.Rect(opening_x, 230, opening_width, 5)
