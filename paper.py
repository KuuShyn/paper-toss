import math
import pygame

class Paper(pygame.sprite.Sprite):
    def __init__(self, spritesheet, row, num_sprites, x, y, screen_width, screen_height, paper_type):
        super().__init__()
        self.images = [spritesheet.get_image(row, col) for col in range(num_sprites)]
        self.index = 0
        self.image = self.images[self.index]
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)
        self.timer = pygame.time.get_ticks()
        self.gravity = pygame.Vector2(0, 0.09) 
        self.air_resistance = 0.006 
        self.velocity = pygame.Vector2(0, 0)
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.paper_type = paper_type

    def update(self):
        if pygame.time.get_ticks() - self.timer > 120: 
            self.index = (self.index + 1) % len(self.images)
            self.image = self.images[self.index]
            self.timer = pygame.time.get_ticks()

        self.velocity += self.gravity  
        self.velocity *= (1 - self.air_resistance)  
        self.rect.topleft += self.velocity 

        if self.rect.left < 0:
            self.velocity.x *= -0.5  
            self.rect.left = 0  # 
        elif self.rect.right > 800:
            self.velocity.x *= -1 
            self.rect.right = self.screen_width  
        if self.rect.top < 0:
            self.velocity.y *= -0.5 
            self.rect.top = 0 
        elif self.rect.bottom > self.screen_height:
            self.velocity.y *= -0.5 
            self.rect.bottom = self.screen_height  

    def throw(self, start_pos, end_pos):
        
        dx = end_pos[0] - start_pos[0]
        dy = start_pos[1] - end_pos[1]
        distance = math.hypot(dx, dy)
        angle = math.atan2(dy, dx)

        speed = distance * 0.02 
        self.velocity.x = math.cos(angle) * speed
        self.velocity.y = -math.sin(angle) * speed 

    def draw_rect(self, surface):
        pygame.draw.rect(surface, (255, 0, 0), self.rect, 2) 