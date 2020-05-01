"""
    File: sense_battleship.py
    Author: Andrew Quamme
    Purpose: Raspberry Pi Sense Hat implementation of
    CSC-120 Week 4 Long Problem
    This is a one-sided game of "Battleship". Ship placements are
    read in from a text file and placed on the game board. Guesses
    are then read in from a text file and processed. There are various
    errors that can occur, and the program attempts to handle them.
"""

import sys
from sense_emu import SenseHat
from time import sleep

class GridPos(object):
    """
    An instance of this class represents a grid position on the board

    Attributes:
        _x -- x coordinate of position
        _y -- y coordinate of position
        _ship -- Ship object at position
        _guessed -- boolean if position has been guessed
        _visual -- visual representation of the space
                   - for empty, O for miss, X for hit

    Methods:
        get_x() -- get x coordinate
        get_y() -- get y coordinate
        was_guessed() -- check if space was guessed
        set_guessed() -- set position as guessed
        miss() -- process a miss at position
        hit() -- process a hit at position
        contains_ship() -- check if space contains a ship
        set_ship_at_pos() -- set ship at position
    """

    def __init__(self, x, y):
        """
        Initializes a GridPos object from an x and y coordinate

        Parameters:
            x -- x coordinate
            y -- y coordinate

        Pre-Condition:
            An existing game board

        Post-Condition:
            An instance of a GridPos object
        """
        self._x = x
        self._y = y
        self._ship = None
        self._guessed = False
        self._visual = '-'

    def get_x(self):
        """
        Get x coordinate of position
        """
        return self._x

    def get_y(self):
        """
        Get y coordinate of position
        """
        return self._y

    def was_guessed(self):
        """
        Get guessed status of position
        """
        return self._guessed

    def set_guessed(self):
        """
        Set position as guessed
        """
        self._guessed = True

    def miss(self):
        """
        Processes a miss at position
        """
        print("miss")
        self.set_guessed()
        self._visual = 'O'

    def hit(self):
        """
        Processes a hit at position
        """
        self.set_guessed()
        self._visual = 'X'
        self._ship.hit()

    def contains_ship(self):
        """
        Check if position contains a ship
        """
        return self._ship is not None

    def set_ship_at_pos(self, ship):
        """
        Set ship at position
        """
        self._ship = ship
        self._visual = ship.get_style()

    def __str__(self):
        """
        String representation of GridPos
        """
        return self._visual


class Board(object):
    """
    An instance of this class represents a game board

    Attributes:
        _grid -- 2d list of GridPos objects
        _ships -- list of ships on board

    Methods:
        place_ship(ship) -- place Ship object onto board
        guess(x, y) -- fire a shot at position x, y
    """

    def __init__(self, n):
        """
        Initializes a Board object of size n x n

        Parameters:
            n -- size for n x n grid to create

        Post-Condition:
            An instance of a Board object
        """
        self._grid = []
        self._ships = []
        self._sense = SenseHat()
        self._sense.clear(0,0,255)

        for i in range(n):
            row = []
            for j in range(n):
                new_pos = GridPos(i, j)
                row.append(new_pos)
            self._grid.append(row)

    def place_ship(self, ship):
        """
        Places a ship onto the board

        Parameters:
            ship -- ship to add

        Returns:
            T/F if ship was successfully placed without
            overlapping an existing ship

        Pre-Condition:
            Ship is valid

        Post-Condition:
            Ship object is added to the board and list of ships
        """
        success = True
        self._ships.append(ship)
        positions = ship.get_positions()
        for pos in positions:
            print(pos)
            x, y = (pos[1], pos[0])
            current = self._grid[-1 - x][y]
            if current.contains_ship():
                success = False
            else:
                current.set_ship_at_pos(ship)
##                self._sense.set_pixel(x,y,0,0,0)
        return success

    def guess(self, x, y):
        """
        Processes a guess at position x, y
        After guess is processed, any sunken ships are
        removed from the list of ships. If all ships are
        removed, the game ends.

        Parameters:
            x -- x coordinate of guess
            y -- y coordinate of guess

        Pre-Conditions:
            Guess is valid
        """
        print(x,y)
        if 0 <= x < len(self._grid[0]) and 0 <= y < len(self._grid):
            current = self._grid[-1 - x][y]
            if not current.contains_ship() and not current.was_guessed():
                current.miss()
##                self._sense.set_pixel(x, y, 255,255,255)
            elif not current.contains_ship() and current.was_guessed():
                print("miss (again)")
            elif current.contains_ship() and not current.was_guessed():
                current.hit()
##                self._sense.set_pixel(x, y, 255,0,0)
            elif current.contains_ship() and current.was_guessed():
                print("hit (again)")
        else:
            print("illegal guess")

        for ship in self._ships:
            if ship.is_sunk():
                self._ships.remove(ship)

        if len(self._ships) == 0:
            print("all ships sunk: game over")
            sys.exit(0)

    def __str__(self):
        """
        String representation of the game board. When printed,
        shows a visual of the current game board
        """
        results = ""
        for i in range(len(self._grid)):
            results += f"{len(self._grid)- 1 - i}\t"
            for j in range(len(self._grid[0])):
                results += str(self._grid[i][j]) + '\t'
            results += '\n'
        for i in range(len(self._grid)):
            results += f"\t{i}"
        return results

    def __len__(self):
        """
        Used to determine the bounds of the game board
        """
        return len(self._grid)


