import pygame

class Inventory:
    def __init__(self):
        self.items = []
        self.active = False 
        self.box_size = 50
        self.grid_origin = (100, 100)


    def add_item(self, item):
        self.items.append(item)

    def remove_item(self, item):
        self.items.remove(item)

    def get_item_at_position(self, x, y):
        # Convert the screen coordinates to grid indices
        col = (x - self.grid_origin[0]) // self.box_size
        row = (y - self.grid_origin[1]) // self.box_size

        index = row * 5 + col  # assuming 5 columns
        if 0 <= index < len(self.items):
            return self.items[index]
        return None

    def draw(self, screen):
        if self.active:
            # Draw background for the inventory
            pygame.draw.rect(screen, (150, 150, 150), (self.grid_origin[0], self.grid_origin[1], self.box_size * 5, self.box_size * 5))
            
            # Draw items in their boxes
            for i, item in enumerate(self.items):
                x = self.grid_origin[0] + (i % 5) * self.box_size  # 5 columns
                y = self.grid_origin[1] + (i // 5) * self.box_size
                screen.blit(item.image, (x, y))
    
    def update(self, events):
        if self.active:
            for event in events:
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:  # left click
                        item = self.get_item_at_position(*event.pos)
                        if item:
                            print("You clicked on", item.type)
