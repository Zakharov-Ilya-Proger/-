import tkinter as tk

# Определяем размеры клетки и размеры окна
CELL_SIZE = 40
MAZE_WIDTH = 10
MAZE_HEIGHT = 10

# Определяем лабиринт
maze = [
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
    [0, 0, 0, 0, 0, 1, 0, 0, 0, 1],
    [1, 1, 1, 1, 0, 1, 1, 1, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 1, 1, 1, 1, 0, 1, 1, 0, 1],
    [1, 0, 0, 0, 0, 0, 1, 0, 0, 1],
    [1, 0, 1, 1, 1, 1, 1, 0, 1, 1],
    [1, 0, 0, 0, 0, 1, 1, 1, 1, 1],
    [1, 1, 1, 1, 0, 0, 0, 0, 0, 1],
    [1, 1, 1, 1, 1, 1, 1, 1, 0, 1]
]

# Начальные координаты игрока (можно изменить на любую допустимую позицию)
player_x = player_y = (5, 5)  # Начинаем с позиции (5,5), которая свободна


class MazeGame:
    def __init__(self):
        self.window = tk.Tk()
        self.window.title("Maze Game")

        # Создаем два канваса
        self.canvas_maze = tk.Canvas(self.window,
                                     width=MAZE_WIDTH * CELL_SIZE,
                                     height=MAZE_HEIGHT * CELL_SIZE)
        self.canvas_maze.pack(side=tk.LEFT)

        self.canvas_path = tk.Canvas(self.window,
                                     width=MAZE_WIDTH * CELL_SIZE,
                                     height=MAZE_HEIGHT * CELL_SIZE,
                                     bg="black")
        self.canvas_path.pack(side=tk.RIGHT)

        self.path_points = []  # Список для хранения пройденного пути
        self.path_points.append(player_x)  # Добавляем начальную позицию в путь

        self.draw_maze()
        self.draw_path()  # Рисуем начальную позицию на правом канвасе
        self.window.bind("<Key>", self.on_key_press)
        self.window.mainloop()

    def draw_maze(self):
        self.canvas_maze.delete("all")  # Очистка канваса лабиринта
        for y in range(len(maze)):
            for x in range(len(maze[y])):
                if maze[y][x] == 1:
                    self.canvas_maze.create_rectangle(x * CELL_SIZE,
                                                      y * CELL_SIZE,
                                                      (x + 1) * CELL_SIZE,
                                                      (y + 1) * CELL_SIZE,
                                                      fill="black")  # Стена
                elif (x == player_x[0] and y == player_x[1]):
                    self.canvas_maze.create_rectangle(x * CELL_SIZE,
                                                      y * CELL_SIZE,
                                                      (x + 1) * CELL_SIZE,
                                                      (y + 1) * CELL_SIZE,
                                                      fill="blue")  # Игрок

    def draw_path(self):
        # Отрисовка пройденного пути на втором канвасе
        for point in self.path_points:
            x, y = point
            self.canvas_path.create_rectangle(x * CELL_SIZE,
                                              y * CELL_SIZE,
                                              (x + 1) * CELL_SIZE,
                                              (y + 1) * CELL_SIZE,
                                              fill="red")  # Пройденный путь

    def on_key_press(self, event):
        global player_x
        new_x = player_x[0]
        new_y = player_x[1]

        if event.keysym == "Up":
            new_y -= 1
        elif event.keysym == "Down":
            new_y += 1
        elif event.keysym == "Left":
            new_x -= 1
        elif event.keysym == "Right":
            new_x += 1

        # Проверка на допустимость нового положения
        if (new_x >= 0 and new_x < len(maze[0]) and
                new_y >= 0 and new_y < len(maze) and
                maze[new_y][new_x] == 0):
            player_x = (new_x, new_y)

            # Добавляем новую позицию в список пройденного пути
            if player_x not in self.path_points:
                self.path_points.append(player_x)
                self.draw_path()  # Обновляем путь на втором канвасе

        self.draw_maze()


if __name__ == "__main__":
    MazeGame()