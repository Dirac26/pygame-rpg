import pygame
import math

class Bullet(pygame.sprite.Sprite):
    def __init__(self, damage, speed, image_path):
        super().__init__()

        # Assuming you want a simple rectangle for the bullet, otherwise you can load an image
        self.original_image = pygame.image.load(image_path)
        self.image = self.original_image.copy()
        self.rect = self.image.get_rect()
        self.dx = 1
        self.y = 0
        self.damage = damage
        self.speed = speed


    def update(self):
        length = math.sqrt(self.dx**2 + self.dy**2)
        if length > 0:
            self.dx /= length
            self.dy /= length

        self.rect.x += self.dx * self.speed
        self.rect.y += self.dy * self.speed

        # Remove bullet if it goes off-screen (for optimization)
        if self.rect.bottom < 0:
            self.kill()

    def rotate_based_on_direction(self):
        angle = math.atan2(self.dy, self.dx)
        degree_angle = math.degrees(angle)
        self.image = pygame.transform.rotate(self.original_image, -degree_angle)
        old_center = self.rect.center
        self.rect = self.image.get_rect()
        self.rect.center = old_center
        
    def draw(self, surface):
        surface.blit(self.image, self.rect)
        pygame.draw.rect(surface, (255, 0, 0), self.rect, 2)