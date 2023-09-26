import pygame
from classes.logger import Logger

class Inventory:
    def __init__(self):
        self.items = []
        self.active = False 
        self.box_size = 50
        self.grid_origin = (100, 100)
        self.active_weapon = None
        self.active_melee_weapon = None
        self.head_armor = None
        self.chest_armor = None
        self.leg_armor = None
        self.boots_armor = None
        self.text_y = 0

        self.title_font = pygame.font.SysFont(None, 36)
        self.item_count_font = pygame.font.SysFont(None, 24)
        self.title_color = (0, 0, 0)
        self.count_color = (0, 0, 0)
        self.active_color = (255, 0, 0)
        self.logger = Logger()
        self.selected_item = None
        self.empty_slot_image = {
            "head": pygame.image.load('./assets/images/empty_head_piece.png'),
            "chest": pygame.image.load('./assets/images/empty_chest_piece.png'),
            "leg": pygame.image.load('./assets/images/empty_leg_piece.png'),
            "boots": pygame.image.load('./assets/images/empty_boots_piece.png'),
            "weapon": pygame.image.load('./assets/images/empty_gun_piece.png'),
            "melee": pygame.image.load('./assets/images/empty_melee_piece.png'),
        }

    def add_item(self, item):
        for t in self.items:
            if t.name == item.name:
                t.count += item.count
                break
        else:
            self.items.append(item)
        self.logger.add_message(f"Added {item.count} {item.name} to inventory")

    def remove_item(self, item):
        self.items.remove(item)

    def get_item(self, name):
        for item in self.items:
            if item.name == name:
                return item
        return None

    def get_item_at_position(self, x, y):
        # Convert the screen coordinates to grid indices
        col = (x - self.grid_origin[0]) // self.box_size
        row = (y - self.grid_origin[1]) // self.box_size

        index = row * 5 + col  # assuming 5 columns
        if 0 <= index < len(self.items):
            return self.items[index]
        return None

    def draw(self, screen):
        items_in_row = 5
        if self.active:

            pygame.draw.rect(screen, (150, 150, 150), (self.grid_origin[0], self.grid_origin[1], self.box_size * items_in_row, self.box_size * items_in_row))
            
            for i, item in enumerate(self.items):
                x = self.grid_origin[0] + (i % items_in_row) * self.box_size  # 5 columns
                y = self.grid_origin[1] + (i // items_in_row) * self.box_size
                screen.blit(item.image, (x, y))
                count_surface = self.item_count_font.render(str(item.count), True, self.count_color)
                count_position = (x + self.box_size - count_surface.get_width() - items_in_row, y + self.box_size - count_surface.get_height() - items_in_row)
                screen.blit(count_surface, count_position)

            # Draw the title
            title_surface = self.title_font.render('Inventory', True, self.title_color)
            title_position = (self.grid_origin[0] + (self.box_size * items_in_row - title_surface.get_width()) // 2, self.grid_origin[1] - title_surface.get_height() - 10)
            screen.blit(title_surface, title_position)

        # Draw details for selected_item
        if self.selected_item is not None:
            large_img = pygame.transform.scale(self.selected_item.image, (100, 100))
            screen.blit(large_img, (400, 100))
            
            # Draw the attributes
            font = pygame.font.Font(None, 36)
            text_y = 210
            for attribute, value in self.selected_item.attributes.items():
                text = font.render(f"{attribute}: {value}", True, (255, 255, 255))
                screen.blit(text, (400, text_y))
                text_y += 40
                
                # Check if text is clipping out of screen
                if text_y > screen.get_height() - 50:
                    break
            self.text_y = text_y + 10
            # Draw "Use" button below the text
            pygame.draw.rect(screen, (0, 255, 0), (400, text_y + 10, 100, 50))
            text = font.render("Use", True, (0, 0, 0))
            screen.blit(text, (425, text_y + 20))
    
        # Draw active melee weapon and armor slots (placeholder)
        if self.active_melee_weapon:
            screen.blit(self.active_melee_weapon.image, (640, 10))
        else:
            screen.blit(self.empty_slot_image["melee"], (640, 10))

        # Draw active melee weapon and armor slots (placeholder)
        if self.active_weapon:
            screen.blit(self.active_weapon.image, (640, 70))
        else:
            screen.blit(self.empty_slot_image["weapon"], (640, 70))

        for i, armor_type in enumerate(['head', 'chest', 'leg', 'boots']):
            armor = getattr(self, f"{armor_type}_armor")
            if armor:
                screen.blit(armor.image, (700, 10 + i*60))
            else:
                screen.blit(self.empty_slot_image[armor_type], (700, 10 + i*60))

    def on_item_click(self, item):
        self.selected_item = item

    def use_selected_item(self, player):
        if self.selected_item is None:
            return
        
        if self.selected_item.type == 'gun':
            self.active_weapon = self.selected_item
            player.set_gun(self.selected_item)
        elif self.selected_item.type == 'melee':
            self.active_melee_weapon = self.selected_item
            player.set_melee(self.selected_item)
        elif self.selected_item.type == 'armor':
            # Match armor type to appropriate slot (assuming armor types are 'Head', 'Chest', etc.)
            setattr(self, f"{self.selected_item.attributes['armor_type'].lower()}_armor", self.selected_item)
        elif self.selected_item.type == 'consumable':
            # Assume the item has a use_effect() method that applies the item's effects
            self.selected_item.use_effect()
            self.items.remove(self.selected_item)

    def update(self, events, player):
        if self.active:
            for event in events:
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        x, y = event.pos
                        item = self.get_item_at_position(x, y)
                        if item:
                            self.on_item_click(item)
                        # Check if clicked on the "Use" button
                        if 400 <= x <= 500 and self.text_y <= y <= self.text_y + 50:
                            self.use_selected_item(player)

                                
