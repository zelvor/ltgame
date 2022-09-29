import pygame
import random
import math
from dataclasses import dataclass

pygame.init()

width = 800
height = 600

bg_image = pygame.image.load("images/boardgreen.jpg")
bg_image = pygame.transform.scale(bg_image, (width, height))
screen = pygame.display.set_mode((width, height))

bonk_music = pygame.mixer.Sound("musics/bonk.mp3")

pygame.mouse.set_visible(False)

hammer_image = pygame.image.load("images/bat.png").convert()
hammer_image.set_colorkey((255, 255, 255))
hammer_image = pygame.transform.scale(hammer_image, (100, 100))
hammer_status = hammer_image
hammered_image = pygame.transform.rotate(hammer_image, 45)

enemy_image = pygame.image.load("images/cheems.png").convert()
enemy_image.set_colorkey((255, 255, 255))
enemy_image = pygame.transform.scale(enemy_image, (140, 140))

enemy_image_bonked = pygame.image.load("images/cheems_bonked.png").convert()
enemy_image_bonked.set_colorkey((255, 255, 255))
enemy_image_bonked = pygame.transform.scale(enemy_image_bonked, (140, 140))

score_value = 0
font = pygame.font.Font('freesansbold.ttf', 32)

textX = 10
textY = 10

enemies = []

clicked_number = 0

NUM_COL = 3
NUM_ROW = 3

TIME = 60 * 1000

ENEMY_LIFE_SPAN = 3 * 1000
@dataclass
class Enemy:
    x: int
    y: int
    life: int = ENEMY_LIFE_SPAN
    image: pygame.Surface = enemy_image

ENEMY_RADIUS = min(enemy_image.get_width(), enemy_image.get_height()) // 2.5
ENEMY_COLOR = (255, 0, 0)
GENERATE_ENEMY, APPEAR_INTERVAL = pygame.USEREVENT + 1, 2 * 1000
pygame.time.set_timer(GENERATE_ENEMY, APPEAR_INTERVAL)
AGE_ENEMY, AGE_INTERVAL = pygame.USEREVENT + 2, 1 * 1000
pygame.time.set_timer(AGE_ENEMY, AGE_INTERVAL)

possible_enemy_pos = [(95,95), (330,95), (565,95), (95,230), (330,230), (565,230), (95,365), (330,365), (565,365)]

def check_exist(pos):
    for enemy in enemies:
        if pos == (enemy.x, enemy.y):
            return True
    return False

def generate_next_enemy_pos():
    new_pos = ()
    while True:
        grid_index = random.randint(0, NUM_ROW * NUM_COL - 1)
        new_pos = possible_enemy_pos[grid_index]
        if not check_exist(new_pos):
            break
    return new_pos


def draw_enemies():
    for enemy in enemies:
        screen.blit(enemy.image, (enemy.x, enemy.y))


def show_score(x, y):
    global score_value
    score = font.render("Score: " + str(score_value), True, (0, 0, 0))
    screen.blit(score, (x, y))
    if clicked_number != 0:
        percent = font.render("Percent: " + str('%.2f'%(score_value / clicked_number * 100)) + "%", True, (0, 0, 0))
        screen.blit(percent, (x, y + 40))

def show_timeleft(x, y):
    timeleft = font.render("Time: " + str('%.0f'%(TIME//1000)), True, (0, 0, 0))
    screen.blit(timeleft, (x, y))


def check_enemy_collision(clickX, clickY, enemyX, enemyY):
    enemyX, enemyY = enemyX + ENEMY_RADIUS, enemyY + ENEMY_RADIUS
    distance = math.sqrt(math.pow(enemyX - clickX, 2) + (math.pow(enemyY - clickY, 2)))
    return distance < ENEMY_RADIUS


def check_enemies_collision(click_pos, enemies):
    for enemy in enemies:
        if check_enemy_collision(click_pos[0], click_pos[1], enemy.x, enemy.y):
            enemy.image = enemy_image_bonked
            global score_value
            score_value += 1
            enemies.remove(enemy)

def age_enemies():
    for enemy in enemies:
        enemy.life = enemy.life-1000

def remove_died_enemies():
    for enemy in enemies:
        if enemy.life == 0:
            enemies.remove(enemy)

running = True
start_ticks = pygame.time.get_ticks()
while running and TIME > 0:
    seconds = (pygame.time.get_ticks()-start_ticks)/1000
    TIME = 60 * 1000 - seconds * 1000
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            clicked_number += 1
            click_pos = pygame.mouse.get_pos()
            bonk_music.play()
            check_enemies_collision(click_pos, enemies)
            #rotate hammer image
            hammer_status = hammered_image
        if event.type == pygame.MOUSEBUTTONUP:
            hammer_status = hammer_image
        if event.type == AGE_ENEMY:
            age_enemies()
            remove_died_enemies()
        if event.type == GENERATE_ENEMY:
            if len(enemies) < NUM_COL * NUM_ROW:
                new_pos = generate_next_enemy_pos()
                print(new_pos)
                enemies.append(Enemy(new_pos[0], new_pos[1]))
    screen.blit(bg_image, (0, 0))
    mx, my = pygame.mouse.get_pos()
    screen.blit(hammer_status, (mx, my))
    draw_enemies()
    show_score(textX, textY)
    show_timeleft(textX, textY + 80)
    pygame.display.update()