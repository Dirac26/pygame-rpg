import os
import pytmx
from classes.item import InventoryBullet
from classes.interactable import WoodenChest
from classes.interactable import Entrance

class Map:
    def __init__(self, map_path):
        self.map_path = map_path
        self.map_id = self.extract_id_from_path(map_path)
        self.tmx_obj = None
        self.unlocked = True 
        self.enterences = []
        self.spawn_points = {}
        self.npcs = []
        self.interactables = []
        self.zones = {}
        self.load_map()

    def load_map(self):
        self.tmx_data = pytmx.load_pygame(self.map_path)
        for object in self.tmx_data.objects:
            if 'chest_zone' in object.name:
                chest_type = object.properties.get('obj_type')
                angle = object.properties.get('angle', 0)
                chest_id = object.properties.get('obj_id')
                if chest_type == 'wooden_chest':
                    # Add a chest with gold items at object.x, object.y
                    items = [InventoryBullet("9mm-bullets", "../assets/images/9mm-inventory.png", 20)]
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
        # Draw the map onto the screen
        for layer in self.tmx_data.visible_layers:
            if isinstance(layer, pytmx.TiledTileLayer):
                for x, y, image in layer.tiles():
                    screen.blit(image, (x * self.tmx_data.tilewidth, y * self.tmx_data.tileheight))
            elif isinstance(layer, pytmx.TiledObjectGroup):
                for obj in layer:
                    if obj.image:
                        screen.blit(obj.image, (obj.x, obj.y))

