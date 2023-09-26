import pygame

class Bag(pygame.sprite.Sprite):
    def __init__(self, x, y, contents):
        super().__init__()
        self.image = pygame.image.load("./assets/images/bundle.png")
        self.rect = self.image.get_rect(topleft=(x, y))
        self.contents = contents

    def collect(self, player):
        for item in self.contents:
            player.inventory.add_item(item)
        self.kill()
    
    def draw(self, surface):
        surface.blit(self.image, self.rect)
        pygame.draw.rect(surface, (255, 0, 0), self.rect, 2)