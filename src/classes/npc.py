import pygame
from classes.dialog import Dialog
from classes.quest import Quest, Objective
from classes.interactable import Interactable
from classes.item import InventoryBullet

class NPC(Interactable):
    def __init__(self, x, y, name):
        self.image = pygame.image.load(npc_images[name])
        rect = self.image.get_rect()
        rect.x = x
        rect.y = y
        super().__init__(rect, self.interact, once_only=False)
        self.interactions = npc_dialogue_quests[name]  # A queue of dialogs and quests
        self.current_interaction_index = 0

    def interact(self, player):
        if self.current_interaction_index >= len(self.interactions):
            return
        interaction = self.interactions[self.current_interaction_index]

        if len(interaction.prequisites_dialog_ids) > 0 and set(interaction.prequisites_dialog_ids).issubset([dialog.dialog_id for dialog in player.old_dialogs]):
            return
        if isinstance(interaction, Dialog):
            player.set_in_dialog(interaction)
        
        if interaction.quest:
            player.add_quest(interaction.quest)

        # After interaction, move to next in queue
        self.current_interaction_index += 1


npc_dialogue_quests = {
    "old guy": [
        Dialog([("old guy", "oh wow if it isnt the retard adventurer"), ("old guy", "lets see how long you will last here")], 1, []),
        Dialog([("old guy", "u look so weak i bet you cant even survive 5 of this place horrible creatures")], 2,
                Quest("kill Zombies", [Objective("kill 5 zombies", "kill", 5, "zombie")], [InventoryBullet("9mm-bullets", "./assets/images/9mm-inventory.png", 20)]), prequisites_dialog_ids=[]),
                ]

}

npc_images = {
    "old guy": "./assets/images/old guy.png"
}