import pygame
from classes.bullet import Bullet

class Gun:
    def __init__(self, type, inventory):
        self.type = type
        self.reloading = False
        self.reload_start_time = None
        self.inventory = inventory
        
        if self.type == "pistol":
            self.bullet_damage = 10
            self.bullet_speed = 10
            self.bullet_image = '../assets/images/9mm-ingame.png'
            self.game_image = pygame.image.load('../assets/images/9mm-ingame.png')
            self.clip_size = 10
            self.current_ammo = 10
            self.fire_rate = 500
            self.reload_time = 5000
            self.bullet_name = "9mm-bullets"


        elif self.type == "machine_gun":
            self.bullet_damage = 5
            self.bullet_speed = 15
            self.bullet_image = '../assets/images/9mm-ingame.png'
            self.game_image = pygame.image.load('../assets/images/9mm-ingame.png')
            self.clip_size = 30
            self.current_ammo = 30
            self.fire_rate = 100
            self.reload_time = 5000
            self.bullet_name = "9mm-bullets"

    def shoot(self, x, y, direction):
        if not self.reloading and self.current_ammo > 0:
            # Actual shooting mechanics
            self.current_ammo -= 1
            bullet = self.create_bullet(x, y, direction)
            if self.current_ammo == 0:
                self.start_reload()
            return bullet

    def create_bullet(self, x, y, direction):
        bullet = Bullet(self.bullet_damage, self.bullet_speed, self.bullet_image)
        bullet.rect.x = x
        bullet.rect.y = y
        bullet.direction = direction
        self.current_ammo -= 1
        bullet.rotate_based_on_direction()
        return bullet
    
    def start_reload(self):
        self.bullet_inventory_object = self.inventory.get_item("9mm-bullets")
        if not self.reloading and self.bullet_inventory_object and self.bullet_inventory_object.count > 0:
            self.reloading = True
            self.reload_start_time = pygame.time.get_ticks()

    def finish_reload(self):
        # Determine how many bullets are transferred from stored_ammo to current_ammo
        transfer_ammo = min(self.bullet_inventory_object.count, self.clip_size)
        self.current_ammo += transfer_ammo
        self.bullet_inventory_object.count -= transfer_ammo
        self.reloading = False

    def update(self):
        if self.reloading:
            if pygame.time.get_ticks() - self.reload_start_time > self.reload_time:
                self.finish_reload()