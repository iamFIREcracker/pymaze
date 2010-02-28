#!/usr/bin/python

from random import randint
from random import shuffle

# directions
(NORTH, EAST, SOUTH, WEST) = (8, 4, 2, 1)

# how to represent a cell depending on its walls.
CELL = '0123456789abcdef'

# generating algorithms
(DEPTH_FIRST, RANDOMIZED_PRIM) = xrange(2)
algorithms = {'depth-first': DEPTH_FIRST,
              'randomized-prim': RANDOMIZED_PRIM,}

def opposite_direction(dir):
  """Return the opposite of the given direction.

  """
  if dir == NORTH: return SOUTH
  elif dir == EAST: return WEST
  elif dir == SOUTH: return NORTH
  elif dir == WEST: return EAST

def beyond_wall(i, j, dir, rows, columns):
  """Return the indices of the cell beyond the wall located at the given
  direction.

  """
  if dir == NORTH and i > 0: return (i - 1, j)
  elif dir == EAST and j < columns - 1: return (i, j + 1)
  elif dir == SOUTH and i < rows - 1: return (i + 1, j)
  elif dir == WEST and j > 0: return (i, j - 1)
  else: return (None, None)

class Cell(object):
  def __init__(self):
    """Create a new cell with all its walls.

    """
    self.north_wall = True
    self.east_wall = True
    self.south_wall = True
    self.west_wall = True

  def knock_down(self, direction):
    """Knock down the wall facing at the given direction.

    """
    if direction == NORTH:
      self.north_wall = False
    elif direction == EAST:
      self.east_wall = False
    elif direction == SOUTH:
      self.south_wall = False
    elif direction == WEST:
      self.west_wall = False

  def __str__(self):
    """Return a character representing the state of the cell. The state is
    given by the walls which have not been knocked down.

    """
    return None
    return CELL[self.walls]

class Maze(object):
  def __init__(self, rows, columns, algorithm):
    """Create an empty maze of the given dimensions.

    """
    self.size = (rows, columns)
    self.grid = [[Cell() for j in xrange(columns)] for i in xrange(rows)]
    self.modified = []
    self.algorithm = algorithm

  def neighbors(self, i, j):
    """Return an array containing the neighbors of the given cell and the
    direction from the current cell.

    """
    (rows, columns) = self.size
    neighborhood = []
    if (i > 0): neighborhood.append((NORTH, (i - 1, j)))
    if (j < columns - 1): neighborhood.append((EAST, (i, j + 1)))
    if (i < rows - 1): neighborhood.append((SOUTH, (i + 1, j)))
    if (j > 0): neighborhood.append((WEST, (i, j - 1)))
    shuffle(neighborhood)
    return neighborhood

  def generate_depth_first(self):
    """Generate the maze by using the depth-first algorithm.
    Basically with start at a random cell and we mark it as a visited. Then we
    look for neighbors which have not been visited yet, knock down the walls in
    between and change our current cell with the new one. We repeat these steps
    untill all the cells of the grid have been visited.  The function yields
    True if there is something else to do, False otherwise.

    """
    visited = {}
    (rows, columns) = self.size
    (i, j) = (randint(0, rows - 1), randint(0, columns - 1))
    visited[(i, j)] = True

    total = rows * columns
    cell_stack = [(i, j)]
    while len(visited) < total:
      (ci, cj) = cell_stack.pop()
      neighborhood = self.neighbors(ci, cj)
      for (dir, (ni, nj)) in neighborhood:
        if (ni, nj) not in visited:
          self.grid[ci][cj].knock_down(dir)
          self.grid[ni][nj].knock_down(opposite_direction(dir))
          cell_stack.append((ci, cj))
          cell_stack.append((ni, nj))
          visited[(ni, nj)] = True
          self.modified = [(ci, cj), (ni, nj)]
          yield True
          break
    yield False

  def generate_randomized_prim(self):
    """Generate the maze by using the randomized prim's algorithm.
    XXX

    """
    visited = {}
    (rows, columns) = self.size
    (i, j) = (randint(0, rows - 1), randint(0, columns - 1))
    visited[(i, j)] = True

    wall_stack = [(NORTH, (i, j)), (EAST, (i, j)),
                  (SOUTH, (i, j)), (WEST, (i, j))]
    while wall_stack:
      i = randint(0, len(wall_stack) - 1)
      (dir, (ci, cj)) = wall_stack.pop(i) 
      (ni, nj) = beyond_wall(ci, cj, dir, rows, columns)
      if ni is not None and nj is not None and (ni, nj) not in visited:
        self.grid[ci][cj].knock_down(dir)
        self.grid[ni][nj].knock_down(opposite_direction(dir))
        if self.grid[ni][nj].north_wall:
          wall_stack.append((NORTH, (ni, nj)))
        if self.grid[ni][nj].east_wall:
          wall_stack.append((EAST, (ni, nj)))
        if self.grid[ni][nj].south_wall:
          wall_stack.append((SOUTH, (ni, nj)))
        if self.grid[ni][nj].west_wall:
          wall_stack.append((WEST, (ni, nj)))
        visited[(ni, nj)] = True
        self.modified = [(ci, cj), (ni, nj)]
        yield True
    yield False

  def generate(self):
    """Return a generator object to be used for the maze generation.

    """
    if self.algorithm == DEPTH_FIRST:
      return self.generate_depth_first()
    elif self.algorithm == RANDOMIZED_PRIM:
      return self.generate_randomized_prim()

  def __getitem__(self, coord):
    """Return the cell addressed by the given coordinates.

    """
    (i, j) = coord
    return self.grid[i][j]

  def __str__(self):
    """Return rows * colums characters separated by a new line. Each character
    is the representation of the state of a cell.

    """
    repr = ''
    for (i, row) in enumerate(self.grid):
      if i != 0:
        repr += '\n'
      repr += ''.join(map(str, row))
    return repr
