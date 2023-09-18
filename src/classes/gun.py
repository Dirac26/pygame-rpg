import pygame
from classes.bullet import Bullet

class Gun:
    def __init__(self, type):
        self.type = type
        
        if self.type == "pistol":
            self.bullet_damage = 10
            self.bullet_speed = 10
            self.bullet_image = '../assets/images/9mm-ingame.png'
            self.inventory_image = pygame.image.load('../assets/images/9mm-ingame.png')
            self.game_image = pygame.image.load('../assets/images/9mm-ingame.png')
            self.clip_size = 10
            self.current_ammo = 10
            self.fire_rate = 500

        elif self.type == "machine_gun":
            self.bullet_damage = 5
            self.bullet_speed = 15
            self.bullet_image = '../assets/images/9mm-ingame.png'
            self.inventory_image = pygame.image.load('../assets/images/9mm-ingame.png')
            self.game_image = pygame.image.load('../assets/images/9mm-ingame.png')
            self.clip_size = 30
            self.current_ammo = 30
            self.fire_rate = 100

    def create_bullet(self, x, y, direction):
        bullet = Bullet(self.bullet_damage, self.bullet_speed, self.bullet_image)
        bullet.rect.x = x
        bullet.rect.y = y
        bullet.direction = direction
        self.current_ammo -= 1
        bullet.rotate_based_on_direction()
        return bullet