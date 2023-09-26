import pygame

class Objective:
    def __init__(self, description, type, count=1, name=None):
        self.description = description
        self.type = type
        self.name = name
        self.count = count
        self.completed = False
        self.progress = 0
        self.started = False

    def assign_player(self, player):
        if self.type == "kill":
            self.reference_kill_count = player.kill_counts[self.name]
        if self.type == "talk":
            self.reference_talk_count = player.talk_counts[self.name]
        self.started = True

    def update(self, player):
        if not self.started:
            return
        self.progress = player.kill_counts[self.name] - self.reference_kill_count
        if self.progress >= self.count:
            self.completed = True

    def is_complete(self):
        return self.completed
    
    def get_progress(self):
        return f"{self.progress}/{self.count}"

class Quest:
    def __init__(self, name, objectives, reward):
        self.name = name
        self.objectives = objectives
        self.active_objective_index = 0
        self.reward = reward

    def get_active_objective(self):
        return self.objectives[self.active_objective_index]

    def update(self, player):
        self.get_active_objective().update(player)
        if self.get_active_objective().is_complete():
            self.active_objective_index += 1

            if self.active_objective_index >= len(self.objectives):
                self.complete(player)
            else:
                self.get_active_objective().assign_player(player)


    def complete(self, player):
        player.finished_quests.append(self)
        player.active_quests.remove(self)
        for item in self.reward:
            player.add_to_inventory(item)

    def is_complete(self):
        return self.active_objective_index >= len(self.objectives)