#!/usr/bin/python

from random import randint
from random import shuffle

from maze import Maze
from maze import opposite_direction
from maze import beyond_wall

"""Dictionary used to map an algorithm to its generator function.
   List of accepted keys:
     depth-first
     randomized-prism

"""
generators = {'depth-first': lambda m: generate_depth_first(m),
              'randomized-prim': lambda m: generate_randomized_prim(m)}

def generate_depth_first(maze):
  """Generate the maze by using the depth-first algorithm.
  Basically with start at a random cell and we mark it as a visited. Then we
  look for neighbors which have not been visited yet, knock down the walls in
  between and change our current cell with the new one. We repeat these steps
  untill all the cells of the grid have been visited.  The function yields
  True if there is something else to do, False otherwise.

  """
  visited = {}
  (rows, columns) = maze.size
  (i, j) = (randint(0, rows - 1), randint(0, columns - 1))
  visited[(i, j)] = True

  total = rows * columns
  cell_stack = [(i, j)]
  while len(visited) < total:
    (ci, cj) = cell_stack.pop()
    neighborhood = maze.neighbors(ci, cj)
    shuffle(neighborhood)
    for (dir, (ni, nj)) in neighborhood:
      if (ni, nj) not in visited:
        maze[(ci, cj)].knock_down(dir)
        maze[(ni, nj)].knock_down(opposite_direction(dir))
        cell_stack.append((ci, cj))
        cell_stack.append((ni, nj))
        visited[(ni, nj)] = True
        maze.modified = [(ci, cj), (ni, nj)]
        yield True
        break
  yield False

def generate_randomized_prim(maze):
  """Generate the maze by using the randomized prim's algorithm.
  XXX

  """
  visited = {}
  (rows, columns) = maze.size
  (i, j) = (randint(0, rows - 1), randint(0, columns - 1))
  visited[(i, j)] = True

  wall_stack = map(lambda d: (d, (i, j)), maze.walls(i, j))
  while wall_stack:
    i = randint(0, len(wall_stack) - 1)
    (dir, (ci, cj)) = wall_stack.pop(i) 
    (ni, nj) = beyond_wall(ci, cj, dir, rows, columns)
    if ni is not None and nj is not None and (ni, nj) not in visited:
      maze[(ci, cj)].knock_down(dir)
      maze[(ni, nj)].knock_down(opposite_direction(dir))
      for dir in maze.walls(ni, nj):
        wall_stack.append((dir, (ni, nj)))
      visited[(ni, nj)] = True
      maze.modified = [(ci, cj), (ni, nj)]
      yield True
  yield False
