#!/usr/bin/python

from random import randint
from random import shuffle

from maze import Maze
from maze import NORTH
from maze import opposite_direction
from maze import beyond_wall

"""Dictionary used to map an algorithm to its generator function.

"""
solvers = {
           'Always Turn Left': lambda m: always_turn_right(m),
          }

def always_turn_left(maze):
  yield False
