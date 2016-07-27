"""
Loyd's Fifteen puzzle - solver and visualizer
Note that solved configuration has the blank (zero) tile in upper left
Use the arrows key to swap this tile with its neighbors
"""

import poc_fifteen_gui
#import poc_simpletest as simpletest

class Puzzle:
    """
    Class representation for the Fifteen puzzle
    """

    def __init__(self, puzzle_height, puzzle_width, initial_grid=None):
        """
        Initialize puzzle with default height and width
        Returns a Puzzle object
        """
        self._height = puzzle_height
        self._width = puzzle_width
        self._grid = [[col + puzzle_width * row
                       for col in range(self._width)]
                      for row in range(self._height)]

        if initial_grid != None:
            for row in range(puzzle_height):
                for col in range(puzzle_width):
                    self._grid[row][col] = initial_grid[row][col]

    def __str__(self):
        """
        Generate string representaion for puzzle
        Returns a string
        """
        ans = ""
        for row in range(self._height):
            ans += str(self._grid[row])
            ans += "\n"
        return ans

    #####################################
    # GUI methods

    def get_height(self):
        """
        Getter for puzzle height
        Returns an integer
        """
        return self._height

    def get_width(self):
        """
        Getter for puzzle width
        Returns an integer
        """
        return self._width

    def get_number(self, row, col):
        """
        Getter for the number at tile position pos
        Returns an integer
        """
        return self._grid[row][col]

    def set_number(self, row, col, value):
        """
        Setter for the number at tile position pos
        """
        self._grid[row][col] = value

    def clone(self):
        """
        Make a copy of the puzzle to update during solving
        Returns a Puzzle object
        """
        new_puzzle = Puzzle(self._height, self._width, self._grid)
        return new_puzzle

    ########################################################
    # Core puzzle methods

    def current_position(self, solved_row, solved_col):
        """
        Locate the current position of the tile that will be at
        position (solved_row, solved_col) when the puzzle is solved
        Returns a tuple of two integers
        """
        solved_value = (solved_col + self._width * solved_row)

        for row in range(self._height):
            for col in range(self._width):
                if self._grid[row][col] == solved_value:
                    return (row, col)
        assert False, "Value " + str(solved_value) + " not found"

    def update_puzzle(self, move_string):
        """
        Updates the puzzle state based on the provided move string
        """
        zero_row, zero_col = self.current_position(0, 0)
        for direction in move_string:
            if direction == "l":
                assert zero_col > 0, "move off grid: " + direction
                self._grid[zero_row][zero_col] = self._grid[zero_row][zero_col - 1]
                self._grid[zero_row][zero_col - 1] = 0
                zero_col -= 1
            elif direction == "r":
                assert zero_col < self._width - 1, "move off grid: " + direction
                self._grid[zero_row][zero_col] = self._grid[zero_row][zero_col + 1]
                self._grid[zero_row][zero_col + 1] = 0
                zero_col += 1
            elif direction == "u":
                assert zero_row > 0, "move off grid: " + direction
                self._grid[zero_row][zero_col] = self._grid[zero_row - 1][zero_col]
                self._grid[zero_row - 1][zero_col] = 0
                zero_row -= 1
            elif direction == "d":
                assert zero_row < self._height - 1, "move off grid: " + direction
                self._grid[zero_row][zero_col] = self._grid[zero_row + 1][zero_col]
                self._grid[zero_row + 1][zero_col] = 0
                zero_row += 1
            else:
                assert False, "invalid direction: " + direction

    ##################################################################
    # Phase one methods

    def lower_row_invariant(self, target_row, target_col):
        """
        Check whether the puzzle satisfies the specified invariant
        at the given position in the bottom rows of the puzzle (target_row > 1)
        Returns a boolean
        """
        # Condition 1 - Tile zero is positioned at (i,j)
        if self.get_number(target_row, target_col) != 0:
            return False

        # Condition 2 - All tiles in rows i+1 or below are at their solved location
        row = self._height - 1

        while row > target_row:
            col = self._width
            while col > 0:
                col -= 1
                if self.current_position(row, col) != (row, col):
                    return False
            row -= 1

        # Condition 3 - All tiles in row i to the right of position (i,j) are at their solved location
        if row == target_row:
            if target_col < self._width - 1:
                col = self._width - 1
                while col > target_col:
                    if self.current_position(row, col) != (row, col):
                        return False
                    col -= 1
        return True

