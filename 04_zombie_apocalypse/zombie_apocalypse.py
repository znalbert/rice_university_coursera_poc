"""
Student portion of Zombie Apocalypse mini-project
"""

import random
import poc_grid
import poc_queue
import poc_zombie_gui

# global constants
EMPTY = 0
FULL = 1
FOUR_WAY = 0
EIGHT_WAY = 1
OBSTACLE = 5
HUMAN = 6
ZOMBIE = 7


class Apocalypse(poc_grid.Grid):
    """
    Class for simulating zombie pursuit of human on grid with
    obstacles
    """

    def __init__(self, grid_height, grid_width, obstacle_list = None,
                 zombie_list = None, human_list = None):
        """
        Create a simulation of given size with given obstacles,
        humans, and zombies
        """
        poc_grid.Grid.__init__(self, grid_height, grid_width)
        if obstacle_list != None:
            for cell in obstacle_list:
                self.set_full(cell[0], cell[1])
        if zombie_list != None:
            self._zombie_list = list(zombie_list)
        else:
            self._zombie_list = []
        if human_list != None:
            self._human_list = list(human_list)
        else:
            self._human_list = []

    def clear(self):
        """
        Set cells in obstacle grid to be empty
        Reset zombie and human lists to be empty
        """
        self._zombie_list = []
        self._human_list = []
        poc_grid.Grid.clear(self)

    def add_zombie(self, row, col):
        """
        Add zombie to the zombie list
        """
        self._zombie_list.append((row, col))

    def num_zombies(self):
        """
        Return number of zombies
        """
        return len(self._zombie_list)

    def zombies(self):
        """
        Generator that yields the zombies in the order they were
        added.
        """
        # replace with an actual generator
        for zombie in self._zombie_list:
            yield zombie

    def add_human(self, row, col):
        """
        Add human to the human list
        """
        self._human_list.append((row, col))

    def num_humans(self):
        """
        Return number of humans
        """
        return len(self._human_list)

    def humans(self):
        """
        Generator that yields the humans in the order they were added.
        """
        # replace with an actual generator
        for human in self._human_list:
            yield human

    def compute_distance_field(self, entity_type):
        """
        Function computes and returns a 2D distance field
        Distance at member of entity_list is zero
        Shortest paths avoid obstacles and use four-way distances
        """
        visited = poc_grid.Grid(self._grid_height, self._grid_width)
        distance_field = [[self._grid_height * self._grid_width for dummy_col in range(self._grid_width)]
                       for dummy_row in range(self._grid_height)]
        boundary = poc_queue.Queue()
        if entity_type == HUMAN:
            for human in self.humans():
                boundary.enqueue(human)
                visited.set_full(human[0], human[1])
                distance_field[human[0]][human[1]] = 0
        elif entity_type == ZOMBIE:
            for zombie in self.zombies():
                boundary.enqueue(zombie)
                visited.set_full(zombie[0], zombie[1])
                distance_field[zombie[0]][zombie[1]] = 0

        while len(boundary) > 0:
            current_cell = boundary.dequeue()
            for neighbor in visited.four_neighbors(current_cell[0], current_cell[1]):
                if visited.is_empty(neighbor[0], neighbor[1]) and self.is_empty(neighbor[0], neighbor[1]):
                    visited.set_full(neighbor[0], neighbor[1])
                    boundary.enqueue((neighbor[0], neighbor[1]))
                    distance_field[neighbor[0]][neighbor[1]] = distance_field[current_cell[0]][current_cell[1]] + 1

        return distance_field

    def move_humans(self, zombie_distance_field):
        """
        Function that moves humans away from zombies, diagonal moves
        are allowed
        """

        for num_human in range(self.num_humans()):
            human = self._human_list[num_human]
            current_distance = zombie_distance_field[human[0]][human[1]]
            possible_moves = [human]

            for neighbor in self.eight_neighbors(human[0], human[1]):
                if self.is_empty(neighbor[0], neighbor[1]):
                    if zombie_distance_field[neighbor[0]][neighbor[1]] > current_distance:
                        current_distance = zombie_distance_field[neighbor[0]][neighbor[1]]
                        possible_moves = [neighbor]
                    elif zombie_distance_field[neighbor[0]][neighbor[1]] == current_distance:
                        possible_moves.append(neighbor)
            self._human_list[num_human] = random.choice(possible_moves)



    def move_zombies(self, human_distance_field):
        """
        Function that moves zombies towards humans, no diagonal moves
        are allowed
        """
        for num_zombie in range(self.num_zombies()):
            zombie = self._zombie_list[num_zombie]
            current_distance = human_distance_field[zombie[0]][zombie[1]]
            possible_moves = [zombie]

            for neighbor in self.four_neighbors(zombie[0], zombie[1]):
                if self.is_empty(neighbor[0], neighbor[1]):
                    if human_distance_field[neighbor[0]][neighbor[1]] < current_distance:
                        current_distance = human_distance_field[neighbor[0]][neighbor[1]]
                        possible_moves = [neighbor]
                    elif human_distance_field[neighbor[0]][neighbor[1]] == current_distance:
                        possible_moves.append(neighbor)
            self._zombie_list[num_zombie] = random.choice(possible_moves)

# Start up gui for simulation - You will need to write some code above
# before this will work without errors

poc_zombie_gui.run_gui(Apocalypse(30, 40))

#test = Apocalypse(4, 6)
#test.add_human(1, 4)
#test.add_human(3, 0)
#test.add_zombie(1, 1)
#test.add_zombie(3, 3)
#print test.compute_distance_field(7)
