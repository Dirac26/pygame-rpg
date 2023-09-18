import pygame

class Bullet(pygame.sprite.Sprite):
    def __init__(self, damage, speed, image_path):
        super().__init__()

        # Assuming you want a simple rectangle for the bullet, otherwise you can load an image
        self.original_image = pygame.image.load(image_path)
        self.image = self.original_image.copy()
        self.rect = self.image.get_rect()

        self.damage = damage
        self.speed = speed


    def update(self):
        if self.direction == 'up':
            self.rect.y -= self.speed
        elif self.direction == 'down':
            self.rect.y += self.speed
        elif self.direction == 'left':
            self.rect.x -= self.speed
        elif self.direction == 'right':
            self.rect.x += self.speed

        # Remove bullet if it goes off-screen (for optimization)
        if self.rect.bottom < 0:
            self.kill()
    def rotate_based_on_direction(self):
        if self.direction == "up":
            angle = 270
        elif self.direction == "right":
            angle = 0
        elif self.direction == "down":
            angle = 90
        elif self.direction == "left":
            angle = 180
        self.image = pygame.transform.rotate(self.original_image, -angle)
        old_center = self.rect.center
        self.rect = self.image.get_rect()
        self.rect.center = old_center
        
    def draw(self, surface):
        surface.blit(self.image, self.rect)
        pygame.draw.rect(surface, (255, 0, 0), self.rect, 2)