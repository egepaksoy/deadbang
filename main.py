import pygame
import random

from pygame.draw import rect


pygame.init()

# -----------COLORS----------
ENEMIE_BULLET_COLOR = (250, 0, 0)
BULLET_COLOR = (0, 0, 250)

# ----------VALUES-----------
FPS = 60
VEL_SHIP = 6
VEL_ENEMIE = 3
VEL_BULLET = 5
VEL_ENEMIE_BULLET = 5
BULLET_WIDTH = 5
BULLET_HEIGHT = 24
HEART_WIDTH = 25
HEART_HEIGHT = 25

#-------------TEXT-----------
label = pygame.font.SysFont(None, 76)

# ---------WIN SIZES---------
WIN_WIDTH = 500
WIN_HEIGHT = 700
WIN = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT))

# -------SHIP SIZES---------
SHIP_WIDTH = 55
SHIP_HEIGHT = 55
ENEMIE_WIDTH = 50
ENEMIE_HEIGHT = 60

# -------------BG------------
BG_IMAGE = pygame.image.load("./assets/space.png")
BG = pygame.transform.scale(BG_IMAGE, (WIN_WIDTH, WIN_HEIGHT))

#-----------SPACESHIP-------
SHIP_IMAGE = pygame.image.load("./assets/spaceship.png")
SHIP = pygame.transform.scale(SHIP_IMAGE, (SHIP_WIDTH, SHIP_HEIGHT))

ENEMIE_SHIP = pygame.image.load("./assets/watermelon.png")
E_SHIP = pygame.transform.scale(ENEMIE_SHIP, (ENEMIE_WIDTH, ENEMIE_HEIGHT))

# -----------HEART---------
HEART = pygame.transform.scale(pygame.image.load("./assets/heart.png"), (HEART_WIDTH, HEART_HEIGHT))


def draw(x, y, bullets, enemies, enemie_bullets, live, score, hearts):
    text = label.render(str(live), True, (255, 255, 255))
    point = label.render(str(score), True, (255, 255, 255))
    WIN.blit(BG, (0, 0))
    WIN.blit(text, (50, 50))
    WIN.blit(point, (WIN_WIDTH - 75 - 20*len(str(score)), 50))

    if bullets:
        for bullet in bullets:
            BULLET = pygame.Rect(
                bullet[0], bullet[1], BULLET_WIDTH, BULLET_HEIGHT)
            pygame.draw.rect(WIN, BULLET_COLOR, BULLET)

    if enemie_bullets:
        for eBullet in enemie_bullets:
            en_bullet = pygame.Rect(
                eBullet[0], eBullet[1], BULLET_WIDTH, BULLET_HEIGHT)
            pygame.draw.rect(WIN, ENEMIE_BULLET_COLOR, en_bullet)

    if enemies:
        for enemie in enemies:
            WIN.blit(E_SHIP, (enemie[0], enemie[1]))

    if hearts:
        for heart in hearts:
            if hearts[heart] != "101":
                WIN.blit(HEART, (hearts[heart][0], hearts[heart][1]))

    WIN.blit(SHIP, (x, y))

    pygame.display.update()


