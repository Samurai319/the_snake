from random import choice, randint

import pygame

# Константы для размеров поля и сетки:
SCREEN_WIDTH, SCREEN_HEIGHT = 640, 480
GRID_SIZE = 15
GRID_WIDTH = SCREEN_WIDTH // GRID_SIZE
GRID_HEIGHT = SCREEN_HEIGHT // GRID_SIZE

# Направления движения:
UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)

KEY_TO_DIRECTION = {
    pygame.K_UP: UP,
    pygame.K_DOWN: DOWN,
    pygame.K_LEFT: LEFT,
    pygame.K_RIGHT: RIGHT,
}

# Цвета игрового поля и объектов
BOARD_BACKGROUND_COLOR = (0, 0, 0)
BORDER_COLOR = (93, 216, 228)
APPLE_COLOR = (255, 0, 0)
SNAKE_COLOR = (0, 255, 0)

# Скорость движения змейки:
SPEED = 15

# Настройка игрового окна:
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), 0, 32)
pygame.display.set_caption('Змейка')

# Настройка времени:
clock = pygame.time.Clock()

# Начальная позиция игры и змеи
POSITION_GAME = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
POSITION_SNAKE = (GRID_WIDTH // 2, GRID_HEIGHT // 2)
POSITION_INITIAL = (SCREEN_WIDTH // 2 // GRID_SIZE, SCREEN_HEIGHT
                    // 2 // GRID_SIZE)


class GameObject:
    """Базовый класс игры."""

    def __init__(self):
        self.position = POSITION_GAME
        self.body_color = None

    def draw_cell(self, screen, position, color):
        """Рисует одну ячейку на экране."""
        rect = pygame.Rect(position[0] * GRID_SIZE, position[1] * GRID_SIZE,
                           GRID_SIZE, GRID_SIZE)
        pygame.draw.rect(screen, color, rect)
        pygame.draw.rect(screen, BORDER_COLOR, rect, 1)

    def draw(self, screen):
        """Реализует отрисовку объекта на экране."""


class Apple(GameObject):
    """Класс описывающий яблоко."""

    def __init__(self, occupied_positions=None):
        super().__init__()
        self.body_color = APPLE_COLOR
        self.position = None
        self.randomize_position(occupied_positions)

    def randomize_position(self, occupied_positions=None):
        """Отвечает за установку случайной позиции яблока."""
        occupied = set(occupied_positions or ())
        while True:
            candidate = (
                randint(0, GRID_WIDTH - 1),
                randint(0, GRID_HEIGHT - 1)
            )
            if candidate not in occupied:
                self.position = candidate
                break

    def draw(self, screen):
        """Предназначен для отображения яблока на игровом экране."""
        self.draw_cell(screen, self.position, self.body_color)


class Snake(GameObject):
    """Класс описывающий объект змейка."""

    def __init__(self, screen=None):
        super().__init__()
        self.screen = screen
        self.reset()

    def reset(self):
        """Используется для сброса состояния змейки."""
        initial_position = POSITION_INITIAL
        self.position = initial_position
        self.body_color = SNAKE_COLOR
        self.length = 1
        self.positions = [initial_position]
        self.direction = choice([UP, DOWN, LEFT, RIGHT])
        self.next_direction = self.direction
        self.growing = False

    def get_head_position(self):
        """Предназначена для получения текущей позиции головы змейки."""
        return self.positions[0]

    def _is_opposite_direction(self, new_direction):
        dx, dy = self.direction
        ndx, ndy = new_direction
        return dx == -ndx and dy == -ndy

    def update_direction(self, new_direction):
        """Обновляет направление движения змейки на основе нажатой клавиши."""
        if new_direction and not self._is_opposite_direction(new_direction):
            self.next_direction = new_direction

    def move(self):
        """Отвечает за движение змейки."""
        self.direction = self.next_direction
        head_x, head_y = self.positions[0]
        dx, dy = self.direction
        new_head = ((head_x + dx) % GRID_WIDTH, (head_y + dy) % GRID_HEIGHT)

        self.positions.insert(0, new_head)
        if not self.growing and len(self.positions) > self.length:
            self.positions.pop()
        else:
            self.length = len(self.positions)
            self.growing = False

        return new_head

    def grow(self):
        """Позволяет змейке увеличиваться в длину."""
        self.growing = True

    def draw(self):
        """Отвечает за визуализацию змейки на экране."""
        for segment in self.positions:
            self.draw_cell(self.screen, segment, self.body_color)


def handle_keys(snake):
    """Позволяя управлять змейкой."""
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            raise SystemExit
        if event.type == pygame.KEYDOWN and event.key in KEY_TO_DIRECTION:
            snake.update_direction(KEY_TO_DIRECTION[event.key])


def main():
    """Запускает игровой процесс."""
    # Инициализация PyGame:
    pygame.init()
    snake = Snake(screen)
    apple = Apple(snake.positions)

    while True:
        clock.tick(SPEED)
        screen.fill(BOARD_BACKGROUND_COLOR)

        handle_keys(snake)
        snake.move()

        if len(snake.positions) != len(set(snake.positions)):
            snake.reset()

        # Проверяем, съели ли яблоко
        if snake.get_head_position() == apple.position:
            snake.grow()
            apple.randomize_position(snake.positions)

        # Отрисовываем объекты:
        apple.draw(screen)
        snake.draw()

        # Обновляем экран:
        pygame.display.update()


if __name__ == '__main__':
    main()
