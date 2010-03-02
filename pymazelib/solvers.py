#!/usr/bin/python

from random import randint
from random import shuffle

from maze import Maze
from maze import NORTH
from maze import EAST
from maze import SOUTH
from maze import WEST
from maze import DIRECTIONS
from maze import opposite_direction

"""Dictionary used to map an algorithm to its generator function.

"""
solvers = {
           'Depth First': lambda m: depth_first(m),
           'Wall Follower': lambda m: wall_follower(m),
          }

def depth_first(maze):
  """Pick up the start cell and then look for open directions, choose one
  randomly, and add the current cell together with the neighbor one to a cell
  stack. Then pop a cell from the stack and repeat the steps untill the end
  cell is found.

  """
  cell_stack = [maze[(0, 0)]]
  while True:
    cell = cell_stack.pop()
    if cell.end:
      break
    directions = cell.open_directions()
    shuffle(directions)
    for dir in directions:
      neighbor = cell.neighbors[dir]
      neighbor.active = True
      cell.directions[dir] = False
      neighbor.directions[opposite_direction(dir)] = False
      cell_stack.append(cell)
      cell_stack.append(neighbor)
      maze.modified = [neighbor.coords]
      break
    else:
      cell.active = False
      cell.backward = True
      maze.modified = [cell.coords]
    yield True
  yield False

def wall_follower(maze):
  """Each time we have a pool of possible directions, we start by analysing the
  one of the left of current one.

  """
  cell_stack = [(maze[(0, 0)], EAST)]
  while True:
    (cell, curr_dir) = cell_stack.pop()
    if cell.end:
      break
    curr_dir = (curr_dir - 1) # let's consider first our left
    for dir in xrange(curr_dir, curr_dir + DIRECTIONS):
      dir = (dir % DIRECTIONS)
      if cell.directions[dir]:
        neighbor = cell.neighbors[dir]
        neighbor.active = True
        cell.directions[dir] = False
        neighbor.directions[opposite_direction(dir)] = False
        cell_stack.append((cell, curr_dir))
        cell_stack.append((neighbor, dir))
        maze.modified = [neighbor.coords]
        break
    else:
      cell.active = False
      cell.backward = True
      maze.modified = [cell.coords]
    yield True
  yield False

