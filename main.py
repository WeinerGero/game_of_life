import pygame
import sys
'''pygame 2.1.2 (SDL 2.0.18, Python 3.10.2)'''


WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (125, 125, 125)


class Window:
    screen_resolution = (1280, 800)
    bg_color = WHITE    # back ground
    FPS = 60

    def __init__(self, screen_resolution=screen_resolution,
                 bg_color=bg_color, FPS=FPS):
        pygame.init()
        screen = pygame.display.set_mode(screen_resolution)
        pygame.display.set_caption('Панда и игра "Жизнь"')
        clock = pygame.time.Clock()

        field = Field(screen, screen_resolution)

        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()
            screen.fill(bg_color)

            field.draw_field()

            pygame.display.update()
            clock.tick(FPS)


class Field:
    scale = 10
    b_color = GRAY    # borders

    def __init__(self, screen, screen_resolution):
        self.screen = screen
        self.size_x = int(screen_resolution[0] / 10)
        self.size_y = int(screen_resolution[1] * 0.8 // 10)
        print(self.size_x, self.size_y)

    def draw_field(self, b_color=b_color, scale=scale):
        for i in range(4, self.size_x-3):       # 121 -> 120 squares
            pygame.draw.line(self.screen, b_color, [i * scale, 40],
                             [i * scale, self.size_y * scale])

        for i in range(4, self.size_y+1):       # 61 -> 60 squares
            pygame.draw.line(self.screen, b_color, [40, i * scale],
                             [self.size_x * scale - 40, i * scale])


Window()
