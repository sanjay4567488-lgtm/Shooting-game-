import pygame
import random
import sys

pygame.init()

screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
WIDTH, HEIGHT = screen.get_width(), screen.get_height()
pygame.display.set_caption("10 Level Shooting Game")

clock = pygame.time.Clock()

WHITE = (255,255,255)
RED = (255,0,0)
GREEN = (0,255,0)
BLUE = (0,150,255)
BLACK = (0,0,0)

player = pygame.Rect(WIDTH//2 - 30, HEIGHT - 120, 60, 60)

bullets = []
rockets = []
enemies = []

bullet_speed = 14
rocket_speed = 10

score = 0
level = 1
rockets_available = 0

font = pygame.font.SysFont(None, 42)
dragging = False

def spawn_enemy():
size = 40 + level * 3
speed = 3 + level
x = random.randint(20, WIDTH - size - 20)
enemy = pygame.Rect(x, -size, size, size)
return enemy, speed

enemy, enemy_speed = spawn_enemy()
enemies.append(enemy)

while True:
clock.tick(60)
screen.fill(BLACK)

for event in pygame.event.get():  
    if event.type == pygame.QUIT:  
        pygame.quit()  
        sys.exit()  

    if event.type == pygame.MOUSEBUTTONDOWN:  
        dragging = True  
        bullets.append(pygame.Rect(player.centerx-4, player.top, 8, 20))  

        if rockets_available > 0:  
            rockets.append(pygame.Rect(player.centerx-10, player.top-25, 20, 35))  
            rockets_available -= 1  

    if event.type == pygame.MOUSEBUTTONUP:  
        dragging = False  

    if event.type == pygame.MOUSEMOTION and dragging:  
        player.centerx = event.pos[0]  
        player.left = max(player.left, 0)  
        player.right = min(player.right, WIDTH)  

# move bullets  
for bullet in bullets[:]:  
    bullet.y -= bullet_speed  
    if bullet.bottom < 0:  
        bullets.remove(bullet)  

for rocket in rockets[:]:  
    rocket.y -= rocket_speed  
    if rocket.bottom < 0:  
        rockets.remove(rocket)  

# enemy move  
for enemy in enemies[:]:  
    enemy.y += enemy_speed  
    if enemy.top > HEIGHT:  
        pygame.quit()  
        sys.exit()  

    for bullet in bullets[:]:  
        if enemy.colliderect(bullet):  
            bullets.remove(bullet)  
            enemies.remove(enemy)  
            score += 1  

            if score % 5 == 0:  
                rockets_available += 1  

            # LEVEL UP  
            if score % 10 == 0 and level < 10:  
                level += 1  

            enemy, enemy_speed = spawn_enemy()  
            enemies.append(enemy)  
            break  

    for rocket in rockets[:]:  
        if enemy.colliderect(rocket):  
            rockets.remove(rocket)  
            enemies.remove(enemy)  
            score += 1  
            enemy, enemy_speed = spawn_enemy()  
            enemies.append(enemy)  
            break  

pygame.draw.rect(screen, GREEN, player)  

for bullet in bullets:  
    pygame.draw.rect(screen, WHITE, bullet)  

for rocket in rockets:  
    pygame.draw.rect(screen, BLUE, rocket)  

for enemy in enemies:  
    pygame.draw.rect(screen, RED, enemy)  

screen.blit(font.render(f"Score : {score}", True, WHITE), (20,20))  
screen.blit(font.render(f"Level : {level}/10", True, BLUE), (20,70))  
screen.blit(font.render(f"Rockets : {rockets_available}", True, BLUE), (20,120))  

pygame.display.update()
