"""pygame 2.1.2 (SDL 2.0.18, Python 3.10.2)"""
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
        matrix = Matrix(screen_resolution)              # initialization Matrix

        while True:                                     # Main cycle of game
            for event in pygame.event.get():
                if event.type == pygame.constants.QUIT:
                    sys.exit()                          # exit

            screen.fill(bg_color)                       # create background
            field.draw_field()                          # draw field

            pygame.display.update()
            clock.tick(FPS)                             # The end of main cycle


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
        print(self.size_x, self.size_y)

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


class Matrix:
    """Class for create matrix"""
    def __init__(self, screen_resolution):
        """
            Create matrix.
        :param screen_resolution: default screen_resolution is 1280 x 800
        """
        self.size_x = int(screen_resolution[0] / 10)
        self.size_y = int(screen_resolution[1] * 0.8 // 10)
        self.data = np.zeros((60, 120), dtype=int)


Window()
