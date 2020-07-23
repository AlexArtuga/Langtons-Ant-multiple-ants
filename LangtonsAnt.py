from graphics import *
import time
import random

win = GraphWin("Langton's Ant", 1000, 1000)
game_board = []
WIDTH = 100
HEIGHT = 100
# Controls what percent of squares start white/black.
PER_WHITE_INIT = 100


class Ant:

    def __init__(self, start_x, start_y):
        self.x = start_x
        self.y = start_y
        self.orientation = 1

    # 0 is left, 1 is up, 2 is right, 3 is down
    def clock_wise_rotation(self):
        self.orientation = (self.orientation + 1) % 4

    def counter_clock_wise_rotation(self):
        self.orientation = (self.orientation - 1) % 4

    def ant_move(self):
        if self.orientation == 0:
            self.x -= 1
        elif self.orientation == 1:
            self.y -= 1
        elif self.orientation == 2:
            self.x += 1
        elif self.orientation == 3:
            self.y += 1


# state of 0 is white, state of 1 is black
class GameSquare:

    def __init__(self, square_x, square_y):
        self.square_x = square_x
        self.square_y = square_y
        self.state = 0
        self.rectangle = Rectangle(Point(square_x * 10, square_y * 10), Point((square_x + 1) * 10, (square_y + 1) * 10))

    def flip_state(self):
        if self.state == 0:
            self.state = 1
        else:
            self.state = 0

    def get_state(self):
        return self.state

    def set_sq_state(self, state):
        self.state = state

    def draw_square(self, is_ant=False):
        if is_ant:
            self.rectangle.setOutline(color_rgb(0, 0, 0))
            self.rectangle.setFill(color_rgb(255, 0, 0))
        elif self.state == 0:
            self.rectangle.setOutline(color_rgb(0, 0, 0))
            self.rectangle.setFill(color_rgb(255, 255, 255))
        else:
            self.rectangle.setOutline(color_rgb(255, 255, 255))
            self.rectangle.setFill(color_rgb(0, 0, 0))

    def init_drawing(self):
        self.rectangle.draw(win)


def main():
    init_game_board()
    ant_list = [Ant(50, 50), Ant(45, 58), Ant(30, 73), Ant(30, 30)]
    loop_forever(ant_list)

    win.getMouse()
    win.close()


def init_game_board():
    for i in range(0, HEIGHT):
        x = []
        for j in range(0, WIDTH):
            obj = GameSquare(i, j)
            x.append(obj)

            # Randomly picks starting square color based on the distribution that you want
            if random.randint(1, 100) <= PER_WHITE_INIT:
                obj.set_sq_state(0)
                obj.draw_square()
            else:
                obj.set_sq_state(1)
                obj.draw_square()

            obj.init_drawing()
        game_board.append(x)


def loop_forever(ant_list):
    already_flipped_squares = []
    while True:

        # Remove ants that have gone off the sides
        for ant in ant_list.copy():
            ant_x_pos = ant.x
            ant_y_pos = ant.y
            if ant_x_pos > 99 or ant_x_pos < 0 or ant_y_pos > 99 or ant_y_pos < 0:
                ant_list.remove(ant)
                print("An ant has died RIP")

        if len(ant_list) == 0:
            print("All ants have died :(")
            break

        # Draw ant squares
        for ant in ant_list:
            ant_x_pos = ant.x
            ant_y_pos = ant.y
            sq = get_game_sq(ant_x_pos, ant_y_pos)
            sq.draw_square(is_ant=True)

        # time.sleep(0.25)

        for ant in ant_list:
            ant_x_pos = ant.x
            ant_y_pos = ant.y

            # Checks if more than one ant are on the same square. Only one flip allowed per cycle.
            if not already_flipped(ant_x_pos, ant_y_pos, already_flipped_squares):
                get_game_sq(ant_x_pos, ant_y_pos).flip_state()
                already_flipped_squares.append([ant_x_pos, ant_y_pos])

            get_game_sq(ant_x_pos, ant_y_pos).draw_square()

            # Update the ant's position
            if game_board[ant_x_pos][ant_y_pos].get_state() == 0:
                ant.clock_wise_rotation()
            else:
                ant.counter_clock_wise_rotation()

            ant.ant_move()

        already_flipped_squares.clear()


def already_flipped(ant_x_pos, ant_y_pos, already_flipped_squares):
    for x, y in already_flipped_squares:
        if ant_x_pos == x and ant_y_pos == y:
            return True
    return False


def get_game_sq(x, y):
    return game_board[x][y]


main()
