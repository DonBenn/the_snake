from random import choice, randint

import pygame


SCREEN_WIDTH, SCREEN_HEIGHT = 640, 480
GRID_SIZE = 20
GRID_WIDTH = SCREEN_WIDTH // GRID_SIZE
GRID_HEIGHT = SCREEN_HEIGHT // GRID_SIZE
SCREEN_CENTER = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)

UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)

BOARD_BACKGROUND_COLOR = (0, 0, 0)

BORDER_COLOR = (93, 216, 228)

APPLE_COLOR = (255, 215, 0)

SNAKE_COLOR = (202, 164, 235)

SPEED = 10

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), 0, 32)

pygame.display.set_caption("Змейка спасает этот мир! "
                           " Вверх ↑, Вниз ↓, Вправо →, Влево ←.")

clock = pygame.time.Clock()


class GameObject:
    """Родительский класс игры"""

    def __init__(self, color=None):
        """Метод инициализации"""
        self.body_color = color
        self.position = SCREEN_CENTER

    def draw(self):
        """Метод отрисовки на игровом поле"""
        pass

    def draw_cell(self):
        """Meтод отрисовки"""
        rect = pygame.Rect(self.position, (GRID_SIZE, GRID_SIZE))
        pygame.draw.rect(screen, self.body_color, rect)
        pygame.draw.rect(screen, BORDER_COLOR, rect, 1)


class Snake(GameObject):
    """Наследуемый класс - змейка"""

    def __init__(self):
        """Инициализация класса"""
        super().__init__(color=SNAKE_COLOR)
        self.next_direction = None
        self.direction = RIGHT
        self.length = 1
        self.positions = [self.position]
        self.last = None

    def draw(self):
        """Метод отрисовки змейки"""
        for self.position in self.positions[:-1]:
            super().draw_cell()

        head_rect = pygame.Rect(self.positions[0], (GRID_SIZE, GRID_SIZE))
        pygame.draw.rect(screen, self.body_color, head_rect)
        pygame.draw.rect(screen, BORDER_COLOR, head_rect, 1)

        if self.last:
            last_rect = pygame.Rect(self.last, (GRID_SIZE, GRID_SIZE))
            pygame.draw.rect(screen, BOARD_BACKGROUND_COLOR, last_rect)

    def update_direction(self):
        """Метод обновления движения змейки"""
        if self.next_direction:
            self.direction = self.next_direction
            self.next_direction = None

    def get_head_position(self):
        """Метод получения начальной позиции змейки"""
        return self.positions[0]

    def move(self):
        """Метод движения змейки по игровому полю"""
        head = self.get_head_position()
        new_head = (
            (head[0] + self.direction[0] * GRID_SIZE) % SCREEN_WIDTH,
            (head[1] + self.direction[1] * GRID_SIZE) % SCREEN_HEIGHT,
        )
        list.insert(self.positions, 0, new_head)
        self.last = self.positions[-1]
        if len(self.positions) > self.length:
            list.pop(self.positions)

    def reset(self):
        """Метод перезагрузки змейки"""
        self.direction = choice([UP, DOWN, LEFT, RIGHT])
        self.length = 1
        self.positions = [self.position]


def handle_keys(game_object):
    """Функция обработки действий пользователя"""
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            raise SystemExit
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP and game_object.direction != DOWN:
                game_object.next_direction = UP
            elif event.key == pygame.K_DOWN and game_object.direction != UP:
                game_object.next_direction = DOWN
            elif event.key == pygame.K_LEFT and game_object.direction != RIGHT:
                game_object.next_direction = LEFT
            elif event.key == pygame.K_RIGHT and game_object.direction != LEFT:
                game_object.next_direction = RIGHT


class Apple(GameObject):
    """Наследуемый класс - яблоко"""

    def __init__(self):
        """Инициализация класса"""
        super().__init__(color=APPLE_COLOR)
        self.position = self.randomize_position()

    def draw(self):
        """Отрисовка яблока"""
        super().draw_cell()

    def randomize_position(self, occupied=SCREEN_CENTER):
        """Метод появления яблока в разных местах"""
        while True:
            apple_positions = (
                randint(0, GRID_WIDTH - 1) * GRID_SIZE,
                randint(0, GRID_HEIGHT - 1) * GRID_SIZE,
            )
            if apple_positions not in occupied:
                return apple_positions


def main():
    """Главный основной метод, в котором идёт цикл игры"""
    pygame.init()
    apple = Apple()
    snake = Snake()

    while True:

        clock.tick(SPEED)
        handle_keys(snake)
        snake.update_direction()
        snake.move()
        snake.draw()
        apple.draw()

        if snake.positions[0] == apple.position:
            list.insert(snake.positions, 0, apple.position)
            snake.length += 1
            apple.position = apple.randomize_position(snake.positions)

        if snake.positions[0] in snake.positions[2:]:
            screen.fill(BOARD_BACKGROUND_COLOR)
            snake.reset()
        pygame.display.update()


if __name__ == "__main__":
    main()
