import pygame
from time import sleep
from classes.player import Player
from classes.hud import HUD
from classes.map import Map
from classes.quest_view import QuestView

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
interactables = []

map = Map("./maps/map_1.tmx")
player.init_map(map, 1)

running = True

spawn_point = map.get_spawn_point(0)
player.move_to(spawn_point[0], spawn_point[1])

quest_view = QuestView()
player.quest_view = quest_view

def check_bullet_collision(bullets, targets):
    for bullet in bullets:
        hit_list = pygame.sprite.spritecollide(bullet, targets, False)
        for target in hit_list:
            bullet.kill()
            target.take_damage(bullet.damage, bullet.knockback_distance, bullet.rect.x, bullet.rect.y)

def dialog_loop():
    running = True
    dialog = player.current_dialog
    while running:
        dialog.update(events)
        if dialog.finished:
            player.dialog_finished()
            running = False
        dialog.draw(screen)
        pygame.display.flip()
        clock.tick(60)

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
        screen.fill((220, 220, 220))
        player.inventory.draw(screen)
        pygame.display.flip()
        clock.tick(60)

def quest_view_loop():
    running = True
    while running:
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_j:
                    player.quest_view.active = False
                    running = False
                    break
        player.quest_view.update(events, player)
        screen.fill((220, 220, 220))
        player.quest_view.draw(screen)
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

    if player.quest_view.active:
        quest_view_loop()
        sleep(.2)

    if player.in_dialog:
        dialog_loop()
        sleep(.2)
    
    player.update(events, dt)
    map = player.current_map
    if player.active_weapon:
        player.active_weapon.item_object.update(player.inventory)
    if player.active_melee_weapon:
        player.active_melee_weapon.item_object.update(dt, player.rect.centerx, player.rect.centery, map.enemies)
    player.check_for_bags(map.loot_bags)
    player.inventory.logger.update()
    map.active_player_bullets.update()
    map.active_enemy_bullets.update()
    check_bullet_collision(map.active_player_bullets, map.enemies)
    check_bullet_collision(map.active_enemy_bullets, [player])

    map.enemies.update(player, map)
    screen.fill(WHITE)
    player.current_map.draw(screen)
    hud.draw(screen)
    player.inventory.logger.draw(screen)
    player.draw(screen)
    
    if player.active_melee_weapon:
        player.active_melee_weapon.item_object.draw(screen)
    for bullet in map.active_player_bullets:
        bullet.draw(screen)
    for bullet in map.active_enemy_bullets:
        bullet.draw(screen)
    for bag in map.loot_bags:
        bag.draw(screen)
    for interactable in map.interactables:
        interactable.draw(screen)
    for enemy in map.enemies:
        enemy.draw(screen)

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
