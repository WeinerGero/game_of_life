"""pygame 2.1.2 (SDL 2.0.18, Python 3.10.2), numpy version 1.23.5"""
import sys
import pygame
import numpy as np


# default colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (125, 125, 125)


class Window:
    """Mainly interface of game"""
    screen_resolution = (1280, 800)
    bg_color = WHITE
    FPS = 60

    def __init__(self, screen_resolution=screen_resolution,
                 bg_color=bg_color, FPS=FPS):
        """
            Here a main cycle of game. Create a window and update it.
        :param screen_resolution: default screen_resolution is 1280 x 800
        :param bg_color: default background color is WHITE
        :param FPS: default FPS is 60
        """
        pygame.init()                                   # initialization Pygame
        screen = pygame.display.set_mode(screen_resolution)     # create screen
        pygame.display.set_caption('Панда и игра "Жизнь"')      # window's name
        clock = pygame.time.Clock()

        field = Field(screen, screen_resolution)        # initialization Field
        matrix = ChangeMatrix(screen_resolution)        # initialization Matrix
        draw_matrix = DrawMatrix(field.scale, screen, screen_resolution)
        button = Button(screen)
        algorithm = Algorithm(screen_resolution, matrix.data)
        flag = True

        while True:                                     # Main cycle of game
            # Events
            for event in pygame.event.get():
                # Mouse motion
                if event.type == pygame.MOUSEMOTION:
                    control_game = ControlGame(event.pos, event.buttons,
                                               field.scale, matrix.data)
                    control_game.choose_button()

                # Click mouse
                if event.type == pygame.MOUSEBUTTONDOWN:
                    control_game = ControlGame(event.pos, event.button,
                                               field.scale, matrix.data)
                    if control_game.choose_button() is None:
                        pass
                    else:
                        matrix.data = control_game.choose_button()

                # Exit
                if event.type == pygame.constants.QUIT:
                    sys.exit()

            algorithm.default_algorithm()

            # draw interface
            screen.fill(bg_color)
            draw_matrix.draw_matrix(matrix.comparison_data())
            field.draw_field()
            button.draw_button(40, 670, 'Старт', 80, 676)
            button.draw_button(210, 670, 'Стоп', 256, 676)
            button.draw_button(380, 670, 'Очистить', 404, 676)

            # The end of main cycle
            pygame.display.update()
            clock.tick(FPS)


