import pygame

class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((32, 32))
        self.image.fill((255, 0, 0))
        self.rect = self.image.get_rect()
        self.rect.center = (400, 300)

    def update(self):
        pass

    def draw(self, surface):
        surface.blit(self.image, self.rect)