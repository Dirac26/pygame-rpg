import pygame
from classes.status_effects import StatusEffectUI

class HUD:
    def __init__(self, player):
        self.player = player  # Assuming the player object has health, gold, and active_weapon attributes
        self.font = pygame.font.SysFont(None, 36)  # You can choose another font and size
        self.small_font = pygame.font.SysFont(None, 24)

    def draw(self, screen):
        # Draw HP bar
        pygame.draw.rect(screen, (255, 0, 0), (10, 10, 100, 20))  # This is the red "background" indicating max health
        pygame.draw.rect(screen, (0, 255, 0), (10, 10, self.player.health, 20))  # This is the green "foreground" indicating current health

        # Display health points
        health_text = self.font.render(f"{self.player.health} / 100", True, (255, 0, 0))
        screen.blit(health_text, (120, 10))

        # Display gold count
        gold_text = self.small_font.render(f"Gold: {self.player.gold}", True, (255, 215, 0))
        screen.blit(gold_text, (10, 40))

        # Display active weapon and ammo
        if self.player.active_gun:
            screen.blit(self.player.active_gun.image, (10, screen.get_height() - 100))
            ammo_text = self.small_font.render(f"Ammo: {self.player.active_gun.item_object.current_ammo} / {self.player.active_gun.item_object.clip_size}", True, (0, 0, 0))
            screen.blit(ammo_text, (20, screen.get_height() - 50))

        if self.player.active_gun.item_object.reloading:
            reload_text = self.small_font.render("Reloading...", True, (255, 0, 0))
            player_position = self.player.rect.topleft
            reload_position = (player_position[0] + self.player.rect.width // 2 - reload_text.get_width() // 2, player_position[1] - 30)
            screen.blit(reload_text, reload_position)

        if self.player.near_interactable:
            interact_text = self.small_font.render("Press E to interact", True, (255, 0, 0))
            interact_position = (self.player.rect.x + self.player.rect.width // 2 - interact_text.get_width() // 2, self.player.rect.y - 30)
            screen.blit(interact_text, interact_position)

        screen_width = screen.get_width()
        spacing = 5
        active_effects = [x for x in self.player.status_effects if x.is_active()]
        total_width = sum(30 for effect in active_effects) + spacing * (len(active_effects) - 1)
        start_x = (screen_width - total_width) // 2
        start_y = screen.get_height() - 60

        for effect in active_effects:
            effect_ui = StatusEffectUI(start_x, start_y, effect)
            effect_ui.draw(screen)
            start_x += effect_ui.image.get_width() + spacing