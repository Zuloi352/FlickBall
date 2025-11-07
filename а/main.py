import pygame
pygame.init()

# Окно игры
screen = pygame.display.set_mode((1600, 1600))  # окно 800x600
pygame.display.set_caption("My Game")  # заголовок окна
clock = pygame.time.Clock()  # контроль FPS

# Загрузка изображения игрока
player_img = pygame.image.load("assets/player.png").convert_alpha()
player_rect = player_img.get_rect(center=(5000, 5000))

# Основной игровой цикл
running = True
while running:
    # Обработка событий
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            running = False

    # Получение состояния клавиш
    keys = pygame.key.get_pressed()
    speed = 1000

    # Движение игрока с помощью клавиш W, A, S, D
    if keys[pygame.K_a]:  # движение влево (A)
        player_rect.x -= speed
    if keys[pygame.K_d]:  # движение вправо (D)
        player_rect.x += speed
    if keys[pygame.K_w]:  # движение вверх (W)
        player_rect.y -= speed
    if keys[pygame.K_s]:  # движение вниз (S)
        player_rect.y += speed

    # Ограничение перемещения игрока в пределах экрана
    if player_rect.left < 0:
        player_rect.left = 0
    if player_rect.right > 1600:
        player_rect.right = 1600
    if player_rect.top < 0:
        player_rect.top = 0
    if player_rect.bottom > 1600:
        player_rect.bottom = 1600

    # Отображение фона и игрока
    screen.fill((30, 30, 30))  # фон
    screen.blit(player_img, player_rect)  # рисуем игрока

    # Обновляем экран
    pygame.display.flip()
    clock.tick(10000000000000000000000000000000000000000000000000000000000000000000000000000000)  # 60 кадров в секунду

pygame.quit()
