import pygame
import random

from pygame.draw import rect


pygame.init()

# -----------COLORS----------
BULLET_COLOR = (255, 0, 0)

# ----------VALUES-----------
FPS = 60
VEL_SHIP = 6
VEL_ENEMIE = 3
VEL_BULLET = 5
VEL_ENEMIE_BULLET = 5
BULLET_WIDTH = 5
BULLET_HEIGHT = 24

# ---------WIN SIZES---------
WIN_WIDTH = 500
WIN_HEIGHT = 700
WIN = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT))

# -------SHIP SIZES---------
SHIP_WIDTH = 55
SHIP_HEIGHT = 55
ENEMIE_WIDTH = 50
ENEMIE_HEIGHT = 50

# -------------BG------------
BG_IMAGE = pygame.image.load("./assets/space.png")
BG = pygame.transform.scale(BG_IMAGE, (WIN_WIDTH, WIN_HEIGHT))

#-----------SPACESHIP-------
SHIP_IMAGE = pygame.image.load("./assets/spaceship.png")
SHIP = pygame.transform.scale(SHIP_IMAGE, (SHIP_WIDTH, SHIP_HEIGHT))


def draw(x, y, bullets, enemies, enemie_bullets):
    WIN.blit(BG, (0, 0))
    
    if bullets:
        for bullet in bullets:
            BULLET = pygame.Rect(bullet[0], bullet[1], BULLET_WIDTH, BULLET_HEIGHT)
            pygame.draw.rect(WIN, BULLET_COLOR, BULLET)
    
    if enemie_bullets:
    	for eBullet in enemie_bullets:
    		en_bullet = pygame.Rect(eBullet[0], eBullet[1], BULLET_WIDTH, BULLET_HEIGHT)
    		pygame.draw.rect(WIN, BULLET_COLOR, en_bullet)

    if enemies:
    	for enemie in enemies:
    		WIN.blit(SHIP, (enemie[0], enemie[1]))

    WIN.blit(SHIP, (x, y))

    pygame.display.update()


def main():
    alive = True
    ship_x = WIN_WIDTH//2-SHIP_WIDTH//2
    ship_y = WIN_HEIGHT//2-SHIP_HEIGHT//2
    clock = pygame.time.Clock()
    bullet_cooldown = 0
    enemie_spawn = 0
    shot_bullet = 0
    bullets = []
    enemie_bullets = []
    enemies = []
    enemie_cooldown = 2000
    last = 0
    live = 5
    
    while alive:
        clock.tick(FPS)
        now = pygame.time.get_ticks()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                alive = False

        key_pressed = pygame.key.get_pressed()
        #-------------------MOVEMENT------------------
        if key_pressed[pygame.K_UP] and ship_y >= 0 + SHIP_HEIGHT//1.5: # Up
            ship_y -= VEL_SHIP
        
        if key_pressed[pygame.K_DOWN] and ship_y <= WIN_HEIGHT - 1.5*SHIP_HEIGHT: # Down
            ship_y += VEL_SHIP
        
        if key_pressed[pygame.K_RIGHT] and ship_x <= WIN_WIDTH - SHIP_WIDTH*1.5: # Right
            ship_x += VEL_SHIP

        if key_pressed[pygame.K_LEFT] and ship_x >= 0 + SHIP_WIDTH//1.5: # Left
            ship_x -= VEL_SHIP
        
        #----------------SHOT THE BULLET----------------
        if key_pressed[pygame.K_SPACE] and now-bullet_cooldown >= 200:
            bullets.append([ship_x+SHIP_HEIGHT//2-BULLET_WIDTH//2, ship_y - BULLET_HEIGHT])
            bullet_cooldown = now

        for bullet in bullets:
        	bullet[1] -= VEL_BULLET
        	if bullet[1] + BULLET_HEIGHT + 12 < 0:
        		bullets.remove(bullet)

        #------------------ENEMIE SPAWN-----------------
        if now - enemie_spawn >= enemie_cooldown:
        	enemies.append([random.randint(0 + ENEMIE_WIDTH + ENEMIE_WIDTH//2, 
        		WIN_WIDTH - ENEMIE_WIDTH - ENEMIE_WIDTH//2), 0-ENEMIE_HEIGHT])
        	enemie_spawn = now

        for enemie in enemies:
        	enemie[1] += VEL_ENEMIE
        	if enemie[1] - ENEMIE_HEIGHT//2 > WIN_HEIGHT:
        		enemies.remove(enemie)

        if now - last > 5000:
        	if enemie_cooldown > 1500:
        		enemie_cooldown -= 500
        	last = now

        #--------------ENEMIES BULLETS--------------
        if now - shot_bullet >= 1500:
        	for enemie in enemies:
	        	enemie_bullets.append([enemie[0] + ENEMIE_WIDTH//2 + BULLET_WIDTH//2, enemie[1]])
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
        			enemies.remove(enemie)
        			bullets.remove(bullet)

        # ------------DROP LIVE----------------
        for enemie in enemies:
        	if (ship_x+SHIP_WIDTH > enemie[0] > ship_x or ship_x+SHIP_WIDTH > enemie[0] + ENEMIE_WIDTH > ship_x or 
        		ship_x+SHIP_WIDTH == enemie[0] or ship_x == enemie[0]) and (
        			ship_y - ENEMIE_HEIGHT <= enemie[1]):
        			live -= 1
        			enemies.remove(enemie)

        for bullet in enemie_bullets:
        	if (ship_x+SHIP_WIDTH > bullet[0] > ship_x or ship_x+SHIP_WIDTH > bullet[0] + BULLET_WIDTH > ship_x or
        		ship_x+SHIP_WIDTH == bullet[0] or ship_x == bullet[0]) and (
        		ship_y - BULLET_HEIGHT <= bullet[1]):
        		live -= 1
        		enemie_bullets.remove(bullet)


        if live == 0:
        	alive = False


        draw(ship_x, ship_y, bullets, enemies, enemie_bullets)


    pygame.quit()



if __name__ == "__main__":
    main()
