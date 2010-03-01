#!/usr/bin/python

from random import randint
from random import shuffle

from maze import Maze
from maze import opposite_direction
from maze import beyond_wall

"""Dictionary used to map an algorithm to its generator function.

"""
generators = {
              'Prim': lambda m: prim(m),
              'Recursive Backtracker': lambda m: recursive_backtracker(m),
             }

def recursive_backtracker(maze):
  """Pick up a a random cell and mark it as a visited. Then look for neighbors
  which have not been visited yet, knock down the walls in between and set the
  new cell as the current one. Repeat these steps untill all the cells of the
  grid have been visited.

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

def prim(maze):
  """Pick up a random cell, mark it as visited, and add its walls inside a
  list of walls. Extract a random wall from the list: if the cell on the
  opposite has not been yet visited, knock down the wall, mark the the new cell
  as visited, and add its walls to the wall list. Repeat the process untill all
  the cells have been visited.

  """
  visited = {}
  (rows, columns) = maze.size
  (i, j) = (randint(0, rows - 1), randint(0, columns - 1))
  visited[(i, j)] = True

  wall_stack = map(lambda d: (d, (i, j)), maze[(i, j)].walls)
  while wall_stack:
    i = randint(0, len(wall_stack) - 1)
    (dir, (ci, cj)) = wall_stack.pop(i) 
    (ni, nj) = beyond_wall(ci, cj, dir, rows, columns)
    if ni is not None and nj is not None and (ni, nj) not in visited:
      maze[(ci, cj)].knock_down(dir)
      maze[(ni, nj)].knock_down(opposite_direction(dir))
      for dir in maze[(ni, nj)].walls:
        wall_stack.append((dir, (ni, nj)))
      visited[(ni, nj)] = True
      maze.modified = [(ci, cj), (ni, nj)]
      yield True
  yield False
