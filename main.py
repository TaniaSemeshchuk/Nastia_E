import pygame
pygame.init()

back = (255, 193, 197)
mw = pygame.display.set_mode((500, 500))
mw.fill(back)
clock = pygame.time.Clock()

# Змінні для координат платформи
platform_x = 200
platform_y = 330

# Змінні для напрямів руху м'яча
dx = 3
dy = 3

# Флаги руху платформи
move_right = False
move_left = False

# Прапорець закінчення гри
game_over = False

# Клас для області
class Area():
    def __init__(self, x=0, y=0, width=10, height=10, color=None):
        self.rect = pygame.Rect(x, y, width, height)
        self.fill_color = back
        if color:
            self.fill_color = color

    def color(self, new_color):
        self.fill_color = new_color

    def fill(self):
        pygame.draw.rect(mw, self.fill_color, self.rect)

    def collidepoint(self, x, y):
        return self.rect.collidepoint(x, y)

    def colliderect(self, rect):
        return self.rect.colliderect(rect)

# Клас для зображень
class Picture(Area):
    def __init__(self, filename, x=0, y=0, width=10, height=10):
        super().__init__(x=x, y=y, width=width, height=height, color=None)
        self.image = pygame.image.load(filename)
        self.image = pygame.transform.scale(self.image, (width, height))

    def draw(self):
        mw.blit(self.image, (self.rect.x, self.rect.y))

# Клас для написів
class Label(Area):
    def set_text(self, text, fsize=12, text_color=(255, 253, 255)):
        self.image = pygame.font.SysFont('Verdana', fsize).render(text, True, text_color)

    def draw(self, Shift_x=0, Shift_y=0):
        self.fill()
        mw.blit(self.image, (self.rect.x + Shift_x, self.rect.y + Shift_y))

# Створення м'яча та платформи
ball = Picture('ball.png', 160, 200, 50, 50)
platform = Picture('polosaa.png', platform_x, platform_y, 50, 50)

# Створення ворогів
start_x = 5
start_y = 5
count = 60  # Змінено на 40
monsters = []
rows = 4  # Кількість рядків
cols_per_row = count // rows  # Кількість ворогів у кожному рядку

for j in range(rows):
    y = start_y + (55 * j)
    x = start_x
    for i in range(cols_per_row):
        d = Picture('hello kitty.png', x, y, 40, 40)
        monsters.append(d)
        x += 55

# Флаг для управління головним циклом гри
running = True

while running:
    ball.fill()
    platform.fill()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RIGHT:
                move_right = True
            if event.key == pygame.K_LEFT:
                move_left = True
        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_RIGHT:
                move_right = False
            if event.key == pygame.K_LEFT:
                move_left = False

    if move_right:
        platform.rect.x += 3
    if move_left:
        platform.rect.x -= 3

    ball.rect.x += dx
    ball.rect.y += dy

    if ball.rect.y < 0:
        dy *= -1
    if ball.rect.x > 450 or ball.rect.x < 0:
        dx *= -1

    if ball.rect.y > 350:
        time_text = Label(100, 150, 50, 50, back)
        time_text.set_text('YOU LOSE', 60, (163, 173, 255))
        time_text.draw(10, 10)
        game_over = True  # Змінено на закінчення гри

    if len(monsters) == 0:
        time_text = Label(100, 150, 50, 50, back)
        time_text.set_text('YOU WIN', 60, (163, 173, 255))
        time_text.draw(10, 10)
        game_over = True  # Змінено на закінчення гри

    if ball.rect.colliderect(platform.rect):
        dy *= -1

    for m in monsters[:]:  # Копіюємо список для безпечного видалення елементів
        m.draw()
        if m.rect.colliderect(ball.rect):
            monsters.remove(m)
            m.fill()
            dy *= -1

    platform.draw()
    ball.draw()

    pygame.display.update()
    clock.tick(50)

pygame.quit()
