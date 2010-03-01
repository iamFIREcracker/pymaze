#!/usr/bin/python

# directions
NORTH = 8
EAST = 4
SOUTH = 2
WEST = 1

# how to represent a cell depending on its walls.
CELL = '0123456789abcdef'

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

  @property
  def directions(self):
    """Return an array containing the open directions of the current cell.

    """
    direction_list = []
    if self.north_wall:
      direction_list.append(NORTH)
    if self.east_wall:
      direction_list.append(EAST)
    if self.south_wall:
      direction_list.append(SOUTH)
    if self.west_wall:
      direction_list.append(WEST)
    return direction_list

  @property
  def walls(self):
    """Return an array containing the directions to the walls which have not
    been knocked down.

    """
    wall_list = []
    if self.north_wall:
      wall_list.append(NORTH)
    if self.east_wall:
      wall_list.append(EAST)
    if self.south_wall:
      wall_list.append(SOUTH)
    if self.west_wall:
      wall_list.append(WEST)
    return wall_list

  def __str__(self):
    """Return a character representing the state of the cell. The state is
    given by the walls which have not been knocked down.

    """
    i = int(self.north_wall) * NORTH + int(self.east_wall) * EAST + \
        int(self.south_wall) * SOUTH + int(self.west_wall) * WEST
    return CELL[i]

class Maze(object):
  def __init__(self, rows, columns):
    """Create an empty maze of the given dimensions.

    """
    self.size = (rows, columns)
    self.grid = [[Cell() for j in xrange(columns)] for i in xrange(rows)]
    self.modified = []

  def neighbors(self, i, j):
    """Return an array containing the neighbors of the given cell and the
    direction from the current cell. The neighbors are searched clockwise
    direction, starting from north.

    """
    (rows, columns) = self.size
    neighborhood = []
    if (i > 0): neighborhood.append((NORTH, (i - 1, j)))
    if (j < columns - 1): neighborhood.append((EAST, (i, j + 1)))
    if (i < rows - 1): neighborhood.append((SOUTH, (i + 1, j)))
    if (j > 0): neighborhood.append((WEST, (i, j - 1)))
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
