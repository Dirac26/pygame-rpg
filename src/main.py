import pygame
from classes.player import Player, bullets
from time import sleep

pygame.init()

SCREEN_WIDTH = 1200
SCREEN_HEIGHT = 800

WHITE = (255, 255, 255)

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("RPG")
clock = pygame.time.Clock()

player = Player()

running = True

def inventory_loop():
    running = True
    while running:
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_i:
                    player.inventory.active = False
                    running = False
                    break
                if event.type == pygame.QUIT:
                    running = False
        player.inventory.update(events)
        player.inventory.draw(screen)
        pygame.display.flip()
        clock.tick(60)

while running:
    clock.tick(60)
    events = pygame.event.get()
    for event in events:
        if event.type == pygame.QUIT:
            running = False
    if player.inventory.active:
        inventory_loop()
        sleep(1)
    player.update(events)
    bullets.update()
    screen.fill(WHITE)
    player.draw(screen)
    for bullet in bullets:
        bullet.draw(screen)
    
    pygame.display.flip()
    clock.tick(60)

pygame.quit()
