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
        self.count = 1
        self.type = "gun"
        self.item_object = item_object

    def use(self, player):
        # Change player's primary gun
        player.gun = self.item_object
        player.active_gun = self

class InventoryBullet(Item):
    def __init__(self, name, inventory_image_path, count):
        super().__init__(name, inventory_image_path)
        self.count = count
        self.type = "bullet"

