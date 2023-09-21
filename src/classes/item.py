import pygame

atter_dict = {
    "pistol": {
        "damage": 10,
        "fire_rate": 1,
        "bullet_speed": 10,
        "bullet_count": 1,
        "bullet_spread": 0,
        "bullet_type": "9mm",
        "lore": "A pistol that has been passed down through \n generations of your family"
    },
    "machine_gun": {
        "damage": 10,
        "fire_rate": 1,
        "bullet_speed": 10,
        "bullet_count": 1,
        "bullet_spread": 0,
        "bullet_type": "9mm",
        "lore": "machine gun, it shoots fast i guess"
    },
    "9mm-bullets": {
        "lore": "these are not candy theese are bullets \n used for small pistols",
    },
    "knife": {
        "damage": 10,
        "lore": "a knife, not very special but it does the job"
    },
    "5.56-bullets": {
        "lore": "high damage bullets used for machine guns\n they also look like they hurt"
}
}
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
        self.attributes = atter_dict[item_object.name]

    def use(self, player):
        # Change player's primary gun
        player.active_weapon = self

class InventoryMelee(Item):
    def __init__(self, name, inventory_image_path):
        super().__init__(name, inventory_image_path)
        self.count = 1
        self.type = "melee"
        self.attributes = atter_dict[name]

    def use(self, player):
        # Change player's primary gun
        player.melee_weapon = self

class InventoryBullet(Item):
    def __init__(self, name, inventory_image_path, count):
        super().__init__(name, inventory_image_path)
        self.count = count
        self.type = "bullet"
        self.attributes = atter_dict[name]