def main():
    alive = True
    ship_x = WIN_WIDTH // 2 - SHIP_WIDTH // 2
    ship_y = WIN_HEIGHT // 2 - SHIP_HEIGHT // 2
    clock = pygame.time.Clock()
    bullet_cooldown = 0
    enemie_spawn = 0
    shot_bullet = 0
    bullets = []
    enemie_bullets = []
    enemies = []
    hearts = {}
    enemie_cooldown = 2000
    enemie_bullet_cooldown = 2000
    last = 0
    live = 5
    score = 0
    hr = 0
    VEL_HEART_X = 1
    VEL_HEART_Y = 0.5
    x = 0

    while alive:
        spawn_heart = random.randint(0,1)
        clock.tick(FPS)
        now = pygame.time.get_ticks()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                alive = False

        key_pressed = pygame.key.get_pressed()
        #-------------------MOVEMENT------------------
        if key_pressed[pygame.K_UP] and ship_y >= 0 + SHIP_HEIGHT // 1.5:  # Up
            ship_y -= VEL_SHIP

        if key_pressed[pygame.K_DOWN] and ship_y <= WIN_HEIGHT - 1.5 * SHIP_HEIGHT:  # Down
            ship_y += VEL_SHIP

        if key_pressed[pygame.K_RIGHT] and ship_x <= WIN_WIDTH - SHIP_WIDTH * 1.5:  # Right
            ship_x += VEL_SHIP

        if key_pressed[pygame.K_LEFT] and ship_x >= 0 + SHIP_WIDTH // 1.5:  # Left
            ship_x -= VEL_SHIP

        #----------------SHOT THE BULLET----------------
        if key_pressed[pygame.K_SPACE] and now - bullet_cooldown >= 200:
            bullets.append([ship_x + SHIP_HEIGHT // 2 -
                           BULLET_WIDTH // 2, ship_y - BULLET_HEIGHT])
            bullet_cooldown = now

        for bullet in bullets:
            bullet[1] -= VEL_BULLET
            if bullet[1] + BULLET_HEIGHT + 12 < 0:
                bullets.remove(bullet)

        #------------------ENEMIE SPAWN-----------------
        if now - enemie_spawn >= enemie_cooldown:
            enemies.append([random.randint(0 + ENEMIE_WIDTH + ENEMIE_WIDTH // 2,
                WIN_WIDTH - ENEMIE_WIDTH - ENEMIE_WIDTH // 2), 0 - ENEMIE_HEIGHT])
            enemie_spawn = now

        for enemie in enemies:
            enemie[1] += VEL_ENEMIE
            if enemie[1] - ENEMIE_HEIGHT // 2 > WIN_HEIGHT:
                enemies.remove(enemie)

        if now - last > 5000:
            if enemie_cooldown > 1000:
                enemie_cooldown -= 500

            if enemie_bullet_cooldown - 500 > 200:
                enemie_bullet_cooldown -= 500
            last = now

        #--------------ENEMIES BULLETS--------------
        if now - shot_bullet >= enemie_bullet_cooldown:
            for enemie in enemies:
                enemie_bullets.append(
                    [enemie[0] + ENEMIE_WIDTH // 2 + BULLET_WIDTH // 2, enemie[1]])
            shot_bullet = now

        for bullet in enemie_bullets:
            bullet[1] += VEL_ENEMIE_BULLET
            if bullet[1] + BULLET_HEIGHT - 12 > WIN_HEIGHT:
                enemie_bullets.remove(bullet)


        # ---------------SHOT ENEMIE----------------
        for bullet in bullets:
            for enemie in enemies:
                if (enemie[0]+ENEMIE_WIDTH > bullet[0] > enemie[0] or enemie[0]+ENEMIE_WIDTH > bullet[0]+BULLET_WIDTH > enemie[0]
                    ) and enemie[1] + ENEMIE_HEIGHT >= bullet[1]:
                    score += 100
                    enemies.remove(enemie)
                    bullets.remove(bullet)
                    if spawn_heart and live + hr < 5:
                        hr += 1
                        hearts[x] = [enemie[0] + ENEMIE_WIDTH//2 - HEART_WIDTH//2, enemie[1] + ENEMIE_HEIGHT//2 - HEART_HEIGHT//2, VEL_HEART_X]
                        x += 1

        #-------------MOVE HEARTS---------------
        for h in hearts:
            if hearts[h] != "101":
                # saga ve sola hareket
                if hearts[h][0] + 1.5*HEART_WIDTH < WIN_WIDTH and hearts[h][0] > 0:
                    hearts[h][0] += hearts[h][2]
                # sagdan sekme
                if hearts[h][0] + 1.5*HEART_WIDTH > WIN_WIDTH:
                    hearts[h][2] = -hearts[h][2]
                    hearts[h][0] += hearts[h][2]
                # soldan sekme
                if hearts[h][0] <= HEART_WIDTH//2:
                    hearts[h][2] = -hearts[h][2]
                    hearts[h][0] += hearts[h][2]

                hearts[h][1] += VEL_HEART_Y

                # assagi carpma
                if hearts[h][1] > WIN_HEIGHT:
                    hearts.update({h: "101"})


        # -----------COLLECT HEART--------------
        for h in hearts:
            if hearts[h] != "101":
                if (ship_x + SHIP_WIDTH > hearts[h][0] > ship_x or ship_x + SHIP_WIDTH > hearts[h][0] + HEART_WIDTH > ship_x or
                    ship_x == hearts[h][0] or ship_x + SHIP_WIDTH == hearts[h][0] or ship_x == hearts[h][0] + HEART_WIDTH or 
                    ship_x + SHIP_WIDTH == hearts[h][0] + HEART_WIDTH) and (
                    hearts[h][1] + HEART_HEIGHT > ship_y > hearts[h][1] or hearts[h][1] + HEART_HEIGHT > ship_y + SHIP_HEIGHT > hearts[h][1]):
                    hearts.update({h: "101"})
                    live += 1
                    hr -= 1


        # ------------DROP LIVE----------------
        for enemie in enemies:
            if (ship_x+SHIP_WIDTH > enemie[0] > ship_x or ship_x+SHIP_WIDTH > enemie[0] + ENEMIE_WIDTH > ship_x or 
                ship_x+SHIP_WIDTH == enemie[0] or ship_x == enemie[0]) and (
                    enemie[1] + ENEMIE_HEIGHT > ship_y > enemie[1] or enemie[1] + ENEMIE_HEIGHT > ship_y + SHIP_HEIGHT > enemie[1]):
                    live -= 1
                    score -= 200
                    enemies.remove(enemie)

            if (enemie[1] + ENEMIE_HEIGHT >= WIN_HEIGHT):
                live -= 1
                score -= 200
                enemies.remove(enemie)

        for bullet in enemie_bullets:
            if (ship_x+SHIP_WIDTH > bullet[0] > ship_x or ship_x+SHIP_WIDTH > bullet[0] + BULLET_WIDTH > ship_x or
                ship_x+SHIP_WIDTH == bullet[0] or ship_x == bullet[0]) and (
                bullet[1] + BULLET_HEIGHT > ship_y > bullet[1] or bullet[1] + BULLET_HEIGHT > ship_y + SHIP_HEIGHT > bullet[1]):
                live -= 1
                score -= 200
                enemie_bullets.remove(bullet)


        if live <= 0:
            alive = False


        draw(ship_x, ship_y, bullets, enemies, enemie_bullets, live, score, hearts)


    pygame.quit()



if __name__ == "__main__":
    main()
