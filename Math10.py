import pygame
import random
import math
import numpy as np
from scipy.interpolate import CubicSpline

# Инициализация pygame
pygame.init()

# Параметры окна
width, height = 800, 600
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Гонка по сложной трассе")

# Количество участников и кругов
num_participants = 4  # Вы можете изменить это значение на 3-5
num_laps = 3

# Цвета участников (можно изменить на любые другие)
colors = [(255, 0, 0), (0, 255, 0), (0, 0, 255), (255, 255, 0)]

# Контрольные точки трассы
control_points = [
    (250, 100),  # Начало
    (300, 100),  # Прямо
    (300, 200),  # Налево
    (400, 200),  # Прямо
    (400, 300),  # Налево
    (500, 300),  # Прямо
    (500, 400),  # Налево
    (400, 400),  # Прямо
    (400, 500),  # Налево
    (300, 500),  # Прямо
    (300, 400),  # Налево
    (200, 400),  # Прямо
    (200, 300),  # Налево
    (100, 300),  # Прямо
    (100, 200),  # Налево
    (200, 200),  # Прямо
    (200, 100),  # Замыкание
    (250, 100)   # Дублирование первой точки для замыкания
]

# Создание сплайна для трассы
x_points = [point[0] for point in control_points]
y_points = [point[1] for point in control_points]
cs_x = CubicSpline(np.linspace(0, 1, len(x_points)), x_points, bc_type='periodic')
cs_y = CubicSpline(np.linspace(0, 1, len(y_points)), y_points, bc_type='periodic')

# Инициализация участников
participants = []
for i in range(num_participants):
    participants.append({
        'name': f'Car {i + 1}',  # Имя участника
        'position': 0,  # Начальная позиция (0 - начало трассы, 1 - конец трассы)
        'speed': random.uniform(0.001, 0.005),  # Начальная скорость
        'laps': 0  # Количество пройденных кругов
    })

# Функция для обновления позиции участника
def update_position(participant):
    participant['position'] += participant['speed']

    # Проверка на завершение круга: если позиция >= 1
    if participant['position'] >= 1:
        participant['position'] -= 1
        participant['laps'] += 1

# Функция для расчета координат участника
def calculate_coordinates(position):
    x = cs_x(position)
    y = cs_y(position)
    return int(x), int(y)

# Главный цикл игры
running = True
clock = pygame.time.Clock()
step_counter = 0

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Обновление позиций участников
    for participant in participants:
        update_position(participant)

    # Изменение скорости через каждые 10 шагов
    step_counter += 1
    if step_counter % random.randint(5, 10) == 0:
        for participant in participants:
            participant['speed'] = random.uniform(0.001, 0.005)

    # Отображение участников и трассы
    screen.fill((255, 255, 255))

    # Отображение трассы
    for i in range(1000):
        x, y = calculate_coordinates(i / 1000)
        pygame.draw.circle(screen, (0, 0, 0), (x, y), 1)

    # Отображение участников и их кругов
    for participant in participants:
        x, y = calculate_coordinates(participant['position'])
        pygame.draw.circle(screen, colors[participants.index(participant)], (x, y), 10)

        font = pygame.font.Font(None, 36)
        text = font.render(f"{participant['name']} - circle: {participant['laps']}", True, (0, 0, 0))
        screen.blit(text, (x - 50, y - 30))

    # Проверка завершения гонки: если любой участник завершил заданное количество кругов
    if any(participant['laps'] >= num_laps for participant in participants):
        running = False

    pygame.display.flip()
    clock.tick(30)

# Вывод итоговых позиций в консоль после завершения гонки
print("Итоговые позиции участников:")
for i in sorted(participants, key=lambda p: p['laps'], reverse=True):
    print(f"{i['name']}: {i['laps']} кругов")

pygame.quit()
