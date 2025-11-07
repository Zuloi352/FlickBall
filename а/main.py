import pygame

# Окно игры
screen_width, screen_height = 828, 500
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("My Game")
clock = pygame.time.Clock()

# Загрузка изображения фона
background = pygame.image.load("soccer/field.jpg")

# Загрузка и уменьшение изображения игрока
player_img = pygame.image.load("assets/player.png").convert_alpha()
player_img = pygame.transform.scale(player_img, (20, 20))
player_rect = player_img.get_rect(center=(100, 100))


enemy_img = pygame.image.load("assets/enemy.png").convert_alpha()
enemy_rect = enemy_img.get_rect(center=(100, 100))
enemy_speed = [3, 2]  # движение по X и Y
enemy_img = pygame.transform.scale(player_img, (20, 20))
enemy_rect.x += enemy_speed[0]
enemy_rect.y += enemy_speed[1]

# Основной игровой цикл
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            running = False

    keys = pygame.key.get_pressed()
    speed = 2

    if keys[pygame.K_a]:
        player_rect.x -= speed
    if keys[pygame.K_d]:
        player_rect.x += speed
    if keys[pygame.K_w]:
        player_rect.y -= speed
    if keys[pygame.K_s]:
        player_rect.y += speed

    # Ограничение движения
    if player_rect.left < 0:
        player_rect.left = 0
    if player_rect.right > screen_width:
        player_rect.right = screen_width
    if player_rect.top < 0:
        player_rect.top = 0
    if player_rect.bottom > screen_height:
        player_rect.bottom = screen_height

    # Отрисовка
    screen.blit(background, (0, 0))
    screen.blit(player_img, player_rect)

    pygame.display.flip()
    clock.tick(60)

pygame.quit()