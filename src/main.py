import pygame
from classes.player import Player

pygame.init()

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

WHITE = (255, 255, 255)

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("RPG")
clock = pygame.time.Clock()

player = Player()

running = True

while running:
    clock.tick(60)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    player.update()

    screen.fill(WHITE)
    player.draw(screen)
    pygame.display.flip()
    clock.tick(60)

pygame.quit()
