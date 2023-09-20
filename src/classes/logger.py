import pygame
from collections import deque

class LogMessage:
    def __init__(self, message, lifetime=200):  # default lifetime is 1 second (1000ms)
        self.message = message
        self.lifetime = lifetime

class Logger:
    def __init__(self, max_logs=5):
        self.logs = deque(maxlen=max_logs)
        self.font = pygame.font.SysFont(None, 24)
        self.lifetime = 200

    def add_message(self, message):
        self.logs.appendleft(LogMessage(message, self.lifetime))

    def update(self):
        try:
            for log in self.logs:
                log.lifetime -= 1
                if log.lifetime <= 0:
                    self.logs.remove(log)
        except:
            pass

    def draw(self, screen):
        y_offset = 0
        try:
            for log in self.logs:
                alpha = max(255 * log.lifetime / self.lifetime, 0)  # linear fade effect
                log_surf = self.font.render(log.message, True, (0, 0, 0))
                log_surf.set_alpha(alpha)
                screen.blit(log_surf, (screen.get_width() - log_surf.get_width() - 10, screen.get_height() - 30 - y_offset))
                y_offset += 25
        except:
            pass