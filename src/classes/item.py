import pygame

class Item:
    def __init__(self, name, inventory_image_path):
        self.name = name
        self.image = pygame.image.load(inventory_image_path)
    
    def use(self):
        pass

class InventoryGun(Item):
    def __init__(self, name, inventory_image_path, item_object):
        super().__init__(name, inventory_image_path)

    def use(self, player):
        # Change player's primary gun
        player.gun = self.item_object

class InventoryBullet(Item):
    def __init__(self, name, inventory_image_path, count):
        super().__init__(name, inventory_image_path)
        self.count = count
