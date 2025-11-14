import pygame

# Инициализация pygame
pygame.init()

# Инициализация звукового модуля
pygame.mixer.init(frequency=44100, size=-16, channels=2, buffer=512)

# Окно игры
screen_width, screen_height = 509, 360
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("My Game")
clock = pygame.time.Clock()

# Загрузка фона
background = pygame.image.load("soccer/field.jpg")

# Загрузка звука удара
kick_sound = pygame.mixer.Sound("assets/kick.mpeg")  # можно заменить на .wav

# Загрузка оригинального изображения игрока
player_original = pygame.image.load("assets/player.png").convert_alpha()

# Начальный размер игрока
player_scale = 1.0
player_img = player_original
player_rect = player_img.get_rect(center=(screen_width // 2, screen_height // 2))


def rescale_player(scale):
    """Масштабирует игрока и сохраняет центр"""
    global player_img, player_rect, player_scale

    old_center = player_rect.center
    width = int(player_original.get_width() * scale)
    height = int(player_original.get_height() * scale)

    # Защита от слишком маленьких размеров
    width = max(5, width)
    height = max(5, height)

    player_img = pygame.transform.scale(player_original, (width, height))
    player_rect = player_img.get_rect(center=old_center)


# Основной цикл
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False

            # Увеличение размера ]
            if event.key == pygame.K_RIGHTBRACKET:
                player_scale += 0.1
                rescale_player(player_scale)

            # Уменьшение размера [
            if event.key == pygame.K_LEFTBRACKET:
                player_scale = max(0.1, player_scale - 0.1)
                rescale_player(player_scale)

            # Удар мяча (звук)
            if event.key == pygame.K_SPACE:
                kick_sound.play()

    # Движение
    keys = pygame.key.get_pressed()
    speed = 5

    if keys[pygame.K_a]:
        player_rect.x -= speed
    if keys[pygame.K_d]:
        player_rect.x += speed
    if keys[pygame.K_w]:
        player_rect.y -= speed
    if keys[pygame.K_s]:
        player_rect.y += speed

    # Ограничения
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
