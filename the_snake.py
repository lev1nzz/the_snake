"""Реализация игры - Змейка, с использованием библиотеки Pygeme"""

from random import choice, randint

import pygame

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
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), 0, 32)

# Заголовок окна игрового поля:
pygame.display.set_caption('Змейка')

# Настройка времени:
clock = pygame.time.Clock()


# Описание классов игры.
class GameObject:
    """
    Базовый класс, который содержит в себе два атрибута и
    один метод, которые будут наследоваться дочерними
    классами

    :param position: Позиция объекта на игровом поле
    :type position: tuple
    :param body_color: Цвет объекта. Будет переопределен объектом класса
    :type body_color: None
    """

    def __init__(self):
        self.position = ((SCREEN_WIDTH // 2), (SCREEN_HEIGHT // 2))
        self.body_color = None

    def draw(self):
        """
        Отрисовка объектов на игровом поле. Будет переопределен -
        объектом класса
        """
        pass


class Apple(GameObject):
    """
    Дочерний класс, унаследован от базового класса GameObjec.
    В классе переопределяются атрибуты и метод для объекта - Яблоко

    :param position: Позиция объекта на игровом поле, определяется случайно
    :type position: tuple
    :param body_color: Цвет объекта - Яблоко
    :type body_color: tuple
    """

    def __init__(self):
        super().__init__()
        self.position = self.randomize_position()
        self.body_color = APPLE_COLOR

    def draw(self):
        """Отрисовка объекта - Яблоко, на игровом поле."""
        rect = pygame.Rect(self.position, (GRID_SIZE, GRID_SIZE))
        pygame.draw.rect(screen, self.body_color, rect)
        pygame.draw.rect(screen, BORDER_COLOR, rect, 1)

    def randomize_position(self) -> tuple:
        """Метод, возвращает кортеж случайных координат, в приделах сетки"""
        value_width = randint(0, GRID_WIDTH - 1) * GRID_SIZE
        value_height = randint(0, GRID_HEIGHT - 1) * GRID_SIZE
        return (value_width, value_height)


class UninedibleApple(Apple):
    """
    Дочерний класс, унаследовн от дочернего класса Apple.
    В классе описывается противоположный по смыслу яблока объект -
    несъедобное яблоко. Атрибуты и методы переопределяются.

    :param position: Позиция объекта на игровом поле, определяется случайно
    :type position: tuple
    :param body_color: Цвет объекта - Несъедобное яблоко
    :type body_color: tuple
    """
    
    def __init__(self):
        super().__init__()
        self.position = self.randomize_position()
        self.body_color = ANOTHER_APPLE_COLOR
    
    def draw(self):
        """Отрисовка объекта - Несъедобное яблоко, на игровом поле."""
        rect = pygame.Rect(self.position, (GRID_SIZE, GRID_SIZE))
        pygame.draw.rect(screen, self.body_color, rect)
        pygame.draw.rect(screen, BORDER_COLOR, rect, 1)


class Stone(Apple):
    """
    Дочерний класс, унаследовн от дочернего класса Apple.
    В классе описывается новый объект на игровом поле.
    Атрибуты и методы переопределяются.
    
    :param position: Позиция объекта на игровом поле, определяется случайно
    :type position: tuple
    :param body_color: Цвет объекта - Камень
    :type body_color: tuple
    """

    def __init__(self):
        super().__init__()
        self.position = self.randomize_position()
        self.body_color = STONE_COLOR
        
    def draw(self):
        """Отрисовка объекта - Камень, на игровом поле."""
        rect = pygame.Rect(self.position, (GRID_SIZE, GRID_SIZE))
        pygame.draw.rect(screen, self.body_color, rect)
        pygame.draw.rect(screen, BORDER_COLOR, rect, 1)
        

class Snake(GameObject):
    """
    Дочерний класс, унаследован от базового класса GameObjec.
    В классе переопределяются атрибуты и метод для объекта - Змейка

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
        super().__init__()
        self.length = 1
        self.positions = [self.position]
        self.body_color = SNAKE_COLOR
        self.direction = RIGHT
        self.next_direction = None
        self.last = None

    def update_direction(self):
        """Обновляет навпрвление движения змейки."""
        if self.next_direction:
            self.direction = self.next_direction
            self.next_direction = None

    def move(self):
        """Обновляет позицию змейки."""
        current_head_position = self.get_head_position()
        if self.direction == RIGHT:
            new_position_head = (
                current_head_position[0] + GRID_SIZE,
                current_head_position[1]
            )
        elif self.direction == LEFT:
            new_position_head = (
                current_head_position[0] - GRID_SIZE,
                current_head_position[1]
            )
        elif self.direction == UP:
            new_position_head = (
                current_head_position[0],
                current_head_position[1] - GRID_SIZE
            )
        elif self.direction == DOWN:
            new_position_head = (
                current_head_position[0],
                current_head_position[1] + GRID_SIZE,
            )
        # Обработка краев экрана.
        new_position_x = new_position_head[0] % SCREEN_WIDTH
        new_position_y = new_position_head[1] % SCREEN_HEIGHT
        new_position_head = (new_position_x, new_position_y)

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
            last_rect = pygame.Rect(self.last, (GRID_SIZE, GRID_SIZE))
            pygame.draw.rect(screen, BOARD_BACKGROUND_COLOR, last_rect)

        for position in self.positions:
            rect = (pygame.Rect(position, (GRID_SIZE, GRID_SIZE)))
            pygame.draw.rect(screen, self.body_color, rect)
            pygame.draw.rect(screen, BORDER_COLOR, rect, 1)

    def get_head_position(self):
        """Возвращает позицию головы змейки."""
        head_position = self.positions[0]
        head_rect = pygame.Rect(head_position, (GRID_SIZE, GRID_SIZE))
        pygame.draw.rect(screen, self.body_color, head_rect)
        pygame.draw.rect(screen, BORDER_COLOR, head_rect, 1)
        return head_position

    def reset(self):
        """Сбрасывает змейку в начальное состояние."""
        direction_list = [
            UP, DOWN, LEFT, RIGHT
        ]

        self.length = 1
        del self.positions[1:]
        self.direction = choice(direction_list)


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


def score_statistic():
    """Функция записывает в файл с ращирением .txt - результаты игры."""
    with open('score_stats.txt', 'a', encoding='utf-8') as f:
        f.write(f'Game Over! Ваш счёт за прошлую игру: {score}\n')
    


def main():
    """Основная функция игры"""
    pygame.init()
    apple = Apple()
    snake = Snake()
    stone = Stone()
    another_apple = UninedibleApple()
    
    speed = INIT_SPEED
    global score
    score = 0
    
    while True:
        clock.tick(speed)
        handle_keys(snake)
        snake.update_direction()
        snake.move()
        
        screen.fill(BOARD_BACKGROUND_COLOR)
        
        apple.draw()
        another_apple.draw()
        stone.draw()
        snake.draw()
        # Проверка на столкновение с яблоком
        if apple.position == snake.positions[0]:
            snake.length += 1
            score += 2
            if speed <= MAX_SPEED: speed += 2
            apple.position = apple.randomize_position()

        # Проверка на столкновение головы с телом змейки
        if snake.get_head_position() in snake.positions[1:]:
            score_statistic()
            snake.reset()
            score = 0
            speed = INIT_SPEED

        # Проверка на столкновение с камнем
        if stone.position == snake.positions[0]:
            score_statistic()
            snake.reset()
            score = 0
            speed = INIT_SPEED
            stone.position = stone.randomize_position()

        # Проверка на валидность тела змейки
        if another_apple.position == snake.positions[0]:
            # Если тело змейки - только голова: Игра Начнется заново
            if len(snake.positions) == 1:
                score_statistic()
                snake.reset()
                score = 0
                speed = INIT_SPEED
            else:
                snake.positions.pop()
                snake.length -= 1
            another_apple.position = another_apple.randomize_position()
            

        pygame.display.update()


if __name__ == '__main__':
    main()
    score_statistic()
