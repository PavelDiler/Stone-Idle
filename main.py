import pygame
import sys

pygame.init()

WIDTH = 800
HEIGHT = 600
FPS = 60

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Stone Clicker")

clock = pygame.time.Clock()

stone_x = 500
stone_y = 180
stone_size = 200

background_color = (130, 130, 130)
stone_color = (85, 85, 85)
mountain_color = (100, 100, 100)
menu_color = (55, 75, 110)
button_color = (75, 100, 145)
white = (255, 255, 255)

font = pygame.font.SysFont("arial", 20)


def draw_background():
    screen.fill(background_color)


def draw_stone():
    pygame.draw.circle(
        screen,
        stone_color,
        (stone_x + stone_size // 2, stone_y + stone_size // 2),
        stone_size // 2
    )


def draw_mountain():
    pygame.draw.circle(screen, mountain_color, (100, 530), 90)
    pygame.draw.circle(screen, mountain_color, (190, 540), 110)
    pygame.draw.circle(screen, mountain_color, (280, 550), 80)
    pygame.draw.circle(screen, mountain_color, (170, 460), 85)


def draw_menu():
    pygame.draw.rect(screen, menu_color, (20, 20, 270, 150), border_radius=10)

    pygame.draw.rect(screen, button_color, (30, 30, 250, 60), border_radius=8)
    pygame.draw.rect(screen, button_color, (30, 100, 250, 60), border_radius=8)

    damage_text = font.render("Увеличить урон", True, white)
    money_text = font.render("Увеличить награду", True, white)

    screen.blit(damage_text, (45, 48))
    screen.blit(money_text, (45, 118))


running = True

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    draw_background()
    draw_menu()
    draw_mountain()
    draw_stone()

    pygame.display.update()
    clock.tick(FPS)

pygame.quit()
sys.exit()
