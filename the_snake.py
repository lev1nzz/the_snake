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

# Цвет змейки
SNAKE_COLOR = (0, 255, 0)

# Скорость движения змейки:
SPEED = 20

# Настройка игрового окна:
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), 0, 32)

# Заголовок окна игрового поля:
pygame.display.set_caption('Змейка')

# Настройка времени:
clock = pygame.time.Clock()


# Описание классов игры.
class GameObject:
    '''
    Базовый класс, который содержит в себе два атрибута и
    один метод, которые будут наследоваться дочерними 
    классами
    
    :param position: Позиция объекта на игровом поле
    :type position: tuple
    :param body_color: Цвет объекта. Будет переопределен объектом класса
    :type body_color: None
    '''
    
    def __init__(self):
        self.position = ((SCREEN_WIDTH // 2), (SCREEN_HEIGHT // 2))
        self.body_color = None
        
    def draw(self):
        '''
        Отрисовка объектов на игровом поле. Будет переопределен - 
        объектом класса
        '''
        pass
    

class Apple(GameObject):
    '''
    Дочерний класс, унаследован от базового класса GameObjec.
    В классе переопределяются атрибуты и метод для объекта - Яблоко
    
    :param position: Позиция объекта на игровом поле, определяется случайно
    :type position: tuple
    :param body_color: Цвет объекта - Яблоко
    :type body_color: tuple
    '''
    
    def __init__(self):
        super().__init__()
        self.position = self.randomize_position()
        self.body_color = APPLE_COLOR

    def draw(self):
        '''Отрисовка объекта - Яблоко, на игровом поле.'''
        rect = pygame.Rect(self.position, (GRID_SIZE, GRID_SIZE))
        pygame.draw.rect(screen, self.body_color, rect)
        pygame.draw.rect(screen, BORDER_COLOR, rect, 1)
        
    
    def randomize_position(self) -> tuple:
        '''
        Метод, возвращает кортеж случайных координат, в приделах сетки
        '''
        value_width = randint(0, GRID_WIDTH - 1) * GRID_SIZE
        value_height = randint(0, GRID_HEIGHT - 1) * GRID_SIZE
        return (value_width, value_height)

class Snake(GameObject):
    '''
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
    '''
    def __init__(self):
        super().__init__()
        self.length = 1
        self.positions = [self.position]
        self.body_color = SNAKE_COLOR
        self.direction = RIGHT
        self.next_direction = None

    
    def update_direction(self):
        '''Обновляет навпрвление движения змейки.'''
        if self.next_direction:
            self.direction = self.next_direction
            self.next_direction = None
            
    def move(self):
        '''Обновляет позицию змейки.'''
        pass

    def draw(self):
        '''Отрисовывает змейку на экране, затирая след.'''
        for position in self.positions[:-1]:
            rect = (pygame.Rect(position, (GRID_SIZE, GRID_SIZE)))
            pygame.draw.rect(screen, self.body_color, rect)
            pygame.draw.rect(screen, BORDER_COLOR, rect, 1)

    def get_head_position(self):
        '''Возвращает позицию головы змейки.'''
        head_rect = pygame.Rect(self.positions[0], (GRID_SIZE, GRID_SIZE))
        pygame.draw.rect(screen, self.body_color, head_rect)
        pygame.draw.rect(screen, BORDER_COLOR, head_rect, 1)
        
    def reset(self):
        '''Сбрасывает змейку в начальное состояние.'''
        pass

def handle_keys(game_object):
    '''Функция обработки действий пользователя'''
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


def main():
    # Инициализация PyGame:
    pygame.init()
    # Тут нужно создать экземпляры классов.
    apple = Apple()
    snake = Snake()
    
    while True:
        clock.tick(SPEED)
        handle_keys(snake)
        apple.draw()
        snake.draw()
        pygame.display.update()
        # Тут опишите основную логику игры.
        # ...


if __name__ == '__main__':
    main()



#     # Затирание последнего сегмента
#     if self.last:
#         last_rect = pygame.Rect(self.last, (GRID_SIZE, GRID_SIZE))
#         pygame.draw.rect(screen, BOARD_BACKGROUND_COLOR, last_rect)



