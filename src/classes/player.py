import pygame
from classes.bullet import Bullet
from classes.gun import Gun
from classes.inventory import Inventory
from classes.item import InventoryGun, InventoryBullet

bullets = pygame.sprite.Group()

class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load("../assets/images/main-player-1.png")
        self.x = 100
        self.y = 100
        self.width = 32
        self.height = 32
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)
        self.inventory = Inventory()
        self.init_inventory()
        self.speed = 5
        self.last_direction = 'right'
        self.last_shot_time = pygame.time.get_ticks()
        
    def init_inventory(self):
        gun = Gun("pistol")
        self.gun = gun
        self.inventory.add_item(InventoryGun("pistol", "../assets/images/9mm-inventory.png", gun))
        self.inventory.add_item(InventoryGun("9mm-bullets", "../assets/images/9mm-inventory.png", 100))
        print(self.inventory.items)


    def update(self, events):
        #continus movement
        keys = pygame.key.get_pressed()
        if keys[pygame.K_w]:
            self.rect.y -= self.speed
            self.last_direction = 'up'
        if keys[pygame.K_a]:
            self.rect.x -= self.speed
            self.last_direction = 'left'
        if keys[pygame.K_s]:
            self.rect.y += self.speed
            self.last_direction = 'down'
        if keys[pygame.K_d]:
            self.rect.x += self.speed
            self.last_direction = 'right'
        if keys[pygame.K_SPACE]:
            self.shoot()

        #single pressed button
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_i:
                    self.inventory.active = True
                    
        
    def shoot(self):
        current_time = pygame.time.get_ticks()
        if current_time - self.last_shot_time >= self.gun.fire_rate:
            bullet = self.gun.create_bullet(self.rect.centerx, self.rect.centery, self.last_direction)  
            bullets.add(bullet)
            self.last_shot_time = current_time

    def draw(self, surface):
        surface.blit(self.image, self.rect)
        pygame.draw.rect(surface, (255, 0, 0), self.rect, 2)