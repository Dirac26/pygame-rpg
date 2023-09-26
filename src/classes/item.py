import pygame
from classes.gun import Gun
from classes.melee import MeleeWeapon

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
        self.attributes = {
            "name": self.name
        }

    def use(self, player):
        # Change player's primary gun
        player.active_weapon = self

    @classmethod
    def from_data(cls, data):
        return cls(data['name'],
                   data['inventory_image_path'], Gun.from_data(data))

class InventoryMelee(Item):
    def __init__(self, name, inventory_image_path, item_object):
        super().__init__(name, inventory_image_path)
        self.count = 1
        self.type = "melee"
        self.item_object = item_object
        self.attributes = {
            "name": self.name
        }

    @classmethod
    def from_data(cls, data):
        return cls(data['name'],
                   data['inventory_image_path'], MeleeWeapon.from_data(data))

    def use(self, player):
        # Change player's primary gun
        player.melee_weapon = self

    

class InventoryBullet(Item):
    def __init__(self, name, inventory_image_path, count):
        super().__init__(name, inventory_image_path)
        self.count = count
        self.type = "bullet"
        self.attributes = {
            "name": self.name
        }

    @classmethod
    def from_data(cls, data, count):
        return cls(data['name'],
                   data['inventory_image_path'], count)


