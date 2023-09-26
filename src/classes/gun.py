import pygame
from classes.bullet import Bullet
from classes.shooting_style import ShootingStyle, PistolStyle, ShotgunStyle

class Gun:
    def __init__(self, name, bullet_name, bullet_damage, bullet_speed,
                 bullet_image_path, clip_size, current_ammo, reload_time, fire_rate, bullet_distance,
                 knockback_distance, sound_file, reload_sound_file):
        self.name = name
        self.bullet_name = bullet_name
        self.bullet_damage = bullet_damage
        self.bullet_speed = bullet_speed
        self.bullet_image = bullet_image_path
        self.clip_size = clip_size
        self.current_ammo = current_ammo
        self.reload_time = reload_time
        self.reloading = False
        self.reload_start_time = 0
        self.bullet_inventory_object = None
        self.fire_rate = fire_rate
        self.bullet_distance = bullet_distance
        self.shots_per_click = 1
        self.knockback_distance = knockback_distance
        self.shoot_sound = pygame.mixer.Sound(sound_file)
        self.reload_sound = pygame.mixer.Sound(reload_sound_file)
        self.shoot_sound.set_volume(0.1)
        self.reload_sound.set_volume(0.1)


    def shoot(self, x, y, dx, dy, inventory):
        if not self.reloading and self.current_ammo > 0:
            # Actual shooting mechanics
            self.current_ammo -= self.shots_per_click
            bullet = self.shooting_style.shoot(x, y, dx, dy)
            self.shoot_sound.play()
            if self.current_ammo <= 0:
                self.start_reload(inventory)
            return bullet

    @classmethod
    def from_data(cls, data):
        obj = cls(data['name'],
                   data['bullet_name'],
                   data['bullet_damage'],
                   data['bullet_speed'],
                   data['bullet_image_path'],
                   data['clip_size'],
                   data['current_ammo'],
                   data['reload_time'],
                   data['fire_rate'],
                   data['bullet_distance'],
                   data['knockback_distance'],
                   data['shoot_sound'],
                   data['reload_sound']
                   )
        if data["shooting_style"] == 'automatic':
            obj.shooting_style = PistolStyle(data['bullet_damage'],
                                             data['bullet_speed'],
                                             data['bullet_distance'],
                                             data['bullet_image_path'],
                                             data['knockback_distance']
                                            )
        elif data["shooting_style"] == 'shotgun':
            obj.shooting_style = ShotgunStyle(data['bullet_damage'],
                                              data['bullet_speed'],
                                              data['bullet_distance'],
                                              data['bullet_image_path'],
                                              data['knockback_distance']
                                             )
        return obj
    
    def start_reload(self, inventory):
        bullet_inventory_object = inventory.get_item(self.bullet_name)
        if not self.reloading and bullet_inventory_object and bullet_inventory_object.count > 0:
            self.reloading = True
            self.reload_start_time = pygame.time.get_ticks()
            self.reload_sound.play()

    def finish_reload(self, inventory):
        bullet_inventory_object = inventory.get_item(self.bullet_name)
        needed_ammo = self.clip_size - self.current_ammo
        transfer_ammo = min(bullet_inventory_object.count, needed_ammo)
        self.current_ammo += transfer_ammo
        bullet_inventory_object.count -= transfer_ammo
        self.reloading = False

    def update(self, inventory):
        if self.reloading:
            if pygame.time.get_ticks() - self.reload_start_time > self.reload_time:
                self.finish_reload(inventory)

