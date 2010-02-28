#!/usr/bin/python

from __future__ import division
import sys

import gobject
import gtk
from gtk import gdk
import cairo

from pymazelib.maze import Maze
from pymazelib.maze import algorithms
from pymazelib.maze import NORTH
from pymazelib.maze import EAST
from pymazelib.maze import SOUTH
from pymazelib.maze import WEST

# enumerate used for the buttons 'clicked' callbacks
(CLEAR, START) = xrange(2)

class Window(gtk.Window):
  def __init__(self, rows, columns, algorithm):
    """The gui consists of a drawing area used to show the progress of the maze
    generation, and a couple of buttons used to clear the current maze, and to
    start the generating process.

    """
    super(Window, self).__init__()
    self.connect('destroy', gtk.main_quit)
    self.resize(200, 200)
    vbox = gtk.VBox()
    darea = gtk.DrawingArea()
    darea.connect('configure-event', self.configure_cb)
    darea.connect('expose-event', self.expose_cb)
    vbox.pack_start(darea)
    hbox = gtk.HBox()
    clear = gtk.Button('Clear')
    clear.connect('clicked', self.clicked_cb, CLEAR)
    hbox.pack_start(clear, False, False)
    start = gtk.Button('Start')
    start.connect('clicked', self.clicked_cb, START)
    hbox.pack_end(start, False, False)
    vbox.pack_end(hbox, False, False)
    self.add(vbox)

    self.maze = Maze(rows, columns, algorithm)

  def configure_cb(self, widget, event):
    """Each time the drawing area is reconfigured, we store a grid used to map
    the cells of the maze into the device space. We need also to inizialize a
    cairo surface which will be used for all the drawing actions.

    """
    (_, _, width, height) = widget.get_allocation()
    self.darea_size = (width, height)
    # create a grid of pixels
    (rows, columns) = self.maze.size
    delta = min(width, height) // max(rows, columns)
    startx = (width - delta * columns) // 2
    starty = (height - delta * rows) // 2
    grid = []
    for y in xrange(starty, starty + delta * rows + 1, delta):
      row = []
      for x in xrange(startx, startx + delta * columns + 1, delta):
        row.append((x, y))
      grid.append(row)
    self.delta = delta
    self.grid = grid
    # create the cairo surface ..
    self.surface = cairo.ImageSurface(cairo.FORMAT_ARGB32, width, height)
    self.cr = cairo.Context(self.surface)
    # .. and blank it
    self.cr.set_source_rgb(1, 1, 1)
    self.cr.rectangle(0, 0, width, height)
    self.cr.fill()
    # draw the maze
    self.draw_maze(self.cr)

    return True

  def expose_cb(self, widget, event):
    """Paint the internal cairo surface, over the exposed area.

    """
    cr = widget.window.cairo_create()
    cr.rectangle(event.area.x, event.area.y,
                 event.area.width, event.area.height)
    cr.clip()
    cr.set_source_surface(self.surface, 0, 0)
    cr.paint()
    return False

  def clicked_cb(self, button, kind):
    """Depending on the flag passed to the callback, we are going to clear the
    current maze or start the generating process.

    """
    if kind == CLEAR:
      (rows, columns) = self.maze.size
      algorithm = self.maze.algorithm
      self.maze = Maze(rows, columns, algorithm)
      self.draw_maze(self.cr)
    elif kind == START:
      gen_fun = self.generate(self.maze.generate())
      gobject.idle_add(gen_fun.next)

  def generate(self, maze_gen):
    """Wrapper of the maze generator function.
    Each time the maze steps forward, we redraw the involved cells.

    """
    while maze_gen.next():
      self.draw_modified(self.cr)
      yield True
    yield False

  def draw_line(self, cr, x1, y1, x2, y2):
    """Draw a straight line connecting the given coordinates.

    """
    cr.move_to(x1, y1)
    cr.line_to(x2, y2)
    cr.stroke()

  def draw_cell(self, cr, i, j):
    """Blank the background of the cell, and then draw the walls depending on
    their state.

    """
    delta = self.delta
    (x, y) = self.grid[i][j]
    cr.set_source_rgb(1, 1, 1)
    cr.rectangle(x, y, delta, delta)
    cr.fill()

    cell = self.maze[(i, j)]
    cr.set_source_rgb(0, 0, 0)
    if cell.north_wall:
      self.draw_line(cr, x, y, x + delta, y)
    if cell.east_wall:
      self.draw_line(cr, x + delta, y, x + delta, y + delta)
    if cell.south_wall:
      self.draw_line(cr, x + delta, y + delta, x, y + delta)
    if cell.west_wall:
      self.draw_line(cr, x, y + delta, x, y)

  def draw_maze(self, cr):
    """Wrapper which invoke the draw_cell on each cell of the maze.

    """
    (rows, columns) = self.maze.size
    for i in xrange(rows):
      for j in xrange(columns):
        self.draw_cell(cr, i, j)
    self.queue_draw()

  def draw_modified(self, cr):
    """Wrapper which invoke the draw_cell on each modified cell.

    """
    while self.maze.modified:
      (i, j) = self.maze.modified.pop()
      self.draw_cell(cr, i, j)
    self.queue_draw()

  def mainloop(self):
    """Wrapper to gtk mainloop.

    """
    self.show_all()
    gtk.main()

def main(argv):
  if len(argv) != 4:
    print "Usage: %s <rows> <columns> <algorithm>" % argv[0]
    return 1
  (rows, columns) = map(int, argv[1:3])
  Window(rows, columns, algorithms[argv[3]]).mainloop()

if __name__ == '__main__':
  sys.exit(main(sys.argv))
