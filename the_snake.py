import pygame
from random import randint
import sys

# Константы для размеров поля и сетки:
SCREEN_WIDTH, SCREEN_HEIGHT = 640, 480
GRID_SIZE = 20
GRID_WIDTH = SCREEN_WIDTH // GRID_SIZE
GRID_HEIGHT = SCREEN_HEIGHT // GRID_SIZE

# Направления движения:
UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)

# Цвета:
BOARD_BACKGROUND_COLOR = (0, 0, 0)
BORDER_COLOR = (93, 216, 228)
APPLE_COLOR = (255, 0, 0)
SNAKE_COLOR = (0, 255, 0)

# Скорость движения змейки:
SPEED = 12


class GameObject:
    """Базовый класс для игровых объектов"""

    def __init__(self, position=(0, 0), body_color=(255, 255, 255)):
        """Инициализация игрового объекта"""
        self.position = position
        self.body_color = body_color  # Цвет объекта

    def draw(self, screen):
        """Отрисовка игрового объекта"""
        rect = pygame.Rect(self.position, (GRID_SIZE, GRID_SIZE))
        pygame.draw.rect(screen, self.body_color, rect)
        pygame.draw.rect(screen, BORDER_COLOR, rect, 1)


class Apple(GameObject):
    """Класс яблока"""

    def __init__(self):
        """Инициализация яблока"""
        super().__init__((0, 0), APPLE_COLOR)
        self.randomize_position()

    def randomize_position(self):
        """Случайное позиционирование яблока"""
        self.position = (
            randint(0, GRID_WIDTH - 1) * GRID_SIZE,
            randint(0, GRID_HEIGHT - 1) * GRID_SIZE,
        )


class Snake(GameObject):
    """Класс змейки"""

    def __init__(self):
        """Инициализация змейки"""
        super().__init__((SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2), SNAKE_COLOR)
        self.positions = [self.position]  # Список координат сегментов тела
        self.direction = RIGHT  # Начальное направление
        self.next_direction = None  # Следующее направление
        self.length = 1  # Начальная длина змейки

    def get_head_position(self):
        """Получение позиции головы змейки"""
        return self.positions[0]

    def turn(self, point):
        """Поворот змейки"""
        opposite_direction = (point[0] * -1, point[1] * -1)
        if self.length > 1 and self.direction == opposite_direction:
            return  # Игнорируем попытку движения в противоположную сторону
        self.next_direction = point

    def move(self):
        """Движение змейки"""
        cur = self.get_head_position()
        x, y = self.direction
        new = (
            (cur[0] + (x * GRID_SIZE)) % SCREEN_WIDTH,
            (cur[1] + (y * GRID_SIZE)) % SCREEN_HEIGHT,
        )
        # Проверка на столкновение с собой
        if len(self.positions) > 2 and new in self.positions[2:]:
            self.reset()  # Сбросить игру, если змейка столкнулась с собой
        else:
            self.positions.insert(0, new)  # Добавить новую голову
            if len(self.positions) > self.length:
                self.positions.pop()  # Удалить хвост, если длина не увеличилась

    def reset(self):
        """Сброс змейки"""
        self.length = 1
        self.positions = [self.position]
        self.direction = RIGHT
        self.next_direction = None

    def draw(self, screen):
        """Отрисовка змейки"""
        for p in self.positions:
            rect = pygame.Rect(p, (GRID_SIZE, GRID_SIZE))
            pygame.draw.rect(screen, self.body_color, rect)
            pygame.draw.rect(screen, BORDER_COLOR, rect, 1)

    def handle_keys(self):
        """Обработка нажатий клавиш"""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    self.turn(UP)
                elif event.key == pygame.K_DOWN:
                    self.turn(DOWN)
                elif event.key == pygame.K_LEFT:
                    self.turn(LEFT)
                elif event.key == pygame.K_RIGHT:
                    self.turn(RIGHT)