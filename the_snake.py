import pygame
from random import randint

# Константы для размеров поля и сетки:
SCREEN_WIDTH = 640
SCREEN_HEIGHT = 480
GRID_SIZE = 20
GRID_WIDTH = SCREEN_WIDTH // GRID_SIZE
GRID_HEIGHT = SCREEN_HEIGHT // GRID_SIZE

# Цвета
BOARD_BACKGROUND_COLOR = (0, 0, 0)  # Заменил на черный
APPLE_COLOR = (255, 0, 0)
SNAKE_COLOR = (0, 255, 0)

# Направления движения:
UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)

# Скорость игры
SPEED = 10

# Инициализация PyGame:
pygame.init()

# Настройка игрового окна:
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Змейка. Для выхода из игры нажмите ESC.")
clock = pygame.time.Clock()


class GameObject:
    """Базовый класс игровых объектов."""

    def __init__(self, position=(0, 0), body_color=(255, 255, 255)):
        self.position = position
        self.body_color = body_color

    def draw(self):
        """Рисует объект на экране."""
        rect = pygame.Rect(self.position, (GRID_SIZE, GRID_SIZE))
        pygame.draw.rect(screen, self.body_color, rect)


class Snake(GameObject):
    """Класс змейки."""

    def __init__(self):
        initial_position = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
        super().__init__(initial_position, SNAKE_COLOR)
        self.positions = [initial_position]
        self.direction = RIGHT
        self.length = 1

    def update_direction(self, key):
        """Обновляет направление движения змейки."""
        if key == pygame.K_UP and self.direction != DOWN:
            self.direction = UP
        elif key == pygame.K_DOWN and self.direction != UP:
            self.direction = DOWN
        elif key == pygame.K_LEFT and self.direction != RIGHT:
            self.direction = LEFT
        elif key == pygame.K_RIGHT and self.direction != LEFT:
            self.direction = RIGHT

    def move(self):
        """Обновляет позицию змейки."""
        x, y = self.positions[0]
        new_position = (
            (x + self.direction[0] * GRID_SIZE) % SCREEN_WIDTH,
            (y + self.direction[1] * GRID_SIZE) % SCREEN_HEIGHT
        )
        self.positions.insert(0, new_position)
        if len(self.positions) > self.length:
            self.positions.pop()

    def draw(self):
        """Рисует змейку на экране."""
        for position in self.positions:
            rect = pygame.Rect(position, (GRID_SIZE, GRID_SIZE))
            pygame.draw.rect(screen, self.body_color, rect)

    def get_head_position(self):
        """Возвращает позицию головы змейки."""
        return self.positions[0]

    def reset(self):
        """Сбрасывает змейку в начальное состояние."""
        self.positions = [self.position]
        self.direction = RIGHT
        self.length = 1

    def check_collision(self):
        """Проверяет столкновение змейки с самой собой."""
        return self.positions[0] in self.positions[1:]


class Apple(GameObject):
    """Класс яблока."""

    def __init__(self):
        super().__init__((0, 0), APPLE_COLOR)
        self.randomize_position([])

    def randomize_position(self, busy_positions):
        """Устанавливает случайное положение яблока."""
        while True:
            self.position = (
                randint(0, GRID_WIDTH - 1) * GRID_SIZE,
                randint(0, GRID_HEIGHT - 1) * GRID_SIZE
            )
            if self.position not in busy_positions:
                break


def handle_keys(snake):
    """Обрабатывает нажатия клавиш."""
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                pygame.quit()
                exit()
            snake.update_direction(event.key)


def main():
    """Основная функция игры."""
    snake = Snake()
    apple = Apple()

    while True:
        clock.tick(SPEED)
        screen.fill(BOARD_BACKGROUND_COLOR)

        # Обработка событий
        handle_keys(snake)

        # Движение змейки
        snake.move()

        # Проверка на поедание яблока
        if snake.get_head_position() == apple.position:
            snake.length += 1
            apple.randomize_position(snake.positions)

        # Проверка на столкновение
        if snake.check_collision():
            print("Game Over!")
            snake.reset()

        # Отрисовка объектов
        snake.draw()
        apple.draw()

        # Обновление дисплея
        pygame.display.update()


if __name__ == '__main__':
    main()
