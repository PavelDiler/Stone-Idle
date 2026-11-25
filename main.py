import pygame
import sys
import os
import random
import math

pygame.init()

WIDTH = 640
HEIGHT = 480
FPS = 60

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Stone Clicker")

clock = pygame.time.Clock()

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
ASSETS = os.path.join(BASE_DIR, "assets")

icon = pygame.image.load(
    os.path.join(ASSETS, "icon.png")
).convert_alpha()

pygame.display.set_icon(icon)

stone_x = 400
stone_y = 130
stone_size = 200

mountain_x = 0
mountain_y = 288

money = 0

damage = 1
max_damage = 4
damage_cost = 50

stone_health = 5
max_health = 5

stone_reward = 5
reward_cost = 75

crit_chance = 10
max_crit_chance = 50
crit_chance_cost = 40

crit_multiplier = 2.0
max_crit_multiplier = 5.0
crit_multiplier_cost = 60

menu_page = 1

shake_time = 0
shake_power = 8
shake_x = 0
shake_y = 0

hit_time = 0
hit_duration = 0.12
hit_direction = 1

damage_numbers = []
particles = []

background_color = (130, 130, 130)
menu_color = (55, 75, 110)
button_color = (75, 100, 145)
disabled_color = (45, 50, 65)
white = (255, 255, 255)
gold = (255, 205, 60)

font = pygame.font.SysFont("arial", 18)
upgrade_title_font = pygame.font.SysFont("arial", 17)
upgrade_detail_font = pygame.font.SysFont("arial", 15)
page_font = pygame.font.SysFont("arial", 17)
big_font = pygame.font.SysFont("arial", 26)
damage_font = pygame.font.SysFont("arial", 26, bold=True)


def load_image(path, size=None):
    if not os.path.exists(path):
        return None

    image = pygame.image.load(path).convert_alpha()

    if size:
        image = pygame.transform.scale(image, size)

    return image


background = load_image(
    os.path.join(ASSETS, "background.png"),
    (WIDTH, HEIGHT)
)

if background:
    if hasattr(pygame.transform, "gaussian_blur"):
        background = pygame.transform.gaussian_blur(background, 5)
    else:
        small = pygame.transform.scale(background, (80, 60))
        background = pygame.transform.smoothscale(small, (WIDTH, HEIGHT))


menu_image = load_image(
    os.path.join(ASSETS, "menu.png"),
    (256, 224)
)

money_icon = load_image(
    os.path.join(ASSETS, "icons", "money.png"),
    (32, 32)
)

damage_icon = load_image(
    os.path.join(ASSETS, "icons", "damage.png"),
    (24, 24)
)

reward_icon = load_image(
    os.path.join(ASSETS, "icons", "reward.png"),
    (24, 24)
)

crit_chance_icon = load_image(
    os.path.join(ASSETS, "icons", "crit_chance.png"),
    (24, 24)
)

crit_multiplier_icon = load_image(
    os.path.join(ASSETS, "icons", "crit_multiplier.png"),
    (24, 24)
)

stones = []

for i in range(1, 6):
    path = os.path.join(ASSETS, "stones", f"stone_{i}.png")
    image = load_image(path, (stone_size, stone_size))

    if image is None:
        raise FileNotFoundError(f"Не найдена текстура: {path}")

    stones.append(image)

mountain = load_image(
    os.path.join(ASSETS, "mountain.png"),
    (256 , 192)
)

if mountain is None:
    raise FileNotFoundError("Не найдена текстура mountain.png")


def draw_background():
    if background:
        screen.blit(background, (0, 0))
    else:
        screen.fill(background_color)


def draw_stone():
    stage = max_health - stone_health
    offset = 0

    if hit_time > 0:
        offset = int(hit_direction * 6 * hit_time / hit_duration)

    screen.blit(stones[stage], (stone_x + offset, stone_y))


