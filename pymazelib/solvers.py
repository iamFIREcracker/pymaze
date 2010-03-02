#!/usr/bin/python

from random import randint
from random import shuffle

from maze import Maze
from maze import opposite_direction

"""Dictionary used to map an algorithm to its generator function.

"""
solvers = {
           'Depth First': lambda m: depth_first(m),
          }

def depth_first(maze):
  """Pick up a a random cell and mark it as a visited. Then look for open
  directions, choose one randomly, and add the current cell together with the
  neighbor one to cell stack. Pop a cell from the stack and repeat the steps
  untill the end cell is found.

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
