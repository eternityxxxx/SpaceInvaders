import characters
import pygame
import os
import laser


# Enemy icons
ENEMY_GREEN = pygame.image.load(os.path.join('images/enemy', 'enemy_green.png'))
ENEMY_BLUE = pygame.image.load(os.path.join('images/enemy', 'enemy_blue.png'))
ENEMY_RED = pygame.image.load(os.path.join('images/enemy', 'enemy_red.png'))

# Bullet icons
LASER_RED = pygame.image.load(os.path.join('images/lasers', 'red.png'))
LASER_BLUE = pygame.image.load(os.path.join('images/lasers', 'blue.png'))
LASER_GREEN = pygame.image.load(os.path.join('images/lasers', 'green.png'))


class Enemy(characters.GameCharacter):
    TYPE_MAP = {
        'green': (ENEMY_GREEN, LASER_GREEN),
        'red': (ENEMY_RED, LASER_RED),
        'blue': (ENEMY_BLUE, LASER_BLUE),
    }

    def __init__(self, x, y, enemy_type, health=100):
        super().__init__(x, y, health)
        self.character_img, self.bullets_img = self.TYPE_MAP[enemy_type]
        self.mask = pygame.mask.from_surface(self.character_img)

    def move(self, vel):
        self.y += vel

    def shoot(self):
        if self.cool_down_counter == 0:
            bullet = laser.Laser(self.x-20, self.y, self.bullets_img)
            self.bullets.append(bullet)
            self.cool_down_counter = 1
