from math import sin, cos
import random
from classes.bullet import Bullet

class ShootingStyle:
    def __init__(self, bullet_damage, bullet_speed, distance, image_path, knockback_distance=10):
        self.bullet_damage = bullet_damage
        self.bullet_distance = distance
        self.bullet_speed = bullet_speed
        self.image_path = image_path
        self.knockback_distance = knockback_distance

    def shoot(self, x, y, dx, dy):
        """
        Create bullets and return them.
        :param start_pos: (x, y) tuple where bullet originates from (gun position).
        :param target_pos: (x, y) tuple where the bullet should go (mouse click or target position).
        :return: list of Bullet instances.
        """
        raise NotImplementedError("Each shooting style must implement its own shoot method")
    
    def create_bullet(self, x, y, dx, dy):
        bullet = Bullet(self.bullet_damage, self.bullet_speed, self.image_path, x, y, self.bullet_distance, self.knockback_distance)
        bullet.dx = dx
        bullet.dy = dy
        bullet.rect.x = x
        bullet.rect.y = y
        bullet.rotate_based_on_direction()
        return bullet
    
class PistolStyle(ShootingStyle):
    def __init__(self, bullet_damage, bullet_speed, distance, image_path, knockback_distance):
        super().__init__(bullet_damage, bullet_speed, distance, image_path, knockback_distance)

    def shoot(self, x, y, dx, dy):
        return [self.create_bullet(x, y, dx, dy)]

class ShotgunStyle(ShootingStyle):
    def __init__(self, bullet_damage, bullet_speed, distance, image_path, knockback_distance):
        super().__init__(bullet_damage, bullet_speed, distance, image_path, knockback_distance)
        self.spread = 3
        self.spread_angle = 10

    def shoot(self, x, y, dx, dy):
        bullets = []
        for _ in range(self.spread):
            deviation = random.uniform(-self.spread_angle, self.spread_angle) * (3.141592653589793 / 180)
            new_dx = dx * cos(deviation) - dy * sin(deviation)
            new_dy = dx * sin(deviation) + dy * cos(deviation)
            bullets.append(self.create_bullet(x, y, new_dx, new_dy))
        return bullets