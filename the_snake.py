"""Реализация игры - Змейка, с использованием библиотеки Pygeme."""

from random import choice, randint

import pygame as pg

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

# Цвет фона - черный:
BOARD_BACKGROUND_COLOR = (0, 0, 0)

# Цвет границы ячейки
BORDER_COLOR = (93, 216, 228)

# Цвет яблока
APPLE_COLOR = (255, 0, 0)

# Цвет несъедобного яблока
ANOTHER_APPLE_COLOR = (127, 123, 32)

# Цвет камня
STONE_COLOR = (224, 224, 224)

# Цвет змейки
SNAKE_COLOR = (0, 255, 0)

# Начальная корость движения змейки:
INIT_SPEED = 5

# Максимальная скорость движения змейки:
MAX_SPEED = 25

# Настройка игрового окна:
screen = pg.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), 0, 32)

# Заголовок окна игрового поля:
pg.display.set_caption('Змейка')

# Настройка времени:
clock = pg.time.Clock()


# Описание классов игры.
class GameObject:
    """
    Базовый класс, игровых объектов.

    Содержит в себе два атрибута и
    один метод, которые будут наследоваться дочерними
    классами.

    :param position: Позиция объекта на игровом поле
    :type position: tuple
    :param body_color: Цвет объекта. Будет переопределен объектом класса
    :type body_color: None
    """

    def __init__(self):
        """Метод инициализации объекта."""
        self.position = ((SCREEN_WIDTH // 2), (SCREEN_HEIGHT // 2))
        self.body_color = None

    def draw(self):
        """Метод отрисовки объектов на игровом поле."""
        raise NotImplementedError(
            'Метод должен быть реализован в дочернем классе.'
        )


class PhysicalObject(GameObject):
    """
    Промежуточный базовый класс, для физицеских объектов на игровом поле.

    Представляет общие методы отрисовки на экране, и генерацию случайной
    позиции при создании, исключая занятые клетки.

    :param position: Позиция объекта на игровом поле.
    :type position: tuple
    :param body_color: Основной цвет объекта для отрисовки.
    :type body_color: tuple
    """

    def __init__(self, occupied_positions=None):
        """Методо инициализации объекта."""
        super().__init__()
        self.randomize_position(occupied_positions or set())

    def draw(self):
        """Отрисовка физических объектов на игровом поле."""
        rect = pg.Rect(self.position, (GRID_SIZE, GRID_SIZE))
        pg.draw.rect(screen, self.body_color, rect)
        pg.draw.rect(screen, BORDER_COLOR, rect, 1)

    def randomize_position(self, occupied_positions):
        """Метод, возвращает кортеж случайных координат, в приделах сетки."""
        while True:
            value_width_x = randint(0, GRID_WIDTH - 1) * GRID_SIZE
            value_height_y = randint(0, GRID_HEIGHT - 1) * GRID_SIZE
            new_position = (value_width_x, value_height_y)

            if new_position not in occupied_positions:
                self.position = new_position
                break


class Apple(PhysicalObject):
    """
    Класс яблока - игрового объекта, который может быть съеден змейкой.

    Наследуется от класса PhysicalObject. Позиция генерируется
    случайным образом на игровом поле.

    :param position: Позиция объекта на игровом поле, определяется случайно
    :type position: tuple
    :param body_color: Цвет объекта - Яблоко
    :type body_color: tuple
    """

    def __init__(self, occupied_positions=None, body_color=APPLE_COLOR):
        """Метод инициализации объекта."""
        super().__init__(occupied_positions)
        self.body_color = body_color


class UninedibleApple(Apple):
    """
    Дочерний класс, описывает игровой объект несъедобное яблоко.

    :param position: Позиция объекта на игровом поле, определяется случайно
    :type position: tuple
    :param body_color: Цвет объекта - Несъедобное яблоко
    :type body_color: tuple
    """

    def __init__(self, occupied_positions=None):
        """Метод инициализации объекта."""
        super().__init__(occupied_positions)
        self.body_color = ANOTHER_APPLE_COLOR


class Stone(PhysicalObject):
    """
    Класс камня - статичного препятствия на игровом поле.

    Наследуется от класса PhysicalObject. При столкновении с камнем
    змейка погибает. Позиция генерируется случайным образом на игровом поле.

    :param position: Позиция объекта на игровом поле, определяется случайно
    :type position: tuple
    :param body_color: Цвет объекта - Камень
    :type body_color: tuple
    """

    def __init__(self, occupied_positions=None, body_color=STONE_COLOR):
        """Метод инициализации объекта."""
        super().__init__(occupied_positions)
        self.body_color = body_color


class Snake(GameObject):
    """
    Дочерний класс, переопределяются атрибуты и метод для объекта - Змейка.

    :param length: Длина змейки. По умолчанию значение = 1
    :type length: int
    :param positions: Спиоск позиций частей тела змейки. Начальная позиция
    центр экрана.
    :type positions: list[tuple]
    :param direction: Направление движения змейки. По умолчанию - вправо
    :type direction: tuple
    :param next_direction: следующее направление движения, применяется после
    обработки нажатия клавиш. По умолчанию - None
    :type next_direction: NoneType | tuple
    :param body_color: цвет змейки. По умолчанию - зеленый
    :type body_color: tuple
    :param last: Хранит в себе позицию последнего элемента перед тем как
    стереть его.
    :type last: None
    """

    def __init__(self):
        """Метод инициализации объекта."""
        super().__init__()
        self.body_color = SNAKE_COLOR
        self.positions = [self.position]
        self.reset()

    def update_direction(self, next_direction=None):
        """Обновляет навпрвление движения змейки."""
        if next_direction is not None:
            self.next_direction = next_direction

        if self.next_direction:
            if not ((self.direction == UP and self.next_direction == DOWN)
               or (self.direction == DOWN and self.next_direction == UP)
               or (self.direction == LEFT and self.next_direction == RIGHT)
               or (self.direction == RIGHT and self.next_direction == LEFT)):
                self.direction = self.next_direction
            self.next_direction = None

    def move(self):
        """Обновляет позицию змейки."""
        current_head_x, current_head_y = self.get_head_position()
        dx, dy = self.direction

        new_x = (current_head_x + dx * GRID_SIZE) % SCREEN_WIDTH
        new_y = (current_head_y + dy * GRID_SIZE) % SCREEN_HEIGHT

        new_position_head = (new_x, new_y)

        if len(self.positions) >= self.length:
            self.last = self.positions[-1]
        else:
            self.last = None

        self.positions.insert(0, new_position_head)

        if len(self.positions) > self.length:
            self.positions.pop()

    def draw(self):
        """Отрисовывает змейку на экране, затирая след."""
        if self.last is not None:
            last_rect = pg.Rect(self.last, (GRID_SIZE, GRID_SIZE))
            pg.draw.rect(screen, BOARD_BACKGROUND_COLOR, last_rect)

        for position in self.positions:
            rect = pg.Rect(position, (GRID_SIZE, GRID_SIZE))
            pg.draw.rect(screen, self.body_color, rect)
            pg.draw.rect(screen, BORDER_COLOR, rect, 1)

    def get_head_position(self):
        """Возвращает позицию головы змейки."""
        return self.positions[0]

    def decrease_length(self):
        """Уменьшает длину змейки на один сегмент."""
        if len(self.positions) > 1:
            self.last = self.positions.pop()
            self.length -= 1
            return True
        return False

    def reset(self):
        """Сбрасывает змейку в начальное состояние."""
        direction_tuple = (UP, DOWN, LEFT, RIGHT)
        self.length = 1
        del self.positions[1:]
        self.last = None
        self.direction = choice(direction_tuple)
        self.next_direction = None


def handle_keys(game_object):
    """Функция обработки действий пользователя."""
    for event in pg.event.get():
        if event.type == pg.QUIT:
            pg.quit()
            raise SystemExit
        elif event.type == pg.KEYDOWN:
            if event.key == pg.K_UP and game_object.direction != DOWN:
                game_object.next_direction = UP
            elif event.key == pg.K_DOWN and game_object.direction != UP:
                game_object.next_direction = DOWN
            elif event.key == pg.K_LEFT and game_object.direction != RIGHT:
                game_object.next_direction = LEFT
            elif event.key == pg.K_RIGHT and game_object.direction != LEFT:
                game_object.next_direction = RIGHT


def initialize_game_objects():
    """Инициализация всех игровых объектов."""
    snake = Snake()
    snake_positions = set(snake.positions)

    apple = Apple(snake_positions)
    occupied_after_apple = snake_positions | {apple.position}

    stone = Stone(occupied_after_apple)
    occupied_after_stone = occupied_after_apple | {stone.position}

    another_apple = UninedibleApple(occupied_after_stone)

    return snake, apple, stone, another_apple


def draw_initial_screen(snake, apple, another_apple, stone):
    """Отрисовка начального экрана."""
    screen.fill(BOARD_BACKGROUND_COLOR)
    apple.draw()
    another_apple.draw()
    stone.draw()
    snake.draw()
    pg.display.update()


def handle_apple_collision(
    snake,
    apple,
    occupied_positions,
    current_score,
    current_speed
):
    """Обработка столкновения с яблоком."""
    snake.length += 1
    new_score = current_score + 2

    if current_speed <= MAX_SPEED:
        new_speed = current_speed + 2
    else:
        new_speed = current_speed

    apple.randomize_position(occupied_positions)
    return new_score, new_speed


def handle_another_apple_collision(
    snake, another_apple, occupied_positions, old_tail_position
):
    """Обработка столкновения с несъедобным яблоком."""
    # Игра заканчивается.
    if len(snake.positions) == 1:
        return False

    snake.decrease_length()
    # ИГра продолжается.
    if old_tail_position:
        last_rect = pg.Rect(old_tail_position, (GRID_SIZE, GRID_SIZE))
        pg.draw.rect(screen, BOARD_BACKGROUND_COLOR, last_rect)
    another_apple.randomize_position(occupied_positions)
    return True


def check_game_over(snake, stone):
    """Проверка условий завершения игры."""
    head_position = snake.get_head_position()

    # Столкновение с телом змейки или с камнем
    return (head_position in snake.positions[1:]
            or stone.position == head_position)


def reset_game_state(snake, apple, another_apple, stone):
    """Сброс состояния игры."""
    snake.reset()

    snake_positions = set(snake.positions)
    apple.randomize_position(snake_positions)

    occupied_after_apple = snake_positions | {apple.position}
    stone.randomize_position(occupied_after_apple)

    occupied_after_stone = occupied_after_apple | {stone.position}
    another_apple.randomize_position(occupied_after_stone)

    # Перерисовка поля
    screen.fill(BOARD_BACKGROUND_COLOR)
    apple.draw()
    another_apple.draw()
    stone.draw()
    snake.draw()
    pg.display.update()

    # score, speed
    return 0, INIT_SPEED


def main():
    """Основная функция игры."""
    pg.init()

    # Инициализация объектов
    snake, apple, stone, another_apple = initialize_game_objects()
    speed = INIT_SPEED
    score = 0

    def score_statistic():
        """Запись результатов игры в файл."""
        with open('score_stats.txt', 'a', encoding='utf-8') as file:
            file.write(f'Game Over! Ваш счёт за прошлую игру: {score}\n')

    # Начальная отрисовка
    draw_initial_screen(snake, apple, another_apple, stone)

    while True:
        clock.tick(speed)

        # Обработка управления
        handle_keys(snake)
        snake.update_direction()

        # Сохраняем позицию хвоста перед движением
        old_tail_position = snake.positions[-1] if snake.positions else None
        snake.move()

        # Получаем занятые позиции
        occupied_positions = set(snake.positions)
        occupied_positions.add(apple.position)
        occupied_positions.add(another_apple.position)
        occupied_positions.add(stone.position)

        head_position = snake.get_head_position()

        # Обработка столкновений
        if apple.position == head_position:
            score, speed = handle_apple_collision(
                snake, apple, occupied_positions, score, speed
            )

        elif another_apple.position == head_position:
            game_continues = handle_another_apple_collision(
                snake, another_apple, occupied_positions, old_tail_position
            )
            if not game_continues:
                score_statistic()
                score, speed = reset_game_state(
                    snake, apple, another_apple, stone
                )
                continue

        # Проверка условий завершения игры
        if check_game_over(snake, stone):
            score_statistic()
            score, speed = reset_game_state(
                snake, apple, another_apple, stone
            )
            continue

        # Отрисовка кадра
        snake.draw()
        apple.draw()
        another_apple.draw()
        stone.draw()
        pg.display.update()


if __name__ == '__main__':
    main()
