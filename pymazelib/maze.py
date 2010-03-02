#!/usr/bin/python

from random import randint

# directions
(NORTH, EAST, SOUTH, WEST) = range(4)
DIRECTIONS = 4

# how to represent a cell depending on its walls.
CELL = '0123456789abcdef'

def opposite_direction(dir):
  """Return the opposite of the given direction.

  """
  return (dir + DIRECTIONS / 2) % DIRECTIONS

class Cell(object):
  def __init__(self, coords):
    """Create a new cell with all its walls. The given coordinates represent
    the position of the cell inside the maze.

    """
    self.coords = coords
    self.walls = [True, True, True, True]
    self.directions = [False, False, False, False]
    self.neighbors = [None, None, None, None]
    self.start = False
    self.end = False
    self.carved = False
    self.active = False
    self.backward = False

  def knock_down(self, dir):
    """Knock down the wall facing at the given direction.

    """
    self.walls[dir] = False
    self.directions[dir] = True

  def intact_walls(self):
    """Return a list of not knocked down walls.

    """
    return [dir for dir in xrange(DIRECTIONS) if self.walls[dir]]

  def open_directions(self):
    """Return the open directions of the current cell.

    """
    return [dir for dir in xrange(DIRECTIONS) if self.directions[dir]]

  def __str__(self):
    """Return a character representing the state of the cell. The state is
    given by the walls which have not been knocked down.

    """
    i = 0
    for (n, valid) in revered(self.walls):
      i += int(valid) * (2 ** n)
    return CELL[i]

class Maze(object):
  def __init__(self, rows, columns):
    """Create an empty maze of the given dimensions.

    """
    self.size = (rows, columns)
    self.grid = [[Cell((i, j)) for j in xrange(columns)] for i in xrange(rows)]
    for i in xrange(rows):
      for j in xrange(columns):
        self.grid[i][j].neighbors = self.neighbors(i, j)
    self.grid[0][0].start = True
    self.grid[rows - 1][columns - 1].end = True
    self.modified = []

  def random(self):
    """Return a random cell taken from the grid.

    """
    (rows, columns) = self.size
    (i, j) = (randint(0, rows - 1), randint(0, columns - 1))
    return self.grid[i][j]

  def neighbors(self, i, j):
    """Return an array containing the neighbors of the given cell and the
    direction from the current cell. The neighbors are searched clockwise
    direction, starting from north.

    """
    (rows, columns) = self.size
    neighborhood = [None, None, None, None]
    if (i > 0): neighborhood[NORTH] = self.grid[i - 1][j]
    if (j < columns - 1): neighborhood[EAST] = self.grid[i][j + 1]
    if (i < rows - 1): neighborhood[SOUTH] = self.grid[i + 1][j]
    if (j > 0): neighborhood[WEST] = self.grid[i][j - 1]
    return neighborhood

  def __getitem__(self, coord):
    """Return the cell addressed by the given coordinates.

    """
    (i, j) = coord
    return self.grid[i][j]

  def __str__(self):
    """Return rows * colums characters separated by a new line. Each character
    is the representation of the state of a cell.

    """
    repr = '%d %d\n' % self.size
    for (i, row) in enumerate(self.grid):
      if i != 0:
        repr += '\n'
      repr += ''.join(map(str, row))
    return repr
