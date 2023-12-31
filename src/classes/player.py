import pygame
from classes.gun import Gun
from classes.inventory import Inventory
from classes.item import InventoryGun
from classes.status_effects import SlowEffect, DamageEffect
from classes.map import Map
import math

class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        #position and ui
        self.image = pygame.image.load("./assets/images/main-player-1.png")
        self.rect = self.image.get_rect()
        self.rect.x = 1100
        self.rect.y = 100
        self.dx = 1
        self.dy = 0
        self.last_position = self.rect.topleft
        self.last_shot_time = pygame.time.get_ticks()

        #maps, weapons, and inventory
        self.inventory = Inventory()
        self.active_weapon = None
        self.active_melee_weapon = None
        self.head_armor = None
        self.chest_armor = None
        self.leg_armor = None
        self.boots_armor = None
        self.maps = {}
        self.gold = 0
        self.current_map = None

        #stats
        self.health = 100
        self.max_speed = 5
        self.speed = 5

        self.malee_damage = 1
        self.status_effects = []

        self.in_dialog = False
        self.current_dialog = None
        self.active_quests = []
        self.finished_quests = []
        self.old_dialogs = []
        self.kill_counts = {
            "zombie": 0, 
        }
        self.quest_view = None
        self.is_attacking = False
        self.attack_timer = 0



    def init_map(self, map, map_id):
        self.maps[map_id] = map
        self.current_map = map

    def add_to_inventory(self, item):
        self.inventory.add_item(item)

    def transition_to_map(self, map_id):
        last_map_id = self.current_map.map_id
        new_map = Map(f"./maps/map_{map_id}.tmx") if map_id not in self.maps else self.maps[map_id]
        self.maps[map_id] = new_map
        spwan_x, spawn_y = new_map.get_spawn_point(last_map_id)
        self.current_map = new_map
        self.move_to(spwan_x, spawn_y)

    def set_gun(self, inv_gun):
        self.active_weapon = inv_gun
        inv_gun.item_object.inventory = self.inventory
    
    def set_melee(self, inv_melee):
        self.active_melee_weapon = inv_melee

    def set_in_dialog(self, in_dialog):
        self.current_dialog = in_dialog
        self.in_dialog = True

    def dialog_finished(self):
        self.in_dialog = False
        self.old_dialogs.append(self.current_dialog)
        self.current_dialog = None

    def add_quest(self, quest):
        self.active_quests.append(quest)
        quest.get_active_objective().assign_player(self)

    def handle_movment(self, keys):
        move_left = keys[pygame.K_LEFT] or keys[pygame.K_a]
        move_right = keys[pygame.K_RIGHT] or keys[pygame.K_d]
        move_up = keys[pygame.K_UP] or keys[pygame.K_w]
        move_down = keys[pygame.K_DOWN] or keys[pygame.K_s]

        dx, dy = 0, 0
        if move_left:
            dx -= 1
            self.last_position = self.rect.topleft
        if move_right:
            dx += 1
            self.last_position = self.rect.topleft
        if move_up:
            dy -= 1
            self.last_position = self.rect.topleft
        if move_down:
            dy += 1
            self.last_position = self.rect.topleft

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

        #continus movement
        keys = pygame.key.get_pressed()
        self.handle_movment(keys)
            
        if not self.is_in_zone(zones["walkable"]) or self.is_in_zone(zones["unwalkable"]) or self.is_in_zone(zones["wall"]):
            # If outside walkable area, revert the position
            self.rect.topleft = self.last_position
        

        self.near_interactable = self.check_near_interactable(interactables)
        mouse_buttons = pygame.mouse.get_pressed()
        #single pressed button
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_i:
                    self.inventory.active = True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_j:
                    self.quest_view.active = True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    self.active_weapon.item_object.start_reload(self.inventory)
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_e and self.near_interactable:
                    self.near_interactable.interact(player=self)
            if mouse_buttons[0]:
                mouse_x, mouse_y = pygame.mouse.get_pos()
                self.shoot(mouse_x, mouse_y)
            if mouse_buttons[2]: 
                mouse_x, mouse_y = pygame.mouse.get_pos()
                self.melee_attack(mouse_x, mouse_y)        
        self.handle_zones()

        for status in self.status_effects:
            status.update(dt)
            status.effect(self)

        for quest in self.active_quests:
            quest.update(self)
        
        self.check_enemy_collision(self.current_map.enemies)
    
    def shoot(self, target_x, target_y):
        if self.active_weapon is None:
            return
        current_time = pygame.time.get_ticks()
        dx = target_x - self.rect.x
        dy = target_y - self.rect.y
        if current_time - self.last_shot_time >= self.active_weapon.item_object.fire_rate:
            bullets = self.active_weapon.item_object.shoot(self.rect.centerx, self.rect.centery, dx, dy, self.inventory)
            if bullets:
                for bullet in bullets:
                    self.current_map.active_player_bullets.add(bullet)
                    self.last_shot_time = current_time
    
    def melee_attack(self, target_x, target_y):
        current_time = pygame.time.get_ticks()
        if self.active_melee_weapon is None:
            return
        if current_time - self.active_melee_weapon.item_object.last_swing_time < self.active_melee_weapon.item_object.swing_cooldown:
            return

        self.active_melee_weapon.item_object.swing(self.rect.centerx, self.rect.centery, target_x, target_y)

    def check_for_bags(self, bags):
        hits = pygame.sprite.spritecollide(self, bags, False)
        for bag in hits:
            bag.collect(self)

    def check_enemy_collision(self, enemies):
        for enemy in enemies:
            if self.rect.colliderect(enemy.rect):
                self.take_damage(enemy.melee_damage, enemy.knockback_distance, enemy.rect.x, enemy.rect.y)

    def take_damage(self, damage, knockback_distance, x, y):
        self.health -= damage
        dx = x - self.rect.x
        dy = x - self.rect.y
        distance = (dx**2 + dy**2)**0.5
        if distance > 0:
            dx /= distance
            dy /= distance
        self.rect.x -= dx * knockback_distance
        self.rect.y -= dy * knockback_distance

    def draw(self, surface):
        surface.blit(self.image, self.rect)
        pygame.draw.rect(surface, (255, 0, 0), self.rect, 2)
        # pygame.draw.circle(surface, (255, 0, 0), (self.rect.centerx, self.rect.centery), 20)
    
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