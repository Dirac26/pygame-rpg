import pygame
from classes.gun import Gun
from classes.inventory import Inventory
from classes.item import InventoryGun
from classes.status_effects import SlowEffect, DamageEffect
from classes.map import Map
import math

bullets = pygame.sprite.Group()

class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load("../assets/images/main-player-1.png")
        self.rect = self.image.get_rect()
        self.rect.x = 1100
        self.rect.y = 100
        self.inventory = Inventory()
        self.init_inventory()
        self.max_speed = 5
        self.speed = 5
        self.last_direction = 'left'
        self.last_shot_time = pygame.time.get_ticks()
        self.health = 100
        self.gold = 0
        self.status_effects = []
        self.maps = {}
        self.dx = 1
        self.dy = 0
        self.current_map = None

    def init_map(self, map, map_id):
        self.maps[map_id] = map
        self.current_map = map

    def add_to_inventory(self, item):
        self.inventory.add_item(item)

    def transition_to_map(self, map_id):
        print(self.maps)
        last_map_id = self.current_map.map_id
        new_map = Map(f"../maps/map_{map_id}.tmx") if map_id not in self.maps else self.maps[map_id]
        self.maps[map_id] = new_map
        spwan_x, spawn_y = new_map.get_spawn_point(last_map_id)
        self.current_map = new_map
        self.move_to(spwan_x, spawn_y)

    def init_inventory(self):
        self.gun = Gun("pistol", self.inventory)
        self.active_gun = InventoryGun("pistol", "../assets/images/glock-inventory.png", self.gun)
        self.inventory.add_item(self.active_gun)
        self.inventory.active_gun = self.inventory.items[0] 

    def handle_movment(self, keys):
        move_left = keys[pygame.K_LEFT] or keys[pygame.K_a]
        move_right = keys[pygame.K_RIGHT] or keys[pygame.K_d]
        move_up = keys[pygame.K_UP] or keys[pygame.K_w]
        move_down = keys[pygame.K_DOWN] or keys[pygame.K_s]

        dx, dy = 0, 0
        if move_left:
            dx -= 1
        if move_right:
            dx += 1
        if move_up:
            dy -= 1
        if move_down:
            dy += 1

        length = math.sqrt(dx**2 + dy**2)
        if length > 0:
            dx /= length
            dy /= length

        if dx != 0 or dy != 0:
            self.dx = dx
            self.dy = dy
            self.rect.x += dx * self.speed
            self.rect.y += dy * self.speed

    def update(self, events, dt):
        zones = self.current_map.zones
        interactables = self.current_map.interactables

        last_position = self.rect.topleft
        #continus movement
        keys = pygame.key.get_pressed()
        self.handle_movment(keys)
        if keys[pygame.K_SPACE]:
            self.shoot()
            
        if not self.is_in_zone(zones["walkable"]) or self.is_in_zone(zones["unwalkable"]) or self.is_in_zone(zones["wall"]):
            # If outside walkable area, revert the position
            self.rect.topleft = last_position
        

        self.near_interactable = self.check_near_interactable(interactables)

        #single pressed button
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_i:
                    self.inventory.active = True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    self.gun.start_reload()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_e and self.near_interactable:
                    self.near_interactable.interact(player=self)
        
        self.handle_zones()

        for status in self.status_effects:
            status.update(dt)
            status.effect(self)
            
    def shoot(self):
        current_time = pygame.time.get_ticks()
        if current_time - self.last_shot_time >= self.gun.fire_rate:
            bullet = self.gun.shoot(self.rect.centerx, self.rect.centery, self.dx, self.dy)
            if bullet:
                bullets.add(bullet)
                self.last_shot_time = current_time
    
    def check_for_bags(self, bags):
        hits = pygame.sprite.spritecollide(self, bags, False)
        for bag in hits:
            bag.collect(self)

    def draw(self, surface):
        surface.blit(self.image, self.rect)
        pygame.draw.rect(surface, (255, 0, 0), self.rect, 2)
    
    def apply_status(self, status):
        # Check if the status effect is already active
        for s in self.status_effects:
            if s.name == status.name:
                s.activate()
                return

        # If not, add and activate it
        self.status_effects.append(status)
        status.activate()

    def is_in_zone(self, zones):
        for zone in zones:
            if self.rect.colliderect(zone.x, zone.y, zone.width, zone.height):
                return True
        return False

    def handle_zones(self):
        zones = self.current_map.zones
        for zone in zones["slow"]:
            if self.rect.colliderect(zone.x, zone.y, zone.width, zone.height):
                self.apply_status(SlowEffect(.1, .8))
        for zone in zones["damage"]:
            if self.rect.colliderect(zone.x, zone.y, zone.width, zone.height):
                self.apply_status(DamageEffect(.1, 5))
                self.apply_status(SlowEffect(.1, .4))

    def check_near_interactable(self, interactables):
        for interactable in interactables:
            if self.rect.colliderect(interactable.rect) and interactable.can_interact():
                return interactable
        return None
    
    def move_to(self, x, y):
        self.rect.x = x
        self.rect.y = y