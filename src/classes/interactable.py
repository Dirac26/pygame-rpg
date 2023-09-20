import pygame

class Interactable:
    def __init__(self, rect, action, once_only=True, angle=0, id=None):
        self.rect = rect
        self.action = action
        self.once_only = once_only
        self.interacted = False
        self.angle = angle
        self.id = id
        self.image = None

    def interact(self, *args, **kwargs):
        if self.once_only and self.interacted:
            return
        self.action(kwargs.get('player'))
        self.interacted = True

    def can_interact(self):
        if self.once_only and self.interacted:
            return False
        return True
    
    def draw(self, screen):
        if self.image:
            rotated_image = pygame.transform.rotate(self.image, self.angle)
            screen.blit(rotated_image, (self.rect.x, self.rect.y))
        else:
            pygame.draw.rect(screen, (255, 0, 0), self.rect, 2)

class Entrance(Interactable):
    def __init__(self, x, y, to_map_id):
        rect = pygame.Rect(x, y, 50, 50) 
        super().__init__(rect, self.change_map, once_only=False)
        self.is_open = False 
        self.to_map_id = to_map_id
    
    def change_map(self, player):
        player.transition_to_map(self.to_map_id)
            

class WoodenChest(Interactable):
    def __init__(self, x, y, items, required_key_name=None, angle=0, id=None):
        rect = pygame.Rect(x, y, 50, 50) 
        super().__init__(rect, self.open_chest, angle=angle, id=id)
        
        self.items = items
        self.required_key_name = required_key_name
        self.is_open = False 
        
        self.closed_image = pygame.image.load('../assets/images/closed_chest.png')
        self.open_image = pygame.image.load('../assets/images/opened_chest.png')
        self.image = self.closed_image

    def open_chest(self, player):
        if not self.is_open:
            if self.required_key_name:
                if player.has_key(self.required_key_name):
                    self.give_items(player)
                else:
                    # Maybe play a sound effect or show a popup saying the player doesn't have the key
                    pass
            else:
                self.give_items(player)

    def give_items(self, player):
        # Code to give items to the player
        for item in self.items:
            player.add_to_inventory(item)
        self.is_open = True
        self.image = self.open_image
        # Maybe add a sound effect or a popup showing the items obtained
        