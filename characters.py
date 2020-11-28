import laser


HEIGHT = 750


class GameCharacter:
    """
        Class describe game entities

        Variables:
            :var: x, y - current character location
            :var: health - current character health
            :var: character_img - character icon
            :var: bullets_img - bullets icon
            :var: bullets -
            :var: cool_down_counter - cool_down to protect from spamming of bullets

        Methods:
            draw()
            get_width()
            get_height()

    """
    COOLDOWN = 30

    def __init__(self, x, y, health=100):
        self.x = x
        self.y = y
        self.health = health
        self.character_img = None
        self.bullets_img = None
        self.bullets = []
        self.cool_down_counter = 0

    def draw(self, window):
        window.blit(self.character_img, (self.x, self.y))

        for bullet in self.bullets:
            bullet.draw(window)

    def move_lasers(self, vel, obj):
        self.cooldown()

        for bullet in self.bullets:
            bullet.move(vel)

            if bullet.off_screen(HEIGHT):
                self.bullets.remove(bullet)
            elif bullet.collision(obj):
                obj.health -= 10
                self.bullets.remove(bullet)

    def cooldown(self):
        if self.cool_down_counter >= self.COOLDOWN:
            self.cool_down_counter = 0
        elif self.cool_down_counter > 0:
            self.cool_down_counter += 1

    def shoot(self):
        if self.cool_down_counter == 0:
            bullet = laser.Laser(self.x, self.y, self.bullets_img)
            self.bullets.append(bullet)
            self.cool_down_counter = 1

    def get_width(self):
        return self.character_img.get_width()

    def get_height(self):
        return self.character_img.get_height()