class Field:
    """Class for drawing field"""
    scale = 10                                          # scale of cell in px
    b_color = GRAY                                      # color of borders

    def __init__(self, screen, screen_resolution):
        """
            Count cells and draw field.
        :param screen: control pygame display
        :param screen_resolution: default screen_resolution is 1280 x 800
        """
        self.screen = screen                            # Get screen control
        self.size_x = int(screen_resolution[0] / 10)    # Count cells on x
        self.size_y = int(screen_resolution[1] * 0.8 // 10)  # Count cells on y
        # print(self.size_x, self.size_y)

    def draw_field(self, b_color=b_color, scale=scale):
        """
            Draw field.
        :param b_color: default borders color is GREY
        :param scale: default scale of cell is 10 px
        :return: None
        """
        for i in range(4, self.size_x-3):               # 121 borders -> 120 cells
            pygame.draw.line(self.screen, b_color, [i * scale, 40],
                             [i * scale, self.size_y * scale])  # space of 40 px on the left and right

        for i in range(4, self.size_y+1):               # 61 borders -> 60 cells
            pygame.draw.line(self.screen, b_color, [40, i * scale],
                             [self.size_x * scale - 40, i * scale])  # space of 40 px on the top and 20% screen on the down


class Button:
    def __init__(self, screen, width=150, height=50, inactive_color=GRAY,
                 active_color=BLACK):
        self.screen = screen
        self.width = width
        self.height = height
        self.inactive_color = inactive_color
        self.active_color = active_color

    def draw_button(self, x, y, message, message_x, message_y):
        pygame.draw.rect(self.screen, self.active_color, (x, y, self.width, self.height),1)
        font = pygame.font.SysFont('Century Gothic', 24)
        text = font.render(message, False, self.active_color)
        self.screen.blit(text, (message_x, message_y))


class Algorithm:
    def __init__(self, screen_resolution, matrix, speed=1, flag=True):
        self.screen_resolution = screen_resolution
        self.matrix = matrix
        self.speed = speed
        self.flag = flag

    def default_algorithm(self):
        pass


class ControlGame:
    """
        Class for control game
    """
    def __init__(self, pos_mouse, num_button, scale, data):
        self.pos_mouse = pos_mouse
        self.num_button = num_button
        self.scale = scale
        self.data = data
        # print(pos_mouse, num_button)

    def choose_button(self):
        """
            Method for looking buttons
        :return: None or self.data
        """
        if 40 <= self.pos_mouse[0] <= 1240 \
                and 40 <= self.pos_mouse[1] <= 640:     # (40,40), (1240, 640)
            InputOnField(self.pos_mouse, self.num_button, self.scale, self.data)
        elif self.num_button == 1 and 40 <= self.pos_mouse[0] <= 190 \
                and 670 <= self.pos_mouse[1] <= 720:
            print('Start')
        elif self.num_button == 1 and 210 <= self.pos_mouse[0] <= 360 \
                and 670 <= self.pos_mouse[1] <= 720:
            print('Stop')
        elif self.num_button == 1 and 380 <= self.pos_mouse[0] <= 530 \
                and 670 <= self.pos_mouse[1] <= 720:
            self.data = np.zeros((60, 120), dtype=int)
            return self.data


class InputOnField:
    """
        Class for interaction with field
    """
    def __init__(self, pos_mouse, num_button, scale, data):
        """
            Class for interaction with field
        :param pos_mouse: position mouse at click
        :param num_button: number of button mouse
        :param scale: default is 10
        :param data: matrix
        """
        self.num_button = num_button
        self.x_field = (pos_mouse[0] - 40) // scale     # 0-119
        self.y_field = (pos_mouse[1] - 40) // scale     # 0-59
        self.data = data
        self.tools()

    def tools(self):
        """
            Choose tool by button of mouse
        :return: None
        """
        if self.num_button == 1 or self.num_button == (1, 0, 0):
            self.draw()
        elif self.num_button == 3 or self.num_button == (0, 0, 1):
            self.remove()

    def draw(self):
        """
            Draw on field
        :return: None
        """
        self.data[self.y_field, self.x_field] = 1

    def remove(self):
        """
            Clean drawn cells.
        :return: None
        """
        self.data[self.y_field, self.x_field] = 0


class Matrix:
    """Class for create matrix"""
    def __init__(self, screen_resolution):
        """
            Create matrix.
        :param screen_resolution: default screen_resolution is 1280 x 800
        """
        self.size_x = int(screen_resolution[0] / 10) - 8
        self.size_y = int(screen_resolution[1] * 0.8 // 10) - 4
        self.data = np.zeros((self.size_y, self.size_x), dtype=int)


class ChangeMatrix:
    """
        class for change matrix
    """
    def __init__(self, screen_resolution):
        """
            class for change matrix
        :param screen_resolution: default is 1280x800
        """
        self.old_data = Matrix(screen_resolution).data
        self.data = Matrix(screen_resolution).data

    def comparison_data(self):
        """
            Looking for changes
        :return: compare_set - tuple of 2 1d_arrays
        """
        compare_data = self.old_data == self.data
        compare_set = np.where(compare_data == False)
        if compare_set:
            return compare_set


class DrawMatrix:
    """
        class for drawing matrix
    """
    def __init__(self, scale, screen, screen_resolution):
        """
            class for drawing matrix
        :param scale: default is 10
        :param screen: control pygame display
        :param screen_resolution: default is 1280x800
        """
        self.scale = scale
        self.screen = screen
        self.size_x = int(screen_resolution[0] / 10) - 8
        self.size_y = int(screen_resolution[1] * 0.8 // 10) - 4

    def convert(self, compare_data):
        """
        (array([1, 2, 3, 4], dtype=int64), array([5, 6, 7, 8], dtype=int64))
        -> [(5, 1), (6, 2), (7, 3), (8, 4)]
        """
        coordinates = [coordinate for coordinate in zip(compare_data[1],
                                                        compare_data[0])]
        return coordinates

    def draw_matrix(self, compare_data):
        """
            Draw matrix.
        :param compare_data:
        :return: None
        """
        if not compare_data:
            return
        coordinates = self.convert(compare_data)

        for coordinate in coordinates:
            pygame.draw.rect(self.screen, BLACK, (
                40 + self.scale * coordinate[0],
                40 + self.scale * coordinate[1],
                self.scale, self.scale
            ))


Window()
