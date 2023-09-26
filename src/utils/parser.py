import  json
from classes.gun import Gun
from classes.item import Item, InventoryGun, InventoryBullet, InventoryMelee
from classes.npc import NPC
from classes.dialog import Dialog


def parse_json(json_file):
    with open(json_file, 'r') as f:
        data = json.load(f)
    return data

def parse_content_json(json_file):
    data = parse_json(json_file)
    if 'npc' in json_file:
        return NPC.from_data(data)
    elif 'quest' in json_file:
        return Dialog.from_data(data)
    elif 'weapon' in json_file:
        return InventoryGun.from_data(data)
    elif 'item' in json_file:
        return Item.from_data(data)
    elif "bullet" in json_file:
        return InventoryBullet.from_data(data, 100)
    elif "melee" in json_file:
        return InventoryMelee.from_data(data)

