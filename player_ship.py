import pygame
import os
import characters


HEIGHT = 750
LASER_YELLOW = pygame.image.load(os.path.join('images/lasers', 'yellow.png'))
SPACE_SHIP = pygame.image.load(os.path.join('images/ship', 'ship.png'))


class PlayerShip(characters.GameCharacter):
    """
        Class describe the player ship.

        Variables:
            :var: x, y - current player location
            :var: health - current player health
            :var: character_img - player ship icon
            :var: mask - player img mask
            :var: max_health - player max health(the health at the start of game)

        Methods:
            ...

    """
    def __init__(self, x, y, health=100):
        super().__init__(x, y, health)
        self.character_img = SPACE_SHIP
        self.bullets_img = LASER_YELLOW
        self.mask = pygame.mask.from_surface(self.character_img)
        self.max_health = health

    def move_lasers(self, vel, objs):
        self.cooldown()

        for laser in self.bullets:
            laser.move(vel)

            if laser.off_screen(HEIGHT):
                self.bullets.remove(laser)
            else:
                for obj in objs:
                    if laser.collision(obj):
                        objs.remove(obj)
                        if laser in self.bullets:
                            self.bullets.remove(laser)

    def draw(self, window):
        super().draw(window)
        self.healthbar(window)

    def healthbar(self, window):
        pygame.draw.rect(
            window,
            (255, 0, 0),
            (
                self.x,
                self.y + self.character_img.get_height() + 10,
                self.character_img.get_width(),
                10
            )
        )
        pygame.draw.rect(
            window,
            (0, 255, 0),
            (
                self.x,
                self.y + self.character_img.get_height() + 10,
                self.character_img.get_width() * (self.health / self.max_health),
                10
            )
        )
