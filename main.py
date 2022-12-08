"""pygame 2.1.2 (SDL 2.0.18, Python 3.10.2), numpy version 1.23.5"""
import sys
import pygame
import numpy as np

# default settings
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (125, 125, 125)
LIGHT_GRAY = (215, 215, 215)
LL_GRAY = (235, 235, 235)

screen_resolution = (1280, 800)
bg_color = WHITE


class Field:
    """Class for drawing field"""
    scale = 10                                          # scale of cell in px
    b_color = GRAY                                      # color of borders

    def __init__(self):
        """
            Count cells and draw field.
        """
        self.screen = screen                            # Get screen control
        self.size_x = int(screen_resolution[0] / 10)    # Count cells on x
        self.size_y = int(screen_resolution[1] * 0.8 // 10)  # Count cells on y

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
    def __init__(self, width=150, height=50, inactive_color=GRAY,
                 active_color=LIGHT_GRAY, target_color=LL_GRAY,
                 text_inactive_color=WHITE, text_active_color=BLACK):
        """
            Class for drawing buttons.
        :param width: default is 150
        :param height: default is 50
        :param inactive_color:  default is GRAY
        :param active_color: default is LIGHT_GRAY
        :param target_color: default is LL_GRAY
        :param text_inactive_color: default is WHITE
        :param text_active_color: default is BLACK
        """
        self.screen = screen
        self.width = width
        self.height = height
        self.inactive_color = inactive_color
        self.active_color = active_color
        self.target_color = target_color
        self.text_inactive_color = text_inactive_color
        self.text_active_color = text_active_color
        self.font = pygame.font.SysFont('Century Gothic', 24)

    def _draw_default_button(self, x, y, message, message_x, message_y):
        """
            draw default buttons without change color
        :param x: x axis of button
        :param y: y axis of button
        :param message: message into
        :param message_x: x axis of massage
        :param message_y: y axis of massage
        :return: None
        """
        pygame.draw.rect(self.screen, self.active_color,
                         (x, y, self.width, self.height), 1)
        text = self.font.render(message, False, self.text_active_color)
        self.screen.blit(text, (message_x, message_y))

    def _draw_action_button(self, x, y, message, message_x, message_y):
        """
            draw action buttons with change color
        :param x: x axis of button
        :param y: y axis of button
        :param message: message into
        :param message_x: x axis of massage
        :param message_y: y axis of massage
        :return: None
        """
        pygame.draw.rect(self.screen, self.inactive_color,
                         (x, y, self.width, self.height))
        text = self.font.render(message, False, self.text_inactive_color)
        self.screen.blit(text, (message_x, message_y))

    def _draw_targeted_button(self, x, y, message, message_x, message_y):
        """
            draw targeted button with change color
        :param x: x axis of button
        :param y: y axis of button
        :param message: message into
        :param message_x: x axis of massage
        :param message_y: y axis of massage
        :return: None
        """
        pygame.draw.rect(self.screen, self.target_color,
                         (x, y, self.width, self.height))
        pygame.draw.rect(self.screen, self.active_color,
                         (x, y, self.width, self.height), 1)
        text = self.font.render(message, False, self.text_active_color)
        self.screen.blit(text, (message_x, message_y))

    def _choose_draw_button(self, x, y, message, message_x, message_y):
        """
            function for choosing what status of button now and what
            function need to use for drawing
        :param x: x axis of button
        :param y: y axis of button
        :param message: message into
        :param message_x: x axis of massage
        :param message_y: y axis of massage
        :return: None
        """
        if action_button == message:
            self._draw_action_button(x, y, message, message_x, message_y)
        else:
            if target_button == message:
                self._draw_targeted_button(x, y, message, message_x, message_y)
            else:
                self._draw_default_button(x, y, message, message_x, message_y)

    def draw_button_start(self):
        """
            function for drawing start button
        :return: None
        """
        x = 40
        y = 670
        message = 'Старт'
        message_x = 80
        message_y = 676
        self._choose_draw_button(x, y, message, message_x, message_y)

    def draw_button_stop(self):
        """
            function for drawing stop button
        :return: None
        """
        x = 210
        y = 670
        message = 'Стоп'
        message_x = 256
        message_y = 676
        self._choose_draw_button(x, y, message, message_x, message_y)

    def draw_button_clear(self):
        """
            function for drawing clear button
        :return: None
        """
        x = 380
        y = 670
        message = 'Очистить'
        message_x = 404
        message_y = 676
        self._choose_draw_button(x, y, message, message_x, message_y)


class Algorithm:
    def __init__(self):
        """
         Class include algorithm of game
        """
        self.screen_resolution = screen_resolution
        self.arr31 = np.zeros((3, 1), dtype=int)
        self.arr13 = np.zeros((1, 3), dtype=int)
        self.arr21 = np.zeros((2, 1), dtype=int)

    def detect_border_cell(self, coordinate):
        """

            :param coordinate: coordinate of dot (x, y)
            left top
                        self.matrix_neighbors(coordinate, start_x=0, start_y=0)

            top
                        self.matrix_neighbors(coordinate, start_y=0)

            right top
                        self.matrix_neighbors(coordinate, start_y=0)

            right
                        self.matrix_neighbors(coordinate, end_x=1)

            right down
                        self.matrix_neighbors(coordinate, end_x=1, end_y=1)

            down
                        self.matrix_neighbors(coordinate, end_y=1)

            left down
                        self.matrix_neighbors(coordinate, start_x=0, end_y=1)

            left
                        self.matrix_neighbors(coordinate, start_x=0)
            """
        start_y = -1; end_y = 2; start_x = -1; end_x = 2
        if coordinate[0] == 0 and coordinate[1] == 0:  # left top
            start_x, start_y = 0, 0
            return start_y, end_y, start_x, end_x

        elif coordinate[1] == 0 and coordinate[0] != 0 \
                and coordinate[0] != 119:  # top
            start_y = 0
            return start_y, end_y, start_x, end_x

        elif coordinate[0] == 119 and coordinate[1] == 0:  # right top
            start_y = 0
            return start_y, end_y, start_x, end_x

        elif coordinate[0] == 119 and coordinate[1] != 0 \
                and coordinate[1] != 59:  # right
            end_x = 1
            return start_y, end_y, start_x, end_x

        elif coordinate[0] == 119 and coordinate[1] == 59:  # right down
            end_x, end_y = 1, 1
            return start_y, end_y, start_x, end_x

        elif coordinate[0] != 119 and coordinate[1] == 59 \
                and coordinate[0] != 0:  # down
            return start_y, end_y, start_x, end_x

        elif coordinate[0] == 0 and coordinate[1] == 59:  # left down
            start_x, end_y = 0, 1
            return start_y, end_y, start_x, end_x

        elif coordinate[0] == 0 and coordinate[1] != 59 \
                and coordinate[1] != 0:  # left
            start_x = 0
            return start_y, end_y, start_x, end_x
        else:       # not is border cell
            return start_y, end_y, start_x, end_x

    def default_algorithm(self):
        """
            main cycle of default algorithm of game
        :return:  None
        """
        self.data = np.copy(matrix.data)
        for coordinate in coordinates:
            self.change_zero_cell(coordinate)
            self.change_one_cell(coordinate)

    def matrix_neighbors_zero(self, coordinate, value=0):
        """
            count neighbors with value zero and get their indexes
        :param coordinate: coordinate of dot (x, y)
        :param value: default is 0
        :return: index_list_zero or None if value is 1
        """
        start_y, end_y, start_x, end_x = self.detect_border_cell(coordinate)
        neighbors = self.data[coordinate[1] + start_y:coordinate[1] + end_y,
                              coordinate[0] + start_x:coordinate[0] + end_x]
        # -> (array(), array())
        count_neighbors = np.where(neighbors == value)
        # (array(), array()) -> [(x1,y1), (x2,y2)]
        count_neighbors = draw_matrix.convert(count_neighbors)

        if value:
            return None

        shape_array = np.shape(neighbors)
        index_list_zero = []
        if shape_array == (3, 3):  # 4, 5, y , x
            for coord in count_neighbors:
                if coord == (0, 0):     # 3, 4
                    index_list_zero.append((coordinate[0]-1,
                                           coordinate[1]-1))
                elif coord == (1, 0):     # 3, 5
                    index_list_zero.append((coordinate[0],
                                           coordinate[1]-1))
                elif coord == (2, 0):     # 3, 6
                    index_list_zero.append((coordinate[0]+1,
                                           coordinate[1]-1))
                elif coord == (0, 1):     # 4, 4
                    index_list_zero.append((coordinate[0]-1,
                                           coordinate[1]))
                # elif coord == (1, 1):     # 4, 5
                #    index_list_zero.append((coordinate[0],
                #                           coordinate[1]))
                elif coord == (2, 1):     # 4, 6
                    index_list_zero.append((coordinate[0]+1,
                                           coordinate[1]))
                elif coord == (0, 2):     # 5, 4
                    index_list_zero.append((coordinate[0]-1,
                                           coordinate[1]+1))
                elif coord == (1, 2):     # 5, 5
                    index_list_zero.append((coordinate[0],
                                           coordinate[1]+1))
                elif coord == (2, 2):     # 5, 6
                    index_list_zero.append((coordinate[0]+1,
                                           coordinate[1]+1))
        elif shape_array == (2, 2):
            for coord in count_neighbors:
                one_position = np.where(neighbors == 1)
                if one_position[0][0] == 0:
                    if one_position[1][0] == 0:
                        # 1 algorithm, the first cell
                        if coord == (0, 0):
                            index_list_zero.append((coordinate[0],
                                                    coordinate[1]))
                        elif coord == (1, 0):
                            index_list_zero.append((coordinate[0]+1,
                                                    coordinate[1]))
                        elif coord == (0, 1):
                            index_list_zero.append((coordinate[0],
                                                    coordinate[1]+1))
                        elif coord == (1, 1):
                            index_list_zero.append((coordinate[0]+1,
                                                    coordinate[1]+1))
                    else:
                        # 2 algorithm, the second cell
                        if coord == (0, 0):
                            index_list_zero.append((coordinate[0]-1,
                                                    coordinate[1]))
                        # elif coord == (1, 0):
                        #    index_list_zero.append((coordinate[0],
                        #                            coordinate[1]))
                        elif coord == (0, 1):
                            index_list_zero.append((coordinate[0]-1,
                                                    coordinate[1]+1))
                        elif coord == (1, 1):
                            index_list_zero.append((coordinate[0],
                                                    coordinate[1]+1))
                else:
                    if one_position[1][0] == 0:
                        # 3 algorithm, the third cell
                        if coord == (0, 0):
                            index_list_zero.append((coordinate[0],
                                                    coordinate[1]-1))
                        elif coord == (1, 0):
                            index_list_zero.append((coordinate[0]+1,
                                                    coordinate[1]-1))
                        # elif coord == (0, 1):
                        #    index_list_zero.append((coordinate[0],
                        #                            coordinate[1]))
                        elif coord == (1, 1):
                            index_list_zero.append((coordinate[0]+1,
                                                    coordinate[1]))
                    else:
                        # 4 algorithm, the 4th cell
                        if coord == (0, 0):
                            index_list_zero.append((coordinate[0]-1,
                                                    coordinate[1]-1))
                        elif coord == (1, 0):
                            index_list_zero.append((coordinate[0],
                                                    coordinate[1]-1))
                        elif coord == (0, 1):
                            index_list_zero.append((coordinate[0]-1,
                                                    coordinate[1]))
                        # elif coord == (1, 1):
                        #    index_list_zero.append((coordinate[0],
                        #                            coordinate[1]))

        elif shape_array == (2, 3):
            for coord in count_neighbors:
                one_position = np.where(neighbors == 1)
                if one_position[0][0] == 0:
                    if coord == (0, 0):
                        index_list_zero.append((coordinate[0]-1,
                                                coordinate[1]))
                    # elif coord == (1, 0):
                    #    index_list_zero.append((coordinate[0],
                    #                            coordinate[1]))
                    elif coord == (2, 0):
                        index_list_zero.append((coordinate[0]+1,
                                                coordinate[1]))
                    elif coord == (0, 1):
                        index_list_zero.append((coordinate[0]-1,
                                                coordinate[1]+1))
                    elif coord == (1, 1):
                        index_list_zero.append((coordinate[0],
                                                coordinate[1]+1))
                    elif coord == (2, 1):
                        index_list_zero.append((coordinate[0]+1,
                                                coordinate[1]+1))
                else:
                    if coord == (0, 0):
                        index_list_zero.append((coordinate[0]-1,
                                                coordinate[1]-1))
                    elif coord == (1, 0):
                        index_list_zero.append((coordinate[0],
                                                coordinate[1]-1))
                    elif coord == (2, 0):
                        index_list_zero.append((coordinate[0]+1,
                                                coordinate[1]-1))
                    elif coord == (0, 1):
                        index_list_zero.append((coordinate[0]-1,
                                                coordinate[1]))
                    # elif coord == (1, 1):
                    #    index_list_zero.append((coordinate[0],
                    #                            coordinate[1]))
                    elif coord == (2, 1):
                        index_list_zero.append((coordinate[0]+1,
                                                coordinate[1]))

        elif shape_array == (3, 2):
            for coord in count_neighbors:
                one_position = np.where(neighbors == 1)
                if one_position[1][0] == 0:
                    if coord == (0, 0):
                        index_list_zero.append((coordinate[0],
                                                coordinate[1]-1))
                    elif coord == (1, 0):
                        index_list_zero.append((coordinate[0]+1,
                                                coordinate[1]-1))
                    # elif coord == (0, 1):
                    #    index_list_zero.append((coordinate[0],
                    #                            coordinate[1]))
                    elif coord == (1, 1):
                        index_list_zero.append((coordinate[0]+1,
                                                coordinate[1]))
                    elif coord == (0, 2):
                        index_list_zero.append((coordinate[0],
                                                coordinate[1]+1))
                    elif coord == (1, 2):
                        index_list_zero.append((coordinate[0]+1,
                                                coordinate[1]+1))
                else:
                    if coord == (0, 0):
                        index_list_zero.append((coordinate[0]-1,
                                                coordinate[1]-1))
                    elif coord == (1, 0):
                        index_list_zero.append((coordinate[0],
                                                coordinate[1]-1))
                    elif coord == (0, 1):
                        index_list_zero.append((coordinate[0]-1,
                                                coordinate[1]))
                    # elif coord == (1, 1):
                    #     index_list_zero.append((coordinate[0],
                    #                            coordinate[1]))
                    elif coord == (0, 2):
                        index_list_zero.append((coordinate[0]+1,
                                                coordinate[1]+1))
                    elif coord == (1, 2):
                        index_list_zero.append((coordinate[0],
                                                coordinate[1]+1))
        return index_list_zero

    def matrix_neighbors_one(self, coordinate, value=1):
        """
            count neighbors with value one
        :param coordinate: coordinate of dot (x, y)
        :param value: default value is one
        :return: count_neighbors
        """
        start_y, end_y, start_x, end_x = self.detect_border_cell(coordinate)
        neighbors = self.data[coordinate[1]+start_y:coordinate[1]+end_y,
                              coordinate[0]+start_x:coordinate[0]+end_x]
        # -> (array(), array())
        count_neighbors = np.where(neighbors == value)
        # (array(), array()) -> [(x1,y1), (x2,y2)]
        count_neighbors = draw_matrix.convert(count_neighbors)
        return count_neighbors      # [(x1,y1), (x2,y2), ... , (xn, yn)]

    def _shape_array21_expansion(self, neighbors):
        """
            Didn't use in algorithm. Transform array (2, 1)
            to (3, 3) with 1 in centre
        :param neighbors: array (2, 1)
        :return: neighbors_expansion
        """
        one_position = np.where(neighbors == 1)
        if one_position[1][0] == 0:
            neighbors_expansion = np.append(self.arr31, neighbors, axis=1)
        else:
            neighbors_expansion = np.append(neighbors, self.arr31, axis=1)
        return neighbors_expansion

    def _shape_array12_expansion(self, neighbors):
        """
            Didn't use in algorithm. Transform array (1, 2)
            to (3, 3) with 1 in centre
        :param neighbors: array (1, 2)
        :return: neighbors_expansion
        """
        one_position = np.where(neighbors == 1)
        if one_position[0][0] == 0:
            neighbors_expansion = np.append(self.arr13, neighbors, axis=0)
        else:
            neighbors_expansion = np.append(neighbors, self.arr13, axis=0)
        return neighbors_expansion

    def _shape_array11_expansion(self, neighbors):
        """
            Didn't use in algorithm. Transform array (1, 1)
            to (3, 3) with 1 in centre
        :param neighbors: array (1, 1)
        :return: neighbors_expansion
        """
        one_position = np.where(neighbors == 1)
        if one_position[1][0] == 0:
            neighbors_expansion = np.append(self.arr21, neighbors, axis=1)
        else:
            neighbors_expansion = np.append(neighbors, self.arr21, axis=1)
        neighbors_expansion = self._shape_array12_expansion(neighbors_expansion)
        return neighbors_expansion

    def change_zero_cell(self, coordinate):
        """
            function for changing cell with value 0 to cell with value 1 if
            cell satisfies the conditions
        :param coordinate:  coordinate of dot (x, y)
        :return: None
        """
        index_list_zero = self.matrix_neighbors_zero(coordinate)
        for index in index_list_zero:
            neighbor_of_one_zero = self.matrix_neighbors_one(index)
            if len(neighbor_of_one_zero) == 3:
                if index[1] == 60:
                    index = (index[0], 59)
                if index[0] == 120:
                    index = (119, index[1])
                matrix.data[index[1], index[0]] = 1

    def change_one_cell(self, coordinate):
        """
            function for changing cell with value 1 to cell with value 0 if
            cell satisfies the conditions
        :param coordinate:  coordinate of dot (x, y)
        :return:
        """
        neighbors_one_one = self.matrix_neighbors_one(coordinate)
        if len(neighbors_one_one) < 3 or len(neighbors_one_one) > 4:
            matrix.data[coordinate[1], coordinate[0]] = 0


class ControlGame:
    """
        Class for control game
    """
    def choose_field(self, pos_mouse, num_button):
        """
            Method for looking field
        :param pos_mouse: position of mouse in moment at click
        :param num_button: a number button that is clicked on
        :return: None
        """
        # field
        if action_button == 'Стоп' or action_button is None:
            if 40 <= pos_mouse[0] <= 1240 \
                    and 40 <= pos_mouse[1] <= 640:     # (40,40), (1240, 640)
                InputOnField(pos_mouse, num_button, field.scale, matrix.data)

    def target_buttons(self, event_pose):
        """
            function for detecting targeted button
        :param event_pose: position of mouse in moment at movement
        :return: 'Старт' / 'Стоп' / 'Очистить'
        """
        # start button
        if 40 <= event_pose[0] <= 190 \
                and 670 <= event_pose[1] <= 720:
            return 'Старт'

        # stop button
        elif 210 <= event_pose[0] <= 360 \
                and 670 <= event_pose[1] <= 720:
            return 'Стоп'

        # clear button
        elif 380 <= event_pose[0] <= 530 \
                and 670 <= event_pose[1] <= 720:
            return 'Очистить'

    def choose_button(self, pos_mouse, num_button):
        """
            function for detecting button clicks
        :param pos_mouse: position of mouse in moment at click
        :param num_button: a number button that is clicked on
        :return: 'Старт' / 'Стоп' / 'Очистить' / None
        """
        # start
        if num_button == 1 and 40 <= pos_mouse[0] <= 190 \
                and 670 <= pos_mouse[1] <= 720:
            return 'Старт'

        # stop
        elif num_button == 1 and 210 <= pos_mouse[0] <= 360 \
                and 670 <= pos_mouse[1] <= 720:
            return 'Стоп'

        # clear
        elif num_button == 1 and 380 <= pos_mouse[0] <= 530 \
                and 670 <= pos_mouse[1] <= 720:
            matrix.data = np.zeros((60, 120), dtype=int)
            return 'Стоп'
        else:
            return action_button


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
        if self.y_field == 60:
            self.y_field = 59
        if self.x_field == 120:
            self.x_field = 119
        self.data[self.y_field, self.x_field] = 1

    def remove(self):
        """
            Clean drawn cells.
        :return: None
        """
        self.data[self.y_field, self.x_field] = 0


class Matrix:
    """Class for create matrix"""
    def __init__(self):
        """
            Create matrix. Count size_x and size_y of field for matrix
        """
        self.size_x = int(screen_resolution[0] / 10) - 8
        self.size_y = int(screen_resolution[1] * 0.8 // 10) - 4
        self.data = np.zeros((self.size_y, self.size_x), dtype=int)


class ChangeMatrix:
    """
        class for change matrix
    """
    def __init__(self):
        """
            class for change matrix
        """
        self.old_data = Matrix().data
        self.data = Matrix().data
        # self.compare_set = self.comparison_data()

    def comparison_data(self):
        """
            Looking for changes
        :return: compare_set - tuple of 2 1d_arrays
        """
        compare_data = self.old_data == self.data
        compare_set = np.where(compare_data == False)
        return compare_set


class DrawMatrix:
    """
        class for drawing matrix
    """
    def __init__(self):
        """
            class for drawing matrix
        :param scale: default is 10
        :param screen: control pygame display
        :param screen_resolution: default is 1280x800
        """
        self.scale = field.scale
        self.screen = screen
        self.size_x = int(screen_resolution[0] / 10) - 8
        self.size_y = int(screen_resolution[1] * 0.8 // 10) - 4
        # self.coordinates = self.convert(compare_data)

    def convert(self, compare_data):
        """
            function for convert compare_data (set of 2 1d arrays) to list
            of tuples
        :param compare_data: set of 2 1d arrays with indexes of dotes
        :return: coordinates
        """
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
        :return: coordinates
        """
        coordinates = self.convert(compare_data)

        for coordinate in coordinates:
            pygame.draw.rect(self.screen, BLACK, (
                40 + self.scale * coordinate[0],
                40 + self.scale * coordinate[1],
                self.scale, self.scale
            ))
        return coordinates


###############################################################################
pygame.init()                                   # initialization Pygame
screen = pygame.display.set_mode(screen_resolution)     # create screen
pygame.display.set_caption('Панда и игра "Жизнь"')      # window's name
clock = pygame.time.Clock()

field = Field()        # initialization Field
matrix = ChangeMatrix()        # initialization Matrix
draw_matrix = DrawMatrix()
button = Button()
algorithm = Algorithm()
flag = True
action_button = None
target_button = None
control_game = ControlGame()
speed = 120

while True:                                     # Main cycle of game
    # Events
    for event in pygame.event.get():
        # Mouse motion
        if event.type == pygame.MOUSEMOTION:
            # control_game.choose_button(event.pos, event.buttons)
            target_button = control_game.target_buttons(event.pos)
            if action_button != 'Старт':
                control_game.choose_field(event.pos, event.buttons)

        # Click mouse
        if event.type == pygame.MOUSEBUTTONDOWN:
            action_button = control_game.choose_button(event.pos, event.button)
            if action_button != 'Старт':
                control_game.choose_field(event.pos, event.button)

        # Exit
        if event.type == pygame.constants.QUIT:
            sys.exit()

    # draw interface
    screen.fill(bg_color)
    coordinates = draw_matrix.draw_matrix(matrix.comparison_data())
    field.draw_field()

    # algorithm
    while action_button == 'Старт':
        # Events
        for event in pygame.event.get():
            # Mouse motion
            if event.type == pygame.MOUSEMOTION:
                # control_game.choose_button(event.pos, event.buttons)
                target_button = control_game.target_buttons(event.pos)
                if action_button != 'Старт':
                    control_game.choose_field(event.pos, event.buttons)

            # Click mouse
            if event.type == pygame.MOUSEBUTTONDOWN:
                action_button = control_game.choose_button(event.pos,
                                                           event.button)
                if action_button != 'Старт':
                    control_game.choose_field(event.pos, event.button)

            # Exit
            if event.type == pygame.constants.QUIT:
                sys.exit()

        # draw interface
        screen.fill(bg_color)
        coordinates = draw_matrix.draw_matrix(matrix.comparison_data())
        field.draw_field()

        algorithm.default_algorithm()

        # draw buttons
        button.draw_button_start()
        button.draw_button_stop()
        button.draw_button_clear()

        # The end of main cycle
        pygame.display.update()

        clock.tick(speed)

    # draw buttons
    button.draw_button_start()
    button.draw_button_stop()
    button.draw_button_clear()

    # The end of main cycle
    pygame.display.update()
    clock.tick(1000)