def create_particles(x, y, amount, critical=False):
    for i in range(amount):
        angle = random.uniform(0, math.pi * 2)
        speed = random.uniform(40, 150)

        color = (150, 150, 150)

        if critical:
            color = random.choice([
                (255, 190, 50),
                (255, 220, 100),
                (190, 190, 190)
            ])

        particles.append({
            "x": x,
            "y": y,
            "vx": math.cos(angle) * speed,
            "vy": math.sin(angle) * speed - 40,
            "life": 0.5,
            "size": random.randint(2, 5),
            "color": color
        })


def update_particles():
    for particle in particles[:]:
        particle["x"] += particle["vx"] / FPS
        particle["y"] += particle["vy"] / FPS

        particle["vy"] += 300 / FPS
        particle["life"] -= 1 / FPS

        if particle["life"] <= 0:
            particles.remove(particle)


def draw_particles():
    for particle in particles:
        pygame.draw.rect(
            screen,
            particle["color"],
            (
                int(particle["x"]),
                int(particle["y"]),
                particle["size"],
                particle["size"]
            )
        )


def draw_damage_numbers():
    for number in damage_numbers:
        color = gold if number[4] else (255, 80, 80)

        text = damage_font.render(number[0], True, color)
        text.set_alpha(int(255 * (number[3] / 0.6)))

        screen.blit(text, (number[1], number[2]))


def update_damage_numbers():
    for number in damage_numbers[:]:
        number[2] -= 1
        number[3] -= 1 / FPS

        if number[3] <= 0:
            damage_numbers.remove(number)


def draw_mountain():
    screen.blit(mountain, (mountain_x + shake_x, mountain_y + shake_y))


def draw_upgrade_row(icon, title, detail, y, color):
    icon_y = y + 57
    text_y = y + 50

    if icon is reward_icon or icon is crit_multiplier_icon:
        icon_y -= 10
        text_y -= 10

    if icon:
        screen.blit(icon, (52, icon_y))

    title_text = upgrade_title_font.render(title, True, color)
    detail_text = upgrade_detail_font.render(detail, True, color)

    screen.blit(title_text, (86, text_y))
    screen.blit(detail_text, (86, text_y + 20))


def draw_menu():
    if menu_image:
        screen.blit(menu_image, (20, 20))
    else:
        pygame.draw.rect(
            screen,
            menu_color,
            (20, 20, 256, 224),
            border_radius=10
        )

        pygame.draw.rect(
            screen,
            button_color,
            (30, 30, 236, 60),
            border_radius=8
        )

        pygame.draw.rect(
            screen,
            button_color,
            (30, 100, 236, 80),
            border_radius=8
        )

        pygame.draw.rect(
            screen,
            button_color,
            (30, 180, 236, 30),
            border_radius=6
        )

    if menu_page == 1:
        damage_available = money >= damage_cost and damage < max_damage
        reward_available = money >= reward_cost

        damage_color = white if damage_available else (150, 150, 150)
        reward_color = white if reward_available else (150, 150, 150)

        damage_detail = (
            "Цена: " + str(damage_cost)
            if damage < max_damage else "Максимум"
        )

        draw_upgrade_row(
            damage_icon,
            "Урон: " + str(damage) + "/" + str(max_damage),
            damage_detail,
            30,
            damage_color
        )

        draw_upgrade_row(
            reward_icon,
            "Награда: " + str(stone_reward),
            "Цена: " + str(reward_cost),
            100,
            reward_color
        )

    else:
        chance_available = money >= crit_chance_cost and crit_chance < max_crit_chance
        multiplier_available = money >= crit_multiplier_cost and crit_multiplier < max_crit_multiplier

        chance_color = white if chance_available else (150, 150, 150)
        multiplier_color = white if multiplier_available else (150, 150, 150)

        chance_detail = (
            "Цена: " + str(crit_chance_cost)
            if crit_chance < max_crit_chance else "Максимум"
        )

        multiplier_detail = (
            "Цена: " + str(crit_multiplier_cost)
            if crit_multiplier < max_crit_multiplier else "Максимум"
        )

        draw_upgrade_row(
            crit_chance_icon,
            "Шанс крита: " + str(crit_chance) + "%",
            chance_detail,
            30,
            chance_color
        )

        draw_upgrade_row(
            crit_multiplier_icon,
            "Сила крита: x" + str(crit_multiplier),
            multiplier_detail,
            100,
            multiplier_color
        )

    page_text = page_font.render(
        "Страница " + str(menu_page) + " / 2",
        True,
        white
    )

    page_rect = page_text.get_rect(center=(142, 195))
    screen.blit(page_text, page_rect)


