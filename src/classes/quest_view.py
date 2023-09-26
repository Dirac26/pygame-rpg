import pygame
from pygame.locals import *

SCREEN_WIDTH, SCREEN_HEIGHT = 1200, 800
BUTTON_HEIGHT = 50

class QuestView:
    def __init__(self):
        self.active = False
        self.active_tab = "Active"
        self.selected_quest = None
        self.scroll_offset = 0
        self.active_quests = []
        self.finished_quests = []

    def update(self, events, player):
        self.active_quests = player.active_quests
        self.finished_quests = player.finished_quests
        for event in events:
            if event.type == MOUSEBUTTONDOWN:
                if event.button == 1:  # Left click
                    x, y = event.pos

                    # Check tabs first
                    if y < BUTTON_HEIGHT:  
                        if x < SCREEN_WIDTH / 2:
                            self.active_tab = "Active"
                        else:
                            self.active_tab = "Completed"
                        return
                    
                    # Check quests list
                    start_y = BUTTON_HEIGHT + 10
                    quest_height = 40
                    max_displayed_quests = (SCREEN_HEIGHT - BUTTON_HEIGHT - 10) // quest_height
                    quest_area_start = start_y
                    quest_area_end = quest_area_start + max_displayed_quests * quest_height

                    if quest_area_start <= y <= quest_area_end:
                        quest_idx = (y - quest_area_start) // quest_height
                        if self.active_tab == "Active":
                            if quest_idx < len(player.active_quests):
                                self.selected_quest = player.active_quests[self.scroll_offset + quest_idx]
                        else:
                            if quest_idx < len(player.finished_quests):
                                self.selected_quest = player.finished_quests[self.scroll_offset + quest_idx]


    def draw(self, screen):
        screen = pygame.display.get_surface()
        screen.fill((50, 50, 50))  # Dark background

        # Drawing tabs
        self.draw_tabs(screen)

        # Drawing quest list
        self.draw_quests_list(screen)

        # Drawing selected quest details
        self.draw_selected_quest(screen)

        pygame.display.flip()

    def draw_tabs(self, screen):
        active_color = (100, 100, 100) if self.active_tab == "Active" else (75, 75, 75)
        completed_color = (100, 100, 100) if self.active_tab == "Completed" else (75, 75, 75)
        
        pygame.draw.rect(screen, active_color, (0, 0, SCREEN_WIDTH / 2, BUTTON_HEIGHT))
        pygame.draw.rect(screen, completed_color, (SCREEN_WIDTH / 2, 0, SCREEN_WIDTH / 2, BUTTON_HEIGHT))
        
        font = pygame.font.Font(None, 36)
        active_text = font.render("Active", True, (255, 255, 255))
        completed_text = font.render("Completed", True, (255, 255, 255))
        
        screen.blit(active_text, (SCREEN_WIDTH / 4 - active_text.get_width() / 2, BUTTON_HEIGHT / 2 - active_text.get_height() / 2))
        screen.blit(completed_text, (3 * SCREEN_WIDTH / 4 - completed_text.get_width() / 2, BUTTON_HEIGHT / 2 - completed_text.get_height() / 2))


    def draw_quests_list(self, screen):
        if self.active_tab == "Active":
            quests = self.active_quests
        else:
            quests = self.finished_quests

        start_y = BUTTON_HEIGHT + 10  # 10 pixels gap
        quest_height = 40
        max_displayed_quests = (SCREEN_HEIGHT - BUTTON_HEIGHT - 10) // quest_height

        for idx, quest in enumerate(quests[self.scroll_offset:self.scroll_offset + max_displayed_quests]):
            y_position = start_y + idx * quest_height
            pygame.draw.rect(screen, (100, 100, 100), (50, y_position, SCREEN_WIDTH - 500, quest_height))
            font = pygame.font.Font(None, 24)
            quest_name = font.render(quest.name, True, (255, 255, 255))
            screen.blit(quest_name, (60, y_position + quest_height / 2 - quest_name.get_height() / 2))


    def draw_selected_quest(self, screen):
        if self.selected_quest is None:
            return
        
        if not self.selected_quest.is_complete():
            description = self.selected_quest.get_active_objective().description
            progress = self.selected_quest.get_active_objective().get_progress()
            reward = self.selected_quest.reward

        else:
            description = "Quest Completed!"
            progress = ""
            reward = self.selected_quest.reward

        # Set some base positions and sizes
        padding = 20
        start_x = SCREEN_WIDTH * 2 // 3 + padding
        start_y = BUTTON_HEIGHT + padding
        text_gap = 30
        reward_gap = 50
        
        # Create fonts
        font = pygame.font.Font(None, 36)
        
        # Draw Quest Description
        quest_description = font.render(description, True, (255, 255, 255))
        screen.blit(quest_description, (start_x, start_y))
        
        # Draw Quest Progress
        progress_text = progress
        progress_rendered = font.render(progress_text, True, (255, 255, 255))
        screen.blit(progress_rendered, (start_x, start_y + text_gap))
        
        # Draw Rewards
        reward_y = start_y + 2 * text_gap
        
        for reward in reward:
            # Assuming each reward item has a 'name', 'image', and 'count'
            reward_img = reward.image
            reward_count = reward.count
            
            # Draw the reward image
            screen.blit(reward_img, (start_x, reward_y))
            
            # Draw the count text beside the image
            count_text = font.render(f"x{reward_count}", True, (255, 255, 255))
            screen.blit(count_text, (start_x + reward_img.get_width() + 10, reward_y + reward_img.get_height() // 2 - count_text.get_height() // 2))
            
            reward_y += reward_gap