class Ship(object):
    """
    An instance of this class represents a ship

    Attributes:
        _style -- style of ship (carrier, sub, etc)
        _health -- hits remaining until ship is sunk
        _startpos -- starting coordinates of ship
        _endpos -- ending coordinates of ship
        _sunk -- if ship is sunk or not

    Methods:
        get_positions() -- returns a list of positions that the
                           ship occupies
        hit() -- process a hit on the ship
        get_style -- get the style of the ship]
        is_sunk -- returns T/F if ship is sunk
    """

    def __init__(self, style, size, startpos, endpos):
        """
        Initializes a Ship object from a line of placement data

        Parameters:
            style -- style of ship
            size -- size of ship
            startpos -- starting coordinates of ship
            endpos -- ending coordinates of ship

        Pre-Condition:
            A valid line of data (ship will be in-bounds,
            correct length, and is either horizontal or vertical)

        Post-Condition:
            An instance of a Ship object to be placed onto board
        """
        self._style = style
        self._health = size
        self._startpos = startpos
        self._endpos = endpos
        self._sunk = False

    def get_positions(self):
        """
        Returns a list of positions that the ship occupies
        """
        positions = []

        if self._startpos[0] == self._endpos[0]:
            # vertical
            for i in range(self._startpos[1], self._endpos[1]+1):
                positions.append((self._startpos[0], i))
        elif self._startpos[1] == self._endpos[1]:
            # horizontal
            for i in range(self._startpos[0], self._endpos[0]+1):
                positions.append((i, self._startpos[1]))
        return positions

    def hit(self):
        """
        Processes a hit on the ship:
            Takes 1 off ship's health and checks if ship is sunk
        """
        self._health -= 1
        if self._health == 0:
            print(f"{self} sunk")
            self._sunk = True
        else:
            print("hit")

    def get_style(self):
        """
        Returns the style of the ship
        """
        return self._style

    def is_sunk(self):
        """
        Returns if ship has been sunk
        """
        return self._sunk

    def __str__(self):
        """
        String representation of ship
        """
        return f"{self._style}"


def load_file(filename):
    """
    Opens a file and returns a list of lines in the file
    """
    results = []
    infile = open(filename, 'r')
    for line in infile:
        data = line.strip()
        if data != "":
            results.append(data)
    infile.close()
    return results


def check_ship_in_bounds(width, pos1, pos2):
    """
    Used to determine if a ship will be in-bounds on the board

    Parameters:
        width -- width of game board
        pos1 -- x1, y1
        pos2 -- x2, y2

    Return:
        True -- pos1 and pos2 are within the bounds of board
        False -- pos1 or pos2 are out-of-bounds
    """
    return (pos1[0] >= 0 and
            pos2[0] < width and
            pos1[1] >= 0 and
            pos2[1] < width)


def check_ship_horizontal_vertical(pos1, pos2):
    """
    Determines if ship is either horizontal or vertical

    Parameters:
        pos1 -- x1, y1
        pos2 -- x2, y2

    Return:
        True -- ship is either horizontal or vertical
        False -- ship is neither horizontal nor vertical
    """
    return pos1[0] == pos2[0] or pos1[1] == pos2[1]


def check_ship_correct_size(length, pos1, pos2):
    """
    Checks if the distance between two positions is the correct length
    of the ship to be created

    Parameters:
        length -- length of ship to be checked
        pos1 -- x1, y1
        pos2 -- x2, y2

    Return:
        True -- ship will be the correct size
        False -- ship will be too long or too short
    """
    return pos2[0] - pos1[0] + 1 == length or pos2[1] - pos1[1] + 1 == length


def process_placement_file(board, file):
    """
    Processees a placement file to create ships and place them
    onto the game board. Also checks to ensure that ships will be valid

    Parameters:
        board -- game board
        file -- file contents to be processed

    Pre-Condition:
        File was opened successfully and lines of data added to a list

    Post-Condition:
        Game board with ships placed ready to play
    """
    ship_dict = {'A': 5, 'B': 4, 'S': 3, 'D': 3, 'P': 2}

    for line in file:
        data = line.split()
        style = data[0]
        if style in ship_dict.keys():
            size = ship_dict[style]
            x1, y1, x2, y2 = map(int, data[1:])
            x = sorted([x1, x2])
            y = sorted([y1, y2])
            startpos = (x[0], y[0])
            endpos = (x[1], y[1])

            if not check_ship_in_bounds(len(board), startpos, endpos):
                print("ERROR: ship out-of-bounds: " + line)
                sys.exit(1)
            elif not check_ship_horizontal_vertical(startpos, endpos):
                print("ERROR: ship not horizontal or vertical " + line)
                sys.exit(1)
            elif not check_ship_correct_size(size, startpos, endpos):
                print("ERROR: incorrect ship size " + line)
                sys.exit(1)
            else:
                new_ship = Ship(style, size, startpos, endpos)
                successful_placement = board.place_ship(new_ship)
                if not successful_placement:
                    print("ERROR: overlapping ship " + line)
                    sys.exit(1)
                del ship_dict[style]
        else:
            print("ERROR: fleet composition incorrect")
            sys.exit(1)

    if len(ship_dict) > 0:
        print("ERROR: fleet composition incorrect")
        sys.exit(1)


def process_guess_file(board, file):
    """
    Processees a guess file to fire shots in the game

    Parameters:
        board -- game board
        file -- file contents to be processed

    Pre-Condition:
        File was opened successfully and lines of data added to a list
        Game board with ships placed
    """
    for line in file:
        try:
            x, y = map(int, line.split())
            board.guess(x, y)
        except ValueError:
            print("illegal guess")


def main():
    try:
##        placements = load_file(input())
##        guesses = load_file(input())
        placements = load_file('battleship_placements.txt')
        guesses = load_file('battleship_guesses.txt')
    except FileNotFoundError:
        print("ERROR: fleet composition incorrect")
        sys.exit(1)

    board = Board(8)
    process_placement_file(board, placements)
    print(board)
    input('Press a key to guess')
    process_guess_file(board, guesses)


if __name__ == "__main__":
    main()