def draw_money():
    if money_icon:
        screen.blit(money_icon, (385, 28))
        text = big_font.render(str(money), True, white)
        screen.blit(text, (420, 30))
    else:
        text = big_font.render("Монеты: " + str(money), True, white)
        screen.blit(text, (420, 30))


def buy_damage():
    global money, damage, damage_cost

    if money >= damage_cost and damage < max_damage:
        money -= damage_cost
        damage += 1
        damage_cost = int(damage_cost * 1.7)


def buy_reward():
    global money, stone_reward, reward_cost

    if money >= reward_cost:
        money -= reward_cost
        stone_reward += 2
        reward_cost = int(reward_cost * 1.7)


def buy_crit_chance():
    global money, crit_chance, crit_chance_cost

    if money >= crit_chance_cost and crit_chance < max_crit_chance:
        money -= crit_chance_cost
        crit_chance += 5
        crit_chance_cost = int(crit_chance_cost * 1.7)


def buy_crit_multiplier():
    global money, crit_multiplier, crit_multiplier_cost

    if money >= crit_multiplier_cost and crit_multiplier < max_crit_multiplier:
        money -= crit_multiplier_cost
        crit_multiplier = round(crit_multiplier + 0.5, 1)
        crit_multiplier_cost = int(crit_multiplier_cost * 1.7)


def hit_stone(mouse_x, mouse_y):
    global stone_health, money
    global hit_time, hit_direction
    global shake_time

    critical = random.randint(1, 100) <= crit_chance

    actual_damage = damage

    if critical:
        actual_damage = int(damage * crit_multiplier)

    stone_health -= actual_damage

    damage_numbers.append([
        "-" + str(actual_damage),
        mouse_x,
        mouse_y - 20,
        0.6,
        critical
    ])

    create_particles(mouse_x, mouse_y, 15 if critical else 7, critical)

    hit_time = hit_duration
    hit_direction = random.choice([-1, 1])

    if stone_health <= 0:
        create_particles(
            stone_x + stone_size // 2,
            stone_y + stone_size // 2,
            30,
            critical
        )

        money += stone_reward
        stone_health = max_health
        shake_time = 0.4
        hit_time = 0


running = True

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            mouse_x, mouse_y = event.pos

            stone_rect = pygame.Rect(
                stone_x, stone_y,
                stone_size, stone_size
            )

            first_button = pygame.Rect(30, 30, 236, 60)
            second_button = pygame.Rect(30, 100, 236, 80)
            page_button = pygame.Rect(30, 180, 236, 30)

            if stone_rect.collidepoint(mouse_x, mouse_y):
                hit_stone(mouse_x, mouse_y)

            elif page_button.collidepoint(mouse_x, mouse_y):
                menu_page = 2 if menu_page == 1 else 1

            elif first_button.collidepoint(mouse_x, mouse_y):
                if menu_page == 1:
                    buy_damage()
                else:
                    buy_crit_chance()

            elif second_button.collidepoint(mouse_x, mouse_y):
                if menu_page == 1:
                    buy_reward()
                else:
                    buy_crit_multiplier()

    if shake_time > 0:
        shake_time -= 1 / FPS
        shake_x = random.randint(-shake_power, shake_power)
        shake_y = random.randint(-shake_power, shake_power)
    else:
        shake_x = 0
        shake_y = 0

    if hit_time > 0:
        hit_time -= 1 / FPS
    else:
        hit_time = 0

    update_damage_numbers()
    update_particles()

    draw_background()
    draw_mountain()
    draw_menu()
    draw_stone()
    draw_particles()
    draw_damage_numbers()
    draw_money()

    pygame.display.update()
    clock.tick(FPS)

pygame.quit()
sys.exit()