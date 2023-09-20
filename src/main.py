import pygame
from time import sleep
from pytmx.util_pygame import load_pygame
from classes.player import Player, bullets
from classes.hud import HUD
from classes.map import Map

pygame.init()

SCREEN_WIDTH = 1200
SCREEN_HEIGHT = 800

pygame.font.init()
WHITE = (255, 255, 255)

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("RPG")
clock = pygame.time.Clock()

player = Player()
hud = HUD(player)
bags = pygame.sprite.Group()
interactables = []

map = Map("../maps/map_1.tmx")
player.init_map(map, 1)

running = True

spawn_point = map.get_spawn_point(0)
player.move_to(spawn_point[0], spawn_point[1])

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
        player.inventory.update(events, player)
        player.inventory.draw(screen)
        pygame.display.flip()
        clock.tick(60)



while running:
    clock.tick(60)
    dt = 1/60.0 
    events = pygame.event.get()
    for event in events:
        if event.type == pygame.QUIT:
            running = False
    
    if player.inventory.active:
        inventory_loop()
        sleep(.2)
    
    player.update(events, dt)
    map = player.current_map
    player.gun.update()
    player.check_for_bags(bags)
    player.inventory.logger.update()
    bullets.update()
    screen.fill(WHITE)
    player.current_map.draw(screen)
    hud.draw(screen)
    player.inventory.logger.draw(screen)
    player.draw(screen)

    for bullet in bullets:
        bullet.draw(screen)
    for bag in bags:
        bag.draw(screen)
    for interactable in map.interactables:
        interactable.draw(screen)

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