#		I wanted to do this with recursion, but had trouble because of the 0 tile
#        might come back to this.
#        if target_row == self._height - 1 and target_col == self._width - 1:
#            if self.get_number(target_row, target_col) == 0:
#                return True
#            else:
#                return check_solved
#        else:
#            if target_col < self._width - 1:
#                target_col += 1
#            else:
#                target_row += 1
#                target_col = 0
#
#            check_solved = self.current_position(target_row, target_col) == (target_row, target_col)
#
#            if not check_solved:
#                return check_solved
#            elif target_row == self._height - 1 and target_col == self._width - 1:
#                return check_solved
#            else:
#                return self.lower_row_invariant(target_row, target_col)


    def solve_interior_tile(self, target_row, target_col):
        """
        Place correct tile at target position
        Updates puzzle and returns a move string
        """
        assert self.lower_row_invariant(target_row, target_col), "Failed pre-test lower_row_invariant"

        tile_row, tile_col = self.current_position(target_row, target_col)

        moves = self._position_tile(target_row, target_col, tile_row, tile_col)

        self.update_puzzle(moves)
        assert self.lower_row_invariant(target_row, target_col - 1), "Failed post-test lower_row_invariant"

        return moves


    def _position_tile(self, target_row, target_col, tile_row, tile_col):
        """
        Takes a tile and moves it to a target location.
        """
        moves = ""

        zero_row, zero_col = target_row, target_col

        #tile_row, tile_col = self.current_position(target_row, target_col)

        # Change horizontal position of tile to be above target position
        if tile_col != target_col:
            if tile_row == 0:
                moves += self.move_tile_off_row0(zero_row, zero_col,
                                                 tile_row, tile_col)
                zero_row, zero_col = tile_row, tile_col
                tile_row += 1
            else:
                moves += self.move_zero_above_tile(zero_row, zero_col,
                                                   tile_row, tile_col)
                zero_row, zero_col = tile_row - 1, tile_col

            moves += self.move_tile_horizontally(target_col, zero_col, tile_col)
            zero_col = target_col
            tile_col = target_col

        if tile_col == target_col:
            moves += self.move_tile_vertically(zero_row, tile_row, target_row)

        return moves


    def _zero_direction(self, zero_col, tile_col):
        """
        Returns a direction dictionary and a direction for the movement of tiles.
        """
        hor_directions = {1: "r", -1: "l"}

        if zero_col < tile_col:
            hor_direction = 1
        else:
            hor_direction = -1

        return hor_directions, hor_direction


    def move_tile_off_row0(self, zero_row, zero_col, tile_row, tile_col):
        """
        Returns moves necessary to move the current tile off of row 0, and
        places the zero tile above it.
        """
        directions, direction = self._zero_direction(zero_col, tile_col)
        off_row0_moves = ""

        ups = (zero_row - (tile_row + 1))
        off_row0_moves += "u" * ups
        zero_row -= ups

        while zero_col != tile_col:
            off_row0_moves += directions[direction]
            zero_col += direction
        off_row0_moves += "u"

        return off_row0_moves


    def move_zero_above_tile(self, zero_row, zero_col, tile_row, tile_col):
        """
        Returns moves necessary to get the zero tile above the current tile.
        """
        directions, direction = self._zero_direction(zero_col, tile_col)
        above_tile_moves = ""

        ups = (zero_row - (tile_row - 1))
        above_tile_moves += "u" * ups
        zero_row -= ups

        while zero_col != tile_col:
            above_tile_moves += directions[direction]
            zero_col += direction

        return above_tile_moves


    def move_tile_horizontally(self,
                               target_col,
                               zero_col,
                               tile_col):
        """
        Returns moves necessary to get the current tile in the correct column
        when starting from a position of having the zero tile above the
        current tile.
        """
        directions, direction = self._zero_direction(tile_col, target_col)

        horizontal_moves = ""

        horizontal_move = directions[direction] + "d" + directions[-direction] + "u"

        while tile_col != target_col:
            if zero_col == tile_col:
                horizontal_moves += horizontal_move
                tile_col += direction
            else:
                horizontal_moves += directions[direction] + horizontal_move
                tile_col += direction
                zero_col += direction
        horizontal_moves += directions[direction]
        return horizontal_moves


    def move_tile_vertically(self, zero_row, tile_row, target_row):
        """
        Moves current tile in correct column down to correct row.
        """
        vertical_moves = ""

        if zero_row > tile_row:
            while zero_row > tile_row:
                vertical_moves += "u"
                zero_row -= 1
            tile_row += 1

        while tile_row < target_row:
            vertical_moves += "lddru"
            tile_row += 1
        vertical_moves += "ld"
        return vertical_moves


    def solve_col0_tile(self, target_row):
        """
        Solve tile in column zero on specified row (> 1)
        Updates puzzle and returns a move string
        """
        assert self.lower_row_invariant(target_row, 0), "Failed pre-test lower_row_invariant"

        first_move = "ur"
        moves = ""
        self.update_puzzle(first_move)
        zero_row, zero_col = target_row - 1, 1
        tile_row, tile_col = self.current_position(target_row, 0)

        if tile_row == target_row and tile_col == 0:
            moves += "r" * (self._width - 2)
        else:
            moves += self._position_tile(zero_row, zero_col, tile_row, tile_col)
            moves += "ruldrdlurdluurddlur" + "r" * (self._width - 2)

        self.update_puzzle(moves)
        assert self.lower_row_invariant(target_row - 1, self._width -1), "Failed post-test lower_row_invariant"

        return first_move + moves


    #############################################################
    # Phase two methods

    def row0_invariant(self, target_col):
        """
        Check whether the puzzle satisfies the row zero invariant
        at the given column (col > 1)
        Returns a boolean
        """
        # Row 0 - Tile zero is positioned at (0,j) and everything to the right is correct
        if self.get_number(0, target_col) != 0:
            return False

        for dummy_col0 in range(target_col + 1, self._width):
            if self.current_position(0, dummy_col0) != (0, dummy_col0):
                return False

        # Row 1 - All tiles from j to eol are correct
        for dummy_col1 in range(target_col, self._width):
            if self.current_position(1, dummy_col1) != (1, dummy_col1):
                return False

        # Remaining Rows - All tiles in correct positions
        row = self._height - 1

        while row > 1:
            col = self._width
            while col > 0:
                col -= 1
                if self.current_position(row, col) != (row, col):
                    return False
            row -= 1

        return True


    def row1_invariant(self, target_col):
        """
        Check whether the puzzle satisfies the row one invariant
        at the given column (col > 1)
        Returns a boolean
        """
        if not self.lower_row_invariant(1, target_col):
            return False

        for dummy_col0 in range(target_col + 1, self._width):
            if self.current_position(0, dummy_col0) != (0, dummy_col0):
                return False

        return True


    def solve_row0_tile(self, target_col):
        """
        Solve the tile in row zero at the specified column
        Updates puzzle and returns a move string
        """
        assert self.row0_invariant(target_col), "Failed pre-test row0_invariant"

        first_move = "ld"
        moves = ""
        self.update_puzzle(first_move)
        zero_row, zero_col = 1, target_col - 1
        tile_row, tile_col = self.current_position(0, target_col)

        if tile_col != target_col or tile_row != 0:
            moves += self._position_tile(zero_row, zero_col, tile_row, tile_col)
            moves += "urdlurrdluldrruld"
            self.update_puzzle(moves)

        assert self.row1_invariant(target_col - 1), "Failed post-test row1_invariant"

        return first_move + moves


    def solve_row1_tile(self, target_col):
        """
        Solve the tile in row one at the specified column
        Updates puzzle and returns a move string
        """
        assert self.row1_invariant(target_col), "Failed pre-test row1_invariant"

        tile_row, tile_col = self.current_position(1, target_col)

        moves = self._position_tile(1, target_col, tile_row, tile_col) + "ur"

        self.update_puzzle(moves)
        assert self.row0_invariant(target_col), "Failed post-test row0_invariant"

        return moves

    ###########################################################
    # Phase 3 methods

    def solve_2x2(self):
        """
        Solve the upper left 2x2 part of the puzzle
        Updates the puzzle and returns a move string
        """
        first_move = "ul"
        self.update_puzzle(first_move)
        if self.row0_invariant(0):
            return first_move
        else:
            moves = ""
            while not self.row0_invariant(0):
                moves += "rdlu"
                self.update_puzzle("rdlu")
        return first_move + moves

    def solve_puzzle(self):
        """
        Generate a solution string for a puzzle
        Updates the puzzle and returns a move string
        """
        moves = ""
        max_row = self._height - 1
        max_col = self._width - 1

        if self.row0_invariant(0):
            return moves

        # Find 0 and move it to the bottom right corner
        zero_row, zero_col = self.current_position(0, 0)

        if zero_row < max_row:
            moves += "d" * (max_row - zero_row)
        if zero_col < max_col:
            moves += "r" * (max_col - zero_col)
        self.update_puzzle(moves)

        # Update moves for rows > 1.
        for row in range(max_row, 1, -1):
            for col in range(max_col, -1, -1):
                if col == 0:
                    moves += self.solve_col0_tile(row)
                else:
                    moves += self.solve_interior_tile(row, col)

        # Update moves for rows 0 and 1 and cols > 1.
        for col in range(max_col, 1, -1):
            moves += self.solve_row1_tile(col)
            moves += self.solve_row0_tile(col)

        moves += self.solve_2x2()

        return moves
