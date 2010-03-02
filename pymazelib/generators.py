#!/usr/bin/python

from random import randint
from random import shuffle

from maze import Maze
from maze import opposite_direction

"""Dictionary used to map an algorithm to its generator function.

"""
generators = {
              'Prim': lambda m: prim(m),
              'Recursive Backtracker': lambda m: recursive_backtracker(m),
             }

def prim(maze):
  """Pick up a random cell, mark it as visited, and add its walls inside a
  list of walls. Extract a random wall from the list: if the cell on the
  opposite has not been yet visited, knock down the wall, mark the the new cell
  as visited, and add its walls to the wall list. Repeat the process untill all
  the cells have been visited.

  """
  (rows, columns) = maze.size
  (i, j) = (randint(0, rows - 1), randint(0, columns - 1))
  maze[(i, j)].carved = True

  wall_stack = [(maze[(i, j)], dir) for dir in maze[(i, j)].intact_walls()]
  while wall_stack:
    i = randint(0, len(wall_stack) - 1)
    (cell, dir) = wall_stack.pop(i) 
    neighbor = cell.neighbors[dir]
    if neighbor and not neighbor.carved:
      cell.knock_down(dir)
      neighbor.knock_down(opposite_direction(dir))
      neighbor.carved = True
      wall_stack += \
          [(neighbor, dir) for dir in neighbor.intact_walls()]
      maze.modified = [cell.coords, neighbor.coords]
      yield True
  yield False

def recursive_backtracker(maze):
  """Pick up a a random cell and mark it as a visited. Then look for neighbors
  which have not been visited yet, knock down the walls in between and set the
  new cell as the current one. Add the old cell and the new one to the cell
  stack and repeat the steps by extracting a cell from the stack untill all the
  cells of the grid have been visited.

  """
  (rows, columns) = maze.size
  total = rows * columns

  (i, j) = (randint(0, rows - 1), randint(0, columns - 1))
  maze[(i, j)].carved = True
  carved = 1
  cell_stack = [maze[(i, j)]]
  while carved < total:
    cell = cell_stack.pop()
    neighborhood = cell.neighbors
    directions = range(len(neighborhood))
    shuffle(directions)
    for dir in directions:
      neighbor = neighborhood[dir]
      if neighbor and not neighbor.carved:
        cell.knock_down(dir)
        neighbor.knock_down(opposite_direction(dir))
        neighbor.carved = True
        carved += 1
        cell_stack.append(cell)
        cell_stack.append(neighbor)
        maze.modified = [cell.coords, neighbor.coords]
        yield True
        break
  yield False
