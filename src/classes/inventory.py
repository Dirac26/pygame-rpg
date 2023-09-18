import pygame

class Inventory:
    def __init__(self):
        self.items = []
        self.active = False 
        self.box_size = 50
        self.grid_origin = (100, 100)

        self.title_font = pygame.font.SysFont(None, 36)
        self.item_count_font = pygame.font.SysFont(None, 24)
        self.title_color = (0, 0, 0)
        self.count_color = (0, 0, 0)
        self.active_color = (255, 0, 0)
        self.active_gun = None

    def add_item(self, item):
        self.items.append(item)

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
        items_in_row = 10
        if self.active:

            pygame.draw.rect(screen, (150, 150, 150), (self.grid_origin[0], self.grid_origin[1], self.box_size * items_in_row, self.box_size * items_in_row))
            
            for i, item in enumerate(self.items):
                x = self.grid_origin[0] + (i % items_in_row) * self.box_size  # 5 columns
                y = self.grid_origin[1] + (i // items_in_row) * self.box_size
                screen.blit(item.image, (x, y))
                count_surface = self.item_count_font.render(str(item.count), True, self.count_color)
                count_position = (x + self.box_size - count_surface.get_width() - items_in_row, y + self.box_size - count_surface.get_height() - items_in_row)
                screen.blit(count_surface, count_position)

                if self.active_gun and self.active_gun.name == item.name:
                    border_thickness = 3
                    border_rect = pygame.Rect(x-border_thickness, y-border_thickness, self.box_size + 2*border_thickness, self.box_size + 2*border_thickness)
                    pygame.draw.rect(screen, (255, 0, 0), border_rect, border_thickness)

            # Draw the title
            title_surface = self.title_font.render('Inventory', True, self.title_color)
            title_position = (self.grid_origin[0] + (self.box_size * items_in_row - title_surface.get_width()) // 2, self.grid_origin[1] - title_surface.get_height() - 10)
            screen.blit(title_surface, title_position)
    
    def update(self, events, player):
        if self.active:
            for event in events:
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        item = self.get_item_at_position(*event.pos)
                        if item:
                            item.use(player)
                            if item.type == "gun":
                                self.active_gun = item
                                
