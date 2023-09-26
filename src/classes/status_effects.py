import pygame

class StatusEffectUI:
    def __init__(self, x, y, status_effect):
        self.x = x
        self.y = y
        self.status_effect = status_effect
        self.image = status_effect.image
        self.font = pygame.font.SysFont(None, 24)  # Choose your desired font and size

    def draw(self, screen):
        # Draw the image with reduced alpha (for slight transparency)
        image_with_alpha = self.image.copy()
        image_with_alpha.fill((255, 255, 255, 128), special_flags=pygame.BLEND_RGBA_MULT)
        screen.blit(image_with_alpha, (self.x, self.y))

        # Draw the remaining time text on the top right corner of the image
        time_text = self.font.render(str(round(self.status_effect.duration)), True, (255, 255, 255))
        text_x = self.x + self.image.get_width() - time_text.get_width() - 20
        text_y = self.y + 20  # a little padding from the top edge
        screen.blit(time_text, (text_x, text_y))

class StatusEffect:
    def __init__(self, name, duration):
        self.name = name
        self.duration = duration
        self.timer = 0
        self.time_since_last_tick = 1
        self.image = pygame.image.load("./assets/images/slowed_status.png")
        self.font = pygame.font.SysFont(None, 24)


    def update(self, dt):
        """Update the status effect timer."""
        if self.timer > 0:
            self.timer -= dt
        self.time_since_last_tick += dt

    def is_active(self):
        """Check if the status effect is active."""
        return self.timer > 0

    def activate(self):
        """Activate the status effect."""
        self.timer = self.duration

    def effect(self, player):
        """Apply the effect on the player."""
        pass


class SlowEffect(StatusEffect):
    def __init__(self, duration, slow_amount):
        super().__init__("slow", duration)
        self.slow_amount = slow_amount
        self.image = pygame.image.load("./assets/images/slowed_status.png")

    def effect(self, player):
        new_speed = player.max_speed - (player.max_speed * self.slow_amount)
        if self.is_active():
            player.speed = new_speed
        else:
            player.speed = player.max_speed

class DamageEffect(StatusEffect):
    def __init__(self, duration, damage_per_tick, tick_interval=0.5):
        super().__init__("damage", duration)
        self.damage_per_tick = damage_per_tick
        self.tick_interval = tick_interval
        self.image = pygame.image.load("./assets/images/bleed_status_effect.png")

    def effect(self, player):
        if self.is_active():
            if self.time_since_last_tick >= self.tick_interval:
                self.time_since_last_tick = 0
                player.health -= self.damage_per_tick