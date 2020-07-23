from graphics import *
import time

win = GraphWin("Langton's Ant", 1000, 1000)
game_board = []
WIDTH = 100
HEIGHT = 100


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

    def draw_ant_square(self):
        sq = Rectangle(Point(self.x * 10, self.y * 10), Point((self.x + 1) * 10, (self.y + 1) * 10))
        sq.setOutline(color_rgb(0, 0, 0))
        sq.setFill(color_rgb(255, 0, 0))
        sq.draw(win)

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

    def flip_state(self):
        if self.state == 0:
            self.state = 1
        else:
            self.state = 0

    def get_state(self):
        return self.state


def main():
    for j in range(0, WIDTH):
        for i in range(0, HEIGHT):
            draw_square(j, i)

    init_game_board()
    ant = Ant(50, 50)
    loop_forever(ant)

    win.getMouse()
    win.close()


def init_game_board():
    for i in range(0, HEIGHT):
        x = []
        for j in range(0, WIDTH):
            x.append(GameSquare(j, i))
        game_board.append(x)


def loop_forever(ant):
    while True:
        ant.draw_ant_square()

        # update the square that the ant was just on
        ant_x_pos = ant.x
        ant_y_pos = ant.y
        try:
            game_board[ant_x_pos][ant_y_pos].flip_state()
        except IndexError:
            break

        draw_square(ant_x_pos, ant_y_pos, game_board[ant_x_pos][ant_y_pos].get_state())

        # Update the ant's position
        if game_board[ant_x_pos][ant_y_pos].get_state() == 0:
            ant.clock_wise_rotation()
        else:
            ant.counter_clock_wise_rotation()

        ant.ant_move()


def draw_square(x, y, state=0):
    sq = Rectangle(Point(x * 10, y * 10), Point((x + 1) * 10, (y + 1) * 10))

    if state == 0:
        sq.setOutline(color_rgb(0, 0, 0))
        sq.setFill(color_rgb(255, 255, 255))
    else:
        sq.setOutline(color_rgb(255, 255, 255))
        sq.setFill(color_rgb(0, 0, 0))

    sq.draw(win)


main()
