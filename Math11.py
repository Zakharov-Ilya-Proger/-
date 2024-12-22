import pygame
import random

# Инициализация Pygame
pygame.init()

# Константы
WIDTH, HEIGHT = 800, 600
FPS = 60
SPACESHIP_SPEED = 5
ROCKET_SPEED = 10
COMET_SPEED = 3

# Цвета
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLACK = (0, 0, 0)

# Загрузка фона
background = pygame.image.load('img/img.png')
background = pygame.transform.scale(background, (WIDTH, HEIGHT))

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Звездоплюй против комет")

class Spaceship:
    def __init__(self):
        self.rect = pygame.Rect(WIDTH // 2 - 25, HEIGHT - 50, 50, 30)

    def move(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and self.rect.left > 0:
            self.rect.x -= SPACESHIP_SPEED
        if keys[pygame.K_RIGHT] and self.rect.right < WIDTH:
            self.rect.x += SPACESHIP_SPEED

    def draw(self):
        pygame.draw.rect(screen, WHITE, self.rect)

class Rocket:
    def __init__(self, x):
        self.x = x
        self.y = HEIGHT - 60
        self.width = 10
        self.height = 20

    def move(self):
        self.y -= ROCKET_SPEED

    def draw(self):
        points = [
            (self.x, self.y),
            (self.x + self.width // 2, self.y - self.height),
            (self.x + self.width, self.y)
        ]
        pygame.draw.polygon(screen, RED, points)

    def get_rect(self):
        return pygame.Rect(self.x, self.y - self.height, self.width, self.height)

class Comet:
    def __init__(self):
        self.x = random.randint(0, WIDTH - 30)
        self.y = 0
        self.radius = 15
        self.trail = []

    def move(self):
        self.y += COMET_SPEED
        self.trail.append((self.x + self.radius, self.y + self.radius))
        if len(self.trail) > 10:  # Ограничиваем длину следа
            self.trail.pop(0)

    def draw(self):
        # Рисуем комету
        pygame.draw.circle(screen, GREEN, (self.x + self.radius, self.y + self.radius), self.radius)

        # Рисуем полупрозрачный след
        for i, (tx, ty) in enumerate(self.trail):
            alpha = 255 - (i * 25)  # Уменьшаем прозрачность следа
            color = (0, 255, 0, alpha)
            trail_surface = pygame.Surface((self.radius * 2, self.radius * 2), pygame.SRCALPHA)
            pygame.draw.circle(trail_surface, color, (self.radius, self.radius), self.radius // 2)
            screen.blit(trail_surface, (tx - self.radius, ty - self.radius))

    def get_rect(self):
        return pygame.Rect(self.x, self.y, self.radius * 2, self.radius * 2)

def main():
    clock = pygame.time.Clock()
    spaceship = Spaceship()
    rockets = []
    comets = []
    score = 0

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and len(rockets) < 3:
                    rockets.append(Rocket(spaceship.rect.centerx))

        spaceship.move()

        for rocket in rockets[:]:
            rocket.move()
            if rocket.y < 0:
                rockets.remove(rocket)

        for comet in comets[:]:
            comet.move()
            if comet.y > HEIGHT:
                comets.remove(comet)
                score += 1

        for comet in comets[:]:
            if spaceship.rect.colliderect(comet.get_rect()):
                print("Игра окончена! Ваш счет:", score)
                running = False

            for rocket in rockets[:]:
                if rocket.get_rect().colliderect(comet.get_rect()):
                    rockets.remove(rocket)
                    comets.remove(comet)
                    score += 5

        if random.randint(1, 20) == 1:
            comets.append(Comet())

        screen.blit(background, (0, 0))
        spaceship.draw()

        for rocket in rockets:
            rocket.draw()

        for comet in comets:
            comet.draw()

        font = pygame.font.Font(None, 36)
        score_text = font.render(f"Счет: {score}", True, WHITE)
        screen.blit(score_text, (10, 10))

        pygame.display.flip()
        clock.tick(FPS)

    pygame.quit()

if __name__ == "__main__":
    main()
