import pygame

class Dialog:
    def __init__(self, lines, dialog_id, quest=None, prequisites_dialog_ids=[]):
        self.dialog_id = dialog_id
        self.lines = lines
        self.index = 0
        self.finished = False
        self.quest = quest
        self.prequisites_dialog_ids = prequisites_dialog_ids

    def next_line(self):
        if self.index < len(self.lines) - 1:
            self.index += 1
        else:
            self.finished = True

    def current_line(self):
        return self.lines[self.index][1]
    
    def current_speaker(self):
        return self.lines[self.index][0]
    
    def update(self, events):
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    self.next_line()
                if event.type == pygame.QUIT:
                    self.next_line()
    
    def draw(self, screen):
        # Draw a semi-transparent background for the dialog box
        pygame.draw.rect(screen, (0, 0, 0, 180), (100, 600, 1000, 150))

        # Draw the text
        font = pygame.font.Font(None, 36)

        # Speaker's name
        speaker_text = font.render(f"{self.current_speaker()}: ", True, (255, 255, 255))
        screen.blit(speaker_text, (120, 620))

        # The dialog line
        line_text = font.render(self.current_line(), True, (255, 255, 255))
        screen.blit(line_text, (120 + speaker_text.get_width(), 620))