"""
Samuel Guttormson

The following will generate automaton using the pygame engine given John conway's rules.
The project is a fork of my original cellular automata project, and thus features 
that don't pertain to conways game of life in pygame are removed.

The main variables for the user to play with at this time are:

    Cell Grid Size: defined in creation of Automaton object

    The initial state: Only random noise method exists in this fork
        - random noise generating multiple live cells all over the grid, based on an intensity parameter.

"""

import random, time
import numpy as np
# import cupy as cp


from Viewer import Viewer
class Automaton:
    def __init__(self, w, h, color_func):
        """
        :params w, h: respective width and height of cell grid
        :return: A new Automaton object
        """

        #Initialize a 2d array of w*h size with 0's (empty cell grid)
        x = [[0 for i in range(w)] for j in range(h)]
        np_x = np.array(x)

        self.dict = {
            'width': w,
            'height': h,
            'current_state': np_x,
            'steps': 0,
            'color_func': color_func,
            'counter': 0 
        }

    def initialize_with_noise(self, intensity):
        """
        Initializes cell grid with random noise
        :param intensity: An integer value that scales how many random cells should be revived.
        Smaller intensity value means more live cells.
        """
        #A list containing the two choices, alive or dead
        r = [0, 255]
        #The more zeros added from intensity, the more dead cells
        for i in range(intensity):
            r.append(0)
        image = self.dict['current_state']
        for (x, y), element in np.ndenumerate(image):
            image[x][y] = random.choice(r)


    def is_alive(self, cell):
        """
        :param cell: A single cell value from the state grid
        :returns: True if cell is alive and otherwise false 
        """
        if (cell > 0): return True
        else: return False 

    def is_within_bounds(self, x, y):
        """
        Determines if x and y are within the bounds of the cellular grid
        :params x, y: x and y index values
        :returns: True if index values are not out of bounds
        """
        if x in range(0, self.dict['width']) and y in range(0, self.dict['height']):
            return True

    def update(self):
        """
        Determines what the next state will look like given the current state
        This is where rulesets are created.
        """
        image_copy = self.dict['current_state'].copy()
        image = self.dict['current_state']
        radius = 1
        # start = time.time()
        for (x, y), element in np.ndenumerate(image):
            total = image[x-radius:x+(radius+1), y-radius:y+(radius+1)].sum()
            if self.is_alive(element):
                total -= 255
            if total < 256:
                if self.is_alive(element):
                    self.kill_cell(image_copy, x, y)
            elif total > 765:
                self.kill_cell(image_copy, x, y)
            elif total == 765:
                if self.is_alive(element) == False:
                    self.revive_cell(image_copy, x, y)
        
        # print(time.time() - start)
        self.dict['current_state'] = image_copy.copy()
        return (image, self.update_steps())

    def update_steps(self):
        self.dict['steps'] +=1
        return self.dict['steps']

    def revive_cell(self, image, x, y):
        """
        Play god and bring the specified cell back from the dead
        :param image: a reference to a cell grid to modify
        :params x, y: x and y coordinates of the dead cell in the provided cell grid
        """
        if self.is_within_bounds(x, y):
            image[x][y] = self.dict['color_func'](x, y)
                
    def kill_cell(self, image, x, y):
        """
        Kills the specified cell 
        :param image: a reference to a cell grid to modify
        :params x, y: x and y coordinates of the living cell in the provided cell grid
        """
        if self.is_within_bounds(x, y):
            image[x][y] = 0


def color_function(x, y):
    """
    This is a fork of my original automata project, and color should be left 255 (white).
    """
    #setting a return of 255 defaults automaton to simple black and white (dead and alive)
    return 255

#Create a new Automaton Object
new_automaton = Automaton(200, 200, color_function)

#There are three methods to choose from for generating an initial state:
new_automaton.initialize_with_noise(12)

#Initializes the pygame viewer object and starts
viewer = Viewer(new_automaton.update, (900, 900))
viewer.start()
