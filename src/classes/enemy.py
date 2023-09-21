import pygame
import random
from classes.bag import Bag
import pygame
import random
from classes.item import InventoryBullet
from time import time

def enemy_constructor(x, y, enemy_type):
    if enemy_type == "basic":
        ai = BasicEnemyAI()
        enemy = Enemy(x, y, ai)
        return enemy

class Enemy(pygame.sprite.Sprite):
    def __init__(self, x, y, ai, loot_pool=None):
        super().__init__()
        self.image = pygame.image.load("../assets/images/zombie1.png")
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)
        self.health = 100
        self.malee_damage = 10
        self.speed = 2
        self.agro = False
        self.ai = ai
        self.dx = 0
        self.dy = 0
        self.loot_pool = [InventoryBullet("9mm-bullets", "../assets/images/9mm-inventory.png", 20)]
        self.last_position = self.rect.topleft

    def update(self, player_pos, map):
        self.ai.update(self, player_pos, map)
        if self.dx > 0:
            self.current_image = self.image
        else:
            self.current_image = pygame.transform.flip(self.image, True, False)
        if self.health <= 0:
            return self.die(map)

    def draw(self, surface):
        surface.blit(self.current_image, self.rect)
        pygame.draw.rect(surface, (255, 0, 0), self.rect, 2)
    
    def die(self, map):
        self.drop_loot(map)
        self.kill()

    def drop_loot(self, map):
        bag = Bag(self.rect.x, self.rect.y, self.loot_pool)
        map.loot_bags.add(bag)
    
    def take_damage(self, bullet):
        self.health -= bullet.damage
        dx = bullet.rect.x - self.rect.x
        dy = bullet.rect.y - self.rect.y
        distance = (dx**2 + dy**2)**0.5
        if distance > 0:
            dx /= distance
            dy /= distance
        self.rect.x -= dx * 10
        self.rect.y -= dy * 10
    def is_in_zone(self, zones):
        for zone in zones:
            if self.rect.colliderect(zone.x, zone.y, zone.width, zone.height):
                return True
        return False


class BasicEnemyAI:
    def __init__(self, aggro_distance=200):
        self.aggro_distance = aggro_distance
        self.target_x = None
        self.target_y = None
        self.last_time_moved = time()
        self.wait_time = 1
        self.max_wait_time = 2

    def update(self, enemy, player_pos, map):
        zones = map.zones
        dx, dy = player_pos[0] - enemy.rect.x, player_pos[1] - enemy.rect.y
        distance = (dx**2 + dy**2)**0.5

        if distance < self.aggro_distance:
            enemy.agro = True

        if enemy.agro:
            self.move_towards_player(enemy, dx, dy, distance)
        else:
            
            if self.target_x is None or self.target_y is None or time() - self.last_time_moved > self.max_wait_time:
                print("not agro")
                self.choose_random_point(enemy)
                return
        
            if time() - self.last_time_moved < self.wait_time:
                return

            self.move_toward_point(enemy)

            if enemy.rect.x == self.target_x and enemy.rect.y == self.target_y:
                self.choose_random_point(enemy)

        if not enemy.is_in_zone(zones["walkable"]) or enemy.is_in_zone(zones["unwalkable"]) or enemy.is_in_zone(zones["wall"]):
            # If outside walkable area, revert the position
            enemy.rect.topleft = enemy.last_position

    def move_towards_player(self, enemy, dx, dy, distance):
        enemy.last_position = enemy.rect.topleft
        if distance > 0:
            enemy.rect.x += enemy.speed * dx / distance
            enemy.rect.y += enemy.speed * dy / distance
        enemy.dx = dx
        enemy.dy = dy

    def move_toward_point(self, enemy):
        enemy.last_position = enemy.rect.topleft
        dx, dy = self.target_x - enemy.rect.x, self.target_y - enemy.rect.y
        enemy.dx = dx
        enemy.dy = dy
        distance = (dx**2 + dy**2)**0.5
        if distance > 0:
            enemy.rect.x += enemy.speed * dx / distance
            enemy.rect.y += enemy.speed * dy / distance

    def choose_random_point(self, enemy):
        self.target_x = enemy.rect.x + random.randint(-30, 30)
        self.target_y = enemy.rect.y + random.randint(-30, 30)
        self.last_time_moved = time()
        self.wait_time = random.uniform(0.5, self.wait_time)  # pause for 0.5 to 2 seconds before moving again

