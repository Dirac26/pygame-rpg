import pygame
import math

class MeleeWeapon:
    def __init__(self, name, damage, image_path, swing_speed, swing_cooldown, knockback_distance, swing_sound_path):
        self.name = name
        self.damage = damage
        self.image = pygame.image.load(image_path)
        self.rect = self.image.get_rect()
        self.swing_speed = swing_speed
        self.swing_cooldown = swing_cooldown
        self.current_swing_time = swing_cooldown
        self.thrusting = False
        self.last_swing_time = 0
        self.angle = 0
        self.swing_angle_range = math.radians(30)  # 30 degrees to left and right
        self.current_swing_angle = 0  # current swing angle relative to initial angle
        self.swing_direction = 1  # 1 for swinging right, -1 for swinging left
        self.swinging = False
        self.knockback_distance = knockback_distance
        self.hit_enemies = []
        self.swing_sound = pygame.mixer.Sound(swing_sound_path)
        self.swing_sound.set_volume(0.2)
    


    @classmethod
    def from_data(cls, data):
        obj = cls(data['name'],
                  data["damage"],
                  data['image_path'],
                  data['swing_speed'],
                  data['swing_cooldown'],
                  data["knockback"],
                  data["swing_sound"]
                   )
        return obj

    def swing(self, x, y, target_x, target_y):
        dx = target_x - x
        dy = target_y - y
        self.angle = math.atan2(dy, dx)

        self.last_swing_time = pygame.time.get_ticks()
        self.swinging = True
        self.swing_direction = 1 if dx > 0 else -1
        self.current_swing_angle = self.angle - self.swing_angle_range * self.swing_direction
        self.hitbox_rect = None
        self.swing_sound.play()

    def update(self, dt, x, y, enemies):
        if self.swinging:
            self.current_swing_angle += self.swing_speed * dt * self.swing_direction
            if self.current_swing_angle > self.angle + self.swing_angle_range or self.current_swing_angle < self.angle - self.swing_angle_range:
                self.swinging = False
                self.current_swing_angle = 0
                self.angle = 0
            width, height = self.rect.size
            handle_offset = (width // 2, height // 2)

            self.handle_x = x + handle_offset[0] * math.cos(self.current_swing_angle) - handle_offset[1] * math.sin(self.current_swing_angle)
            self.handle_y = y + handle_offset[0] * math.sin(self.current_swing_angle) + handle_offset[1] * math.cos(self.current_swing_angle)

            self.points = [
                (x, y),
                (x + math.cos(self.current_swing_angle) * width, y + math.sin(self.current_swing_angle) * width),
                (x + math.cos(self.current_swing_angle) * width - math.sin(self.current_swing_angle) * height,
                 y + math.sin(self.current_swing_angle) * width + math.cos(self.current_swing_angle) * height),
                (x - math.sin(self.current_swing_angle) * height, y + math.cos(self.current_swing_angle) * height)
            ]

            for enemey in enemies:
                if enemey in self.hit_enemies:
                    continue
                if self.hitbox_rect and self.hitbox_rect.colliderect(enemey.rect):
                    enemey.take_damage(self.damage, self.knockback_distance, self.rect.x, self.rect.y)
                    self.hit_enemies.append(enemey)
                    self.swinging = False
        self.hit_enemies = []
            

    def draw(self, surface):
        if self.swinging:
            pygame.draw.polygon(surface, (255, 0, 0), self.points, 2)
            rotated_image, new_rect = self.rotate(self.image, math.degrees(self.current_swing_angle), (self.handle_x, self.handle_y))
            surface.blit(rotated_image, new_rect.topleft)
            self.hitbox_rect = new_rect
            

    def rotate(self, surface, angle, pivot):
        rotated_image = pygame.transform.rotate(surface, -angle)  # Note the negation of the angle
        new_rect = rotated_image.get_rect(center=pivot)
        return rotated_image, new_rect