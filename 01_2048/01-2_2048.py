"""
Clone of 2048 game.
"""

import poc_2048_gui
import random

# Directions, DO NOT MODIFY
UP = 1
DOWN = 2
LEFT = 3
RIGHT = 4

# Offsets for computing tile indices in each direction.
# DO NOT MODIFY this dictionary.
OFFSETS = {UP: (1, 0),
           DOWN: (-1, 0),
           LEFT: (0, 1),
           RIGHT: (0, -1)}

def merge(line):
    """
    Helper function that merges a single row or column in 2048
    """
    numbers = list_numbers(line)
    zeroes = list_zeroes(line)
    merged_tiles = []

    for item in range(len(numbers)):
        if len(merged_tiles) == 0:
            merged_tiles.append(numbers[item])
        elif merged_tiles[-1] == 0:
            merged_tiles[-1] += numbers[item]
            zeroes.append(0)
        elif merged_tiles[-1] == numbers[item]:
            merged_tiles[-1] += numbers[item]
            merged_tiles.append(0)
        else:
            merged_tiles.append(numbers[item])

    merged = merged_tiles + zeroes
    return merged

def list_zeroes(line):
    """
    Takes a list of integers and removes all non-zero elements.
    """
    zeroes = []
    for item in line:
        if item == 0:
            zeroes.append(item)
    return zeroes

def list_numbers(line):
    """
    Takes a list of integers and removes all zero elements.
    """
    numbers = []
    for item in line:
        if item > 0:
            numbers.append(item)
    return numbers

class TwentyFortyEight:
    """
    Class to run the game logic.
    """

    def __init__(self, grid_height, grid_width):
        self._grid_height = grid_height
        self._grid_width = grid_width
        self._directions = {UP: [], DOWN: [], LEFT: [], RIGHT: []}

        for col in range(grid_width):
            self._directions[UP].append((0, col))
            self._directions[DOWN].append((grid_height - 1, col))
        for row in range(grid_height):
            self._directions[LEFT].append((row, 0))
            self._directions[RIGHT].append((row, grid_width - 1))
        self.reset()

    def reset(self):
        """
        Reset the game so the grid is empty except for two
        initial tiles.
        """
        self._grid = [[0 for dummy_col in range(self._grid_width)]
                      for dummy_row in range(self._grid_height)]
        self._empty = self.get_empty()
        self.new_tile()
        self.new_tile()

    def __str__(self):
        """
        Return a string representation of the grid for debugging.
        """
        return '\n'.join(str(row) for row in self._grid)

    def get_grid_height(self):
        """
        Get the height of the board.
        """
        return self._grid_height

    def get_grid_width(self):
        """
        Get the width of the board.
        """
        return self._grid_width

    def move(self, direction):
        """
        Move all tiles in the given direction and add
        a new tile if any tiles moved.
        """
        changed = False
        if direction == UP or direction == DOWN:
            max_steps = self._grid_height
        else:
            max_steps = self._grid_width

        for initial in self._directions[direction]:
            to_merge = []
            for step in range(max_steps):
                row = initial[0] + step * OFFSETS[direction][0]
                col = initial[1] + step * OFFSETS[direction][1]
                to_merge.append(self.get_tile(row, col))
            merged = merge(to_merge)
            if merged != to_merge:
                changed = True

            for step in range(max_steps):
                row = initial[0] + step * OFFSETS[direction][0]
                col = initial[1] + step * OFFSETS[direction][1]
                self.set_tile(row, col, merged[step])
        if changed == True:
            self.new_tile()

    def new_tile(self):
        """
        Create a new tile in a randomly selected empty
        square.  The tile should be 2 90% of the time and
        4 10% of the time.
        """
        self.get_empty()
        if len(self._empty) > 0:
            tile_loc = random.choice(self._empty)
            randomizer = random.random()
            if randomizer < .9:
                tile_value = 2
            else:
                tile_value = 4
            self.set_tile(tile_loc[0], tile_loc[1], tile_value)


    def set_tile(self, row, col, value):
        """
        Set the tile at position row, col to have the given value.
        """
        self._grid[row][col] = value

    def get_tile(self, row, col):
        """
        Return the value of the tile at position row, col.
        """
        return self._grid[row][col]

    def get_empty(self):
        """
        Return list of empty cells.
        """
        self._empty = []
        for row in range(len(self._grid)):
            for col in range(len(self._grid[row])):
                if self._grid[row][col] == 0:
                    self._empty.append([row, col])
        return self._empty

poc_2048_gui.run_gui(TwentyFortyEight(4, 4))
