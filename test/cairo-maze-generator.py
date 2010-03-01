#!/usr/bin/python

from __future__ import division
import sys
import os

import gobject
import gtk
from gtk import gdk
import cairo

from pymazelib.maze import Maze
from pymazelib.generators import generators
from pymazelib.solvers import solvers

GUI_CONF = os.path.join(os.path.dirname(__file__), 'cairo-maze-generator.xml')

def combobox_init(combobox, items):
  model = gtk.ListStore(str)
  for i in items:
      model.append([i])
  combobox.set_model(model)
  cell = gtk.CellRendererText()
  combobox.pack_start(cell, True)
  combobox.add_attribute(cell, 'text', 0)
  combobox.set_active(0)

def create_grid_and_delta(width, height, rows, columns):
  """XXX

  """
  delta = min(width, height) // max(rows, columns)
  startx = (width - delta * columns) // 2
  starty = (height - delta * rows) // 2
  grid = []
  for y in xrange(starty, starty + delta * rows + 1, delta):
    row = []
    for x in xrange(startx, startx + delta * columns + 1, delta):
      row.append((x, y))
    grid.append(row)
  return (grid, delta)

class Gui(object):
  def __init__(self):
    """The gui consists of a serie of controls to choose the number of rows,
    the number of columns, and the generating algorithm, a drawing area used to
    show the progress of the maze generation, and a couple of buttons used to
    clear the current maze, and to start the generating process.

    """
    builder = gtk.Builder()
    builder.add_from_file(GUI_CONF)
    builder.connect_signals(self)

    self.window = builder.get_object('window')
    self._rows = builder.get_object('rows')
    self._columns = builder.get_object('columns')
    self._generators = builder.get_object('generators')
    self._solvers = builder.get_object('solvers')
    self._generate = builder.get_object('generate')
    self._solve = builder.get_object('solve')
    self._show_evoltuion = builder.get_object('show_evolution')
    self.widgets = [self._rows, self._columns, self._generators,
                    self._solvers, self._generate]

    combobox_init(self._generators, generators.keys())
    combobox_init(self._solvers, solvers.keys())

    self.maze = Maze(self.rows, self.columns)

  def delete_cb(self, widget, event):
    """Quit the gtk main loop.

    """
    gtk.main_quit()

  def value_changed_cb(self, widget):
    """Create a new maze, update the grid and then redraw the scene.

    """
    (width, height) = self.darea_size
    self.maze = Maze(self.rows, self.columns)
    (self.grid, self.delta) = \
        create_grid_and_delta(width, height, self.rows, self.columns)
    self.draw_maze(self.cr)

  def configure_cb(self, widget, event):
    """Each time the drawing area is reconfigured, we store a grid used to map
    the cells of the maze into the device space. We need also to inizialize a
    cairo surface which will be used for all the drawing actions.

    """
    (_, _, width, height) = widget.get_allocation()
    self.darea_size = (width, height)

    self.surface = cairo.ImageSurface(cairo.FORMAT_ARGB32, width, height)
    self.cr = cairo.Context(self.surface)

    (self.grid, self.delta) = \
        create_grid_and_delta(width, height, self.rows, self.columns)
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

  def generate_clicked_cb(self, button):
    """Start the maze generator process.

    """
    self.maze = Maze(self.rows, self.columns)
    self.draw_maze(self.cr)
    process_fun = self.process(generators[self.generator](self.maze))
    gobject.idle_add(process_fun.next)

  def solve_clicked_cb(self, button):
    """Start the maze solver process.

    """
    process_fun = self.process(solvers[self.solver](self.maze))
    gobject.idle_add(process_fun.next)

  def process(self, maze_gen):
    """Wrapper of the maze generator/solver functions.
    Each time a new step is done, we redraw the involved cells.
    All the widgets are disabled durint the process.

    """
    for item in self.widgets:
      item.set_sensitive(False)

    while maze_gen.next():
      if self._show_evoltuion.get_active():
        self.draw_modified(self.cr)
      yield True
    if not self._show_evoltuion.get_active():
      self.draw_maze(self.cr)

    for item in self.widgets:
      item.set_sensitive(True)

    yield False

  def draw_line(self, cr, x1, y1, x2, y2):
    """Draw a straight line connecting the given coordinates.

    """
    cr.move_to(x1, y1)
    cr.line_to(x2, y2)
    cr.stroke()

  def draw_cell(self, cr, i, j):
    """Draw a cell of the maze depending on the kind of cell (start point, end
    point..) and its walls.

    """
    cell = self.maze[(i, j)]
    delta = self.delta
    (x, y) = self.grid[i][j]
    if cell.start: cr.set_source_rgb(1, 0, 0)
    elif cell.end: cr.set_source_rgb(0, 1, 0)
    else: cr.set_source_rgb(1, 1, 1)
    cr.rectangle(x, y, delta, delta)
    cr.fill()

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
    (width, height) = self.darea_size
    self.cr.set_source_rgb(1, 1, 1)
    self.cr.rectangle(0, 0, width, height)
    self.cr.fill()

    (rows, columns) = self.maze.size
    for i in xrange(rows):
      for j in xrange(columns):
        self.draw_cell(cr, i, j)
    self.window.queue_draw()

  def draw_modified(self, cr):
    """Wrapper which invoke the draw_cell on each modified cell.

    """
    while self.maze.modified:
      (i, j) = self.maze.modified.pop()
      self.draw_cell(cr, i, j)
    self.window.queue_draw()

  def mainloop(self):
    """Wrapper to gtk mainloop.

    """
    gtk.main()

  @property
  def rows(self):
    """Return the value of the spinbutton controlling the number of rows.

    """
    return self._rows.get_value_as_int()

  @property
  def columns(self):
    """Return the value of the spinbutton controlling the number of columns.

    """
    return self._columns.get_value_as_int()

  @property
  def generator(self):
    """Return the active text of the combobox controlling the generator
    algorithm.

    """
    return self._generators.get_active_text()

  @property
  def solver(self):
    """Return the active text of the combobox controlling the solver
    algorithm.

    """
    return self._solvers.get_active_text()

def main(argv):
  Gui().mainloop()

if __name__ == '__main__':
  sys.exit(main(sys.argv))
