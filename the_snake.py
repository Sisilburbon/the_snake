"""
Модуль игры "Змейка".

Реализует логику игры "Змейка" с использованием библиотеки Pygame.

Основные элементы:
- `GameObject`: Базовый класс для всех игровых объектов.
- `Snake`: Класс змейки.
- `Apple`: Класс яблока.

Основные функции:
- handle_keys : Обрабатывает нажатия клавиш.
- main : Основная функция игры.
"""
import sys
import pygame as pg
from random import randint, choice

# Константы для размеров поля и сетки:
SCREEN_WIDTH = 640
SCREEN_HEIGHT = 480
GRID_SIZE = 20
GRID_WIDTH = SCREEN_WIDTH // GRID_SIZE
GRID_HEIGHT = SCREEN_HEIGHT // GRID_SIZE

# Цвета:
BOARD_BACKGROUND_COLOR = (0, 0, 0)  # Черный
APPLE_COLOR = (255, 0, 0)  # Красный
SNAKE_COLOR = (0, 255, 0)  # Зеленый
WHITE = (255, 255, 255)    # Белый

# Направления движения:
UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)

# Скорость игры:
SPEED = 10

# Инициализация PyGame:
pg.init()

# Настройка игрового окна:
screen = pg.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pg.display.set_caption("Змейка. Для выхода из игры нажмите ESC.")
clock = pg.time.Clock()


class GameObject:
    """Базовый класс игровых объектов."""

    def __init__(self, position=(0, 0), body_color=WHITE):
        """Инициализирует игровой объект."""
        self.position = position
        self.body_color = body_color

    def draw_cell(self, position=None, color=None):
        """Рисует ячейку объекта."""
        if position is None:
            position = self.position
        if color is None:
            color = self.body_color
        rect = pg.Rect(position, (GRID_SIZE, GRID_SIZE))
        pg.draw.rect(screen, color, rect)

    def draw(self):
        """Рисует объект."""
        raise NotImplementedError


class Snake(GameObject):
    """Класс змейки."""

    def __init__(self):
        """Инициализирует змейку."""
        super().__init__((SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2), SNAKE_COLOR)
        self.positions = [self.position]
        self.direction = RIGHT
        self.length = 1

    def update_direction(self, new_direction):
        """Обновляет направление движения змейки."""
        if (new_direction == UP and self.direction != DOWN) or \
           (new_direction == DOWN and self.direction != UP) or \
           (new_direction == LEFT and self.direction != RIGHT) or \
           (new_direction == RIGHT and self.direction != LEFT):
            self.direction = new_direction

    def move(self):
        """Перемещает змейку."""
        head_x, head_y = self.get_head_position()
        new_head_position = (
            (head_x + self.direction[0] * GRID_SIZE) % SCREEN_WIDTH,
            (head_y + self.direction[1] * GRID_SIZE) % SCREEN_HEIGHT
        )
        self.positions.insert(0, new_head_position)
        if len(self.positions) > self.length:
            self.positions.pop()
        self.position = self.positions[0]

    def draw(self):
        """Рисует змейку."""
        for position in self.positions:
            self.draw_cell(position)

    def get_head_position(self):
        """Возвращает позицию головы змейки."""
        return self.positions[0]

    def check_collision(self):
        """Проверяет, столкнулась ли змейка сама с собой."""
        return self.get_head_position() in self.positions[1:]

    def reset(self):
        """Сбрасывает змейку в начальное состояние."""
        self.position = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
        self.positions = [self.position]
        self.direction = choice([UP, DOWN, LEFT, RIGHT])  # направление рандом
        self.length = 1


class Apple(GameObject):
    """Класс яблока."""

    def __init__(self, busy_positions=None):
        """Инициализирует яблоко."""
        super().__init__(body_color=APPLE_COLOR)
        self.randomize_position(busy_positions or [])

    def randomize_position(self, busy_positions):
        """Размещает яблоко в случайной позиции."""
        while True:
            self.position = (
                randint(0, GRID_WIDTH - 1) * GRID_SIZE,
                randint(0, GRID_HEIGHT - 1) * GRID_SIZE
            )
            if self.position not in busy_positions:
                break

    def draw(self):
        """Рисует яблоко."""
        self.draw_cell()


def handle_keys(snake):
    """Обрабатывает нажатия клавиш."""
    for event in pg.event.get():
        if event.type == pg.QUIT:
            pg.quit()
            sys.exit()
        elif event.type == pg.KEYDOWN:
            if event.key == pg.K_ESCAPE:
                pg.quit()
                sys.exit()
            elif event.key == pg.K_UP:
                snake.update_direction(UP)
            elif event.key == pg.K_DOWN:
                snake.update_direction(DOWN)
            elif event.key == pg.K_LEFT:
                snake.update_direction(LEFT)
            elif event.key == pg.K_RIGHT:
                snake.update_direction(RIGHT)


def main():
    """Основная функция игры."""
    snake = Snake()
    apple = Apple()
    apple.randomize_position(snake.positions)  # Яблоко не в змейке

    while True:
        clock.tick(SPEED)
        screen.fill(BOARD_BACKGROUND_COLOR)

        handle_keys(snake)
        snake.move()

        # Проверка на поедание яблока
        if snake.get_head_position() == apple.position:
            snake.length += 1
            apple.randomize_position(snake.positions)

        # Проверка на столкновение
        if snake.check_collision():
            snake.reset()
            apple.randomize_position(snake.positions)

        # Отрисовка объектов
        snake.draw()
        apple.draw()

        pg.display.update()


if __name__ == '__main__':
    main()
