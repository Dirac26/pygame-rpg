import os
import pygame
import pytmx
from classes.item import InventoryBullet, InventoryGun, InventoryMelee
from classes.gun import Gun
from classes.interactable import WoodenChest
from classes.interactable import Entrance
from classes.enemy import enemy_constructor
from classes.npc import NPC
from utils.parser import parse_content_json

class Map:
    def __init__(self, map_path):
        self.map_path = map_path
        self.map_id = self.extract_id_from_path(map_path)
        self.tmx_obj = None
        self.unlocked = True 
        self.enterences = []
        self.spawn_points = {}
        self.npcs = []
        self.enemies = pygame.sprite.Group()
        self.interactables = []
        self.loot_bags = pygame.sprite.Group()
        self.zones = {}
        self.load_map()
        self.active_player_bullets = pygame.sprite.Group()
        self.active_enemy_bullets = pygame.sprite.Group()

    def load_map(self):
        self.tmx_data = pytmx.load_pygame(self.map_path)
        for object in self.tmx_data.objects:
            if 'chest_zone' in object.name:
                chest_type = object.properties.get('obj_type')
                angle = object.properties.get('angle', 0)
                chest_id = object.properties.get('obj_id')
                if chest_type == 'wooden_chest':
                    # Add a chest with gold items at object.x, object.y
                    items = [InventoryBullet("9mm-bullets", "./assets/images/9mm-inventory.png", 20)]
                    chest = WoodenChest(object.x, object.y, items, id=chest_id, angle=angle)
                    self.interactables.append(chest)
                elif chest_type == "starter_chest":
                    # Add a chest with gold items at object.x, object.y
                    items = [
                             parse_content_json("./content/weapons/m4a1.json"),
                             parse_content_json("./content/bullets/5.56.json"),
                             parse_content_json("./content/bullets/shells.json"),
                             parse_content_json("./content/weapons/shotgun.json"),
                             parse_content_json("./content/melee/knife.json"),
                             ]
                    chest = WoodenChest(object.x, object.y, items, id=chest_id, angle=angle)
                    self.interactables.append(chest)
            if 'user_spawn' in object.name:
                spawn = object
                from_id = object.properties.get('from_map_id')
                self.spawn_points[from_id] = (spawn.x, spawn.y)
            if 'entrance' in object.name:
                to_id = object.properties.get('to_map_id')
                entrance = Entrance(object.x, object.y, to_id)
                self.interactables.append(entrance)
            if "enemy_spawn" in object.name:
                enemy_type = object.properties.get('obj_type')
                enemy = enemy_constructor(object.x, object.y, enemy_type)
                self.enemies.add(enemy)
            if "npc" in object.name:
                npc_name = object.properties.get('obj_type')
                npc = NPC(object.x, object.y, npc_name)
                self.npcs.append(npc)
                self.interactables.append(npc)
        self.get_map_zones()

    def get_spawn_point(self, from_map_id):
        if from_map_id in self.spawn_points:
            return self.spawn_points[from_map_id]
    
    def get_map_zones(self):
        self.zones = {"slow": [], "damage": [], "walkable": [], "unwalkable": [], "wall": [], "entrance": []}
        for zone_type in self.zones:
            for obj in self.tmx_data.objects:
                if zone_type in obj.name:
                    self.zones[zone_type].append(obj)
        return self.zones

    def extract_id_from_path(self, path):
        # Extracts the map ID from the filename
        filename = os.path.basename(path)
        return int(filename.split('_')[1].split('.')[0])
    
    def draw(self, screen):
        offset_x = 0
        offset_y = 0 

        # Draw the map onto the screen
        for layer in self.tmx_data.visible_layers:
            if isinstance(layer, pytmx.TiledTileLayer):
                for x, y, image in layer.tiles():
                    screen.blit(image, ((x * self.tmx_data.tilewidth) + offset_x, (y * self.tmx_data.tileheight) + offset_y))
            elif isinstance(layer, pytmx.TiledObjectGroup):
                for obj in layer:
                    if obj.image:
                        screen.blit(obj.image, (obj.x + offset_x, obj.y + offset_y))

