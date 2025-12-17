import pygame
import random
import math

pygame.init()
pygame.mixer.init()

# ----------------- Настройки окна -----------------
screen_width, screen_height = 800, 600
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Football Game")
clock = pygame.time.Clock()

# ----------------- Звуки -----------------
try:
    kick_sound = pygame.mixer.Sound("assets/kick.wav")
except:
    kick_sound = None
    print("Файл kick.wav не найден, звук удара отключен.")

# ----------------- Загрузка изображений -----------------
try:
    field_img = pygame.image.load("soccer/field.jpg").convert()
    field_img = pygame.transform.scale(field_img, (screen_width, screen_height))

    player1_img = pygame.image.load("asset/player.png").convert_alpha()
    player1_img = pygame.transform.scale(player1_img, (80, 50))

    player2_img = pygame.image.load("asse/player2.png").convert_alpha()
    player2_img = pygame.transform.scale(player2_img, (80, 50))

    ball_img = pygame.image.load("fottball/ball.png").convert_alpha()
    ball_img = pygame.transform.scale(ball_img, (30, 30))

except:
    print("Некоторые изображения не найдены. Убедитесь, что они в папках.")
    pygame.quit()
    exit()

# ----------------- Игроки и мяч -----------------
player1_rect = player1_img.get_rect(center=(150, screen_height//2))
player2_rect = player2_img.get_rect(center=(screen_width-150, screen_height//2))
player_speed = 7
player2_speed = 7

ball_rect = ball_img.get_rect(center=(screen_width//2, screen_height//2))
ball_velocity = pygame.Vector2(0,0)
ball_speed = 12

# ----------------- Ворота -----------------
goal_width, goal_height = 10, 100
goal1 = pygame.Rect(0, screen_height//2 - goal_height//2, goal_width, goal_height)
goal2 = pygame.Rect(screen_width-10, screen_height//2 - goal_height//2, goal_width, goal_height)

# ----------------- Игровые переменные -----------------
mode = None  # "1" - против ИИ, "2" - 2 игрока
score1 = 0
score2 = 0

# ----------------- Способности -----------------
SUPER_KICK_POWER = 20
TURBO_SPEED_BOOST = 12
INVISIBILITY_TIME = 300  # кадры

SUPER_KICK_COOLDOWN = 1000
TURBO_SPEED_COOLDOWN = 500
INVISIBILITY_COOLDOWN = 500

cooldowns = {
    "super_kick1":0, "turbo_speed1":0, "invisibility1":0,
    "super_kick2":0, "turbo_speed2":0, "invisibility2":0
}

active = {
    "turbo_speed1":0, "invisibility1":0,
    "turbo_speed2":0, "invisibility2":0
}

# ----------------- Функции -----------------
def reset_ball():
    global ball_rect, ball_velocity
    ball_rect.center = (screen_width//2, screen_height//2)
    ball_velocity = pygame.Vector2(0,0)

def move_player(keys, rect, speed, controls):
    vx, vy = 0,0
    if keys[controls['up']]:
        vy = -speed
    if keys[controls['down']]:
        vy = speed
    if keys[controls['left']]:
        vx = -speed
    if keys[controls['right']]:
        vx = speed

    rect.x += vx
    rect.y += vy
    rect.clamp_ip(screen.get_rect())

def handle_player_collision(rect1, rect2):
    if rect1.colliderect(rect2):
        if rect1.centerx < rect2.centerx:
            rect1.right = rect2.left
        else:
            rect1.left = rect2.right
        if rect1.centery < rect2.centery:
            rect1.bottom = rect2.top
        else:
            rect1.top = rect2.bottom

def move_ai():
    if ball_rect.centerx > player2_rect.centerx:
        player2_rect.x += min(player2_speed, ball_rect.centerx - player2_rect.centerx)
    elif ball_rect.centerx < player2_rect.centerx:
        player2_rect.x -= min(player2_speed, player2_rect.centerx - ball_rect.centerx)
    if ball_rect.centery > player2_rect.centery:
        player2_rect.y += min(player2_speed, ball_rect.centery - player2_rect.centery)
    elif ball_rect.centery < player2_rect.centery:
        player2_rect.y -= min(player2_speed, player2_rect.centery - ball_rect.centery)
    player2_rect.clamp_ip(screen.get_rect())

def check_ball_collision(rect):
    global ball_velocity
    if rect.colliderect(ball_rect):
        dx = ball_rect.centerx - rect.centerx
        dy = ball_rect.centery - rect.centery
        distance = math.hypot(dx, dy)
        if distance == 0:
            distance = 1
        ball_velocity.x = (dx / distance) * ball_speed
        ball_velocity.y = (dy / distance) * ball_speed
        if kick_sound:
            kick_sound.play()

def update_ball():
    global ball_rect, ball_velocity
    ball_rect.x += ball_velocity.x
    ball_rect.y += ball_velocity.y

    # Отскок от стенок
    if ball_rect.left <= 0:
        ball_rect.left = 0
        ball_velocity.x = -ball_velocity.x * 0.8
    if ball_rect.right >= screen_width:
        ball_rect.right = screen_width
        ball_velocity.x = -ball_velocity.x * 0.8
    if ball_rect.top <= 0:
        ball_rect.top = 0
        ball_velocity.y = -ball_velocity.y * 0.8
    if ball_rect.bottom >= screen_height:
        ball_rect.bottom = screen_height
        ball_velocity.y = -ball_velocity.y * 0.8

    # Постепенное замедление
    ball_velocity *= 0.95
    if abs(ball_velocity.x) < 0.1:
        ball_velocity.x = 0
    if abs(ball_velocity.y) < 0.1:
        ball_velocity.y = 0

def check_goal():
    global score1, score2
    if goal1.colliderect(ball_rect):
        score2 += 1
        reset_ball()
    if goal2.colliderect(ball_rect):
        score1 += 1
        reset_ball()

def main_menu():
    global mode
    font = pygame.font.Font(None, 40)
    choosing = True
    while choosing:
        screen.fill((0,0,0))
        texts = [
            "Выберите режим игры:",
            "1. Игрок против ИИ",
            "2. Два игрока на одном ПК"
        ]
        for i,text in enumerate(texts):
            t = font.render(text, True, (255,255,255))
            screen.blit(t, (screen_width//2 - t.get_width()//2, 150 + i*60))
        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1:
                    mode = "1"
                    choosing = False
                elif event.key == pygame.K_2:
                    mode = "2"
                    choosing = False

# ----------------- Главное меню -----------------
main_menu()

# ----------------- Основной цикл -----------------
font_score = pygame.font.Font(None, 50)
font_cd = pygame.font.Font(None, 25)
running = True
while running:
    keys = pygame.key.get_pressed()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:
            # --- Игрок 1 ---
            if event.key == pygame.K_SPACE and cooldowns["super_kick1"] == 0:
                dx = ball_rect.centerx - player1_rect.centerx
                dy = ball_rect.centery - player1_rect.centery
                dist = math.hypot(dx, dy) or 1
                ball_velocity.x = (dx / dist) * SUPER_KICK_POWER
                ball_velocity.y = (dy / dist) * SUPER_KICK_POWER
                cooldowns["super_kick1"] = SUPER_KICK_COOLDOWN
                if kick_sound:
                    kick_sound.play()
            if event.key == pygame.K_LSHIFT and cooldowns["turbo_speed1"] == 0:
                active["turbo_speed1"] = TURBO_SPEED_BOOST
                cooldowns["turbo_speed1"] = TURBO_SPEED_COOLDOWN
            if event.key == pygame.K_i and cooldowns["invisibility1"] == 0:
                active["invisibility1"] = INVISIBILITY_TIME
                cooldowns["invisibility1"] = INVISIBILITY_COOLDOWN

            # --- Игрок 2 ---
            if event.key == pygame.K_RETURN and cooldowns["super_kick2"] == 0:
                dx = ball_rect.centerx - player2_rect.centerx
                dy = ball_rect.centery - player2_rect.centery
                dist = math.hypot(dx, dy) or 1
                ball_velocity.x = (dx / dist) * SUPER_KICK_POWER
                ball_velocity.y = (dy / dist) * SUPER_KICK_POWER
                cooldowns["super_kick2"] = SUPER_KICK_COOLDOWN
                if kick_sound:
                    kick_sound.play()
            if event.key == pygame.K_RCTRL and cooldowns["turbo_speed2"] == 0:
                active["turbo_speed2"] = TURBO_SPEED_BOOST
                cooldowns["turbo_speed2"] = TURBO_SPEED_COOLDOWN
            if event.key == pygame.K_p and cooldowns["invisibility2"] == 0:
                active["invisibility2"] = INVISIBILITY_TIME
                cooldowns["invisibility2"] = INVISIBILITY_COOLDOWN

    # Движение игроков
    speed1 = player_speed + (TURBO_SPEED_BOOST if active["turbo_speed1"] > 0 else 0)
    speed2 = player2_speed + (TURBO_SPEED_BOOST if active["turbo_speed2"] > 0 else 0)

    move_player(keys, player1_rect, speed1, {'up':pygame.K_w,'down':pygame.K_s,'left':pygame.K_a,'right':pygame.K_d})
    if mode == "2":
        move_player(keys, player2_rect, speed2, {'up':pygame.K_UP,'down':pygame.K_DOWN,'left':pygame.K_LEFT,'right':pygame.K_RIGHT})
    elif mode == "1":
        move_ai()

    # Коллизия игроков
    handle_player_collision(player1_rect, player2_rect)
    handle_player_collision(player2_rect, player1_rect)

    # Коллизия с мячом
    check_ball_collision(player1_rect)
    check_ball_collision(player2_rect)

    # Движение мяча
    update_ball()
    check_goal()

    # Обновление КД и активных эффектов
    for ab in cooldowns:
        if cooldowns[ab] > 0:
            cooldowns[ab] -= 1
    for ab in active:
        if active[ab] > 0:
            active[ab] -= 1

    # ----------------- Отрисовка -----------------
    screen.blit(field_img, (0,0))

    if active["invisibility1"] == 0:
        screen.blit(player1_img, player1_rect)
    if active["invisibility2"] == 0:
        screen.blit(player2_img, player2_rect)
    screen.blit(ball_img, ball_rect)

    # Счёт
    score_text = font_score.render(f"{score1} : {score2}", True, (255,255,255))
    screen.blit(score_text, (screen_width//2 - score_text.get_width()//2, 20))

    # Индикаторы КД игрока 1 слева
    cd_texts1 = [
        f"Супер удар: {cooldowns['super_kick1']//60}s",
        f"Турбо скорость: {cooldowns['turbo_speed1']//60}s",
        f"Невидимость: {cooldowns['invisibility1']//60}s"
    ]
    for i, txt in enumerate(cd_texts1):
        t = font_cd.render(txt, True, (255,255,0))
        screen.blit(t, (10, 50 + i*20))

    # Индикаторы КД игрока 2 справа
    cd_texts2 = [
        f"Супер удар: {cooldowns['super_kick2']//60}s",
        f"Турбо скорость: {cooldowns['turbo_speed2']//60}s",
        f"Невидимость: {cooldowns['invisibility2']//60}s"
    ]
    for i, txt in enumerate(cd_texts2):
        t = font_cd.render(txt, True, (0,255,255))
        screen.blit(t, (screen_width - 180, 50 + i*20))

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
