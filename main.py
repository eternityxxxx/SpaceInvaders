import pygame
import os
import random
import player_ship
from enemy import Enemy


# Screen size
WIDTH, HEIGHT = 1400, 750


# Game window and title
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Space Invaders')


# Fonts
pygame.font.init()

# Background image
BG = pygame.transform.scale(pygame.image.load(os.path.join('images/background', 'background.jpg')), (WIDTH, HEIGHT))


def collide(obj1, obj2):
    offset_x = obj2.x - obj1.x
    offset_y = obj2.y - obj1.y
    return obj1.mask.overlap(obj2.mask, (offset_x, offset_y)) is not None


def main():
    # Game start status
    run = True
    # FPS
    FPS = 60
    clock = pygame.time.Clock()
    # End of game
    lost = False
    lost_count = 0

    # Player ship
    ship = player_ship.PlayerShip(650, 650)

    # Enemies
    enemies = []
    wave_length = 5
    enemy_velocity = 1

    # Player speeds or the distance, which player will move with one click
    velocity = 5
    # Level counter (1 by default)
    level = 0
    # Lives counter (5 by default)
    lives = 5

    laser_velocity = 5

    # Font settings for lives and level info
    main_font = pygame.font.SysFont('comicsans', 50)
    lost_font = pygame.font.SysFont('comicsans', 60)


    def redraw_window():
        WIN.blit(BG, (0, 0))

        lives_label = main_font.render(f'Lives: {lives}', True, (255, 255, 255))
        level_label = main_font.render(f'Level: {level}', True, (255, 255, 255))

        WIN.blit(lives_label, (10, 10))
        WIN.blit(level_label, (WIDTH - level_label.get_width() - 10, 10))

        for hero in enemies:
            hero.draw(WIN)

        ship.draw(WIN)

        if lost:
            lost_label = lost_font.render('You lost!', True, (255, 255, 255))
            WIN.blit(lost_label, (WIDTH/2 - lost_label.get_width()/2, 350))

        pygame.display.update()


    while run:
        clock.tick(FPS)
        redraw_window()

        if lives <= 0 or ship.health <= 0:
            lost = True
            lost_count += 1

        if lost:
            if lost_count > FPS * 3:
                run = False
            else:
                continue

        if len(enemies) == 0:
            level += 1
            wave_length += 5
            for i in range(wave_length):
                enemy_hero = Enemy(
                    random.randrange(50, WIDTH-100),
                    random.randrange(-1500, -100),
                    random.choice(['green', 'red', 'blue'])
                )
                enemies.append(enemy_hero)

        # Cycle of all events
        for event in pygame.event.get():
            # If user pressed the X at the corner of the screen
            if event.type == pygame.QUIT:
                # Quit the game
                run = False

        # List of key, that pressed at the moment
        keys = pygame.key.get_pressed()

        # Player movement
        # Left
        if keys[pygame.K_a] or keys[pygame.K_LEFT] and (ship.x - velocity) > 0:
            # X - 5
            ship.x -= velocity
        # Right
        if keys[pygame.K_d] or keys[pygame.K_RIGHT] and (ship.x + velocity + ship.get_width()) < WIDTH:
            # X +5
            ship.x += velocity
        # Down
        if (keys[pygame.K_s] or keys[pygame.K_DOWN]) and (ship.y + velocity + ship.get_height()) < HEIGHT:
            ship.y += velocity
        # Up
        if keys[pygame.K_w] or keys[pygame.K_UP] and (ship.y - velocity) > 0:
            ship.y -= velocity
        # Shoot
        if keys[pygame.K_SPACE]:
            ship.shoot()

        for enemy in enemies[:]:
            enemy.move(enemy_velocity)
            enemy.move_lasers(laser_velocity, ship)

            if random.randrange(0, 2 * 60) == 1:
                enemy.shoot()

            if collide(enemy, ship):
                ship.health -= 10
                enemies.remove(enemy)
            if enemy.y + enemy.get_height() > HEIGHT:
                lives -= 1
                enemies.remove(enemy)

        ship.move_lasers(-laser_velocity, enemies)


if __name__ == '__main__':
    title_font = pygame.font.SysFont("comicsans", 70)

    start = True

    while start:
        WIN.blit(BG, (0, 0))

        title_label = title_font.render("Press the mouse to begin...", True, (255, 255, 255))

        WIN.blit(title_label, (WIDTH / 2 - title_label.get_width() / 2, 350))

        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                start = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                main()

    pygame.quit()
