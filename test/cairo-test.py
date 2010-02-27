#!/usr/bin/python

import sys

import gobject
import gtk
from gtk import gdk
import cairo

from pymazelib.maze import Maze
from pymazelib.maze import DEPTH_FIRST
from pymazelib.maze import NORTH
from pymazelib.maze import EAST
from pymazelib.maze import SOUTH
from pymazelib.maze import WEST

(CLEAR, START) = xrange(2)

class Window(gtk.Window):
  def __init__(self, rows, columns):
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

    self.maze = Maze(rows, columns)

  def configure_cb(self, widget, event):
    (_, _, width, height) = widget.get_allocation()
    self.darea_size = (width, height)
    self.surface = cairo.ImageSurface(cairo.FORMAT_ARGB32,
                                      width, height)
    self.cr = cairo.Context(self.surface)
    self.draw(self.cr)
    return True

  def expose_cb(self, widget, event):
    cr = widget.window.cairo_create()
    cr.rectangle(event.area.x, event.area.y,
                 event.area.width, event.area.height)
    cr.clip()
    cr.set_source_surface(self.surface, 0, 0)
    cr.paint()
    return False

  def clicked_cb(self, button, kind):
    if kind == CLEAR:
      (rows, columns) = self.maze.size
      self.maze = Maze(rows, columns)
      self.draw(self.cr)
    elif kind == START:
      gen_fun = self.generate(self.maze.generate(DEPTH_FIRST))
      gobject.idle_add(gen_fun.next)

  def generate(self, gen_fun):
    while gen_fun.next():
      self.draw(self.cr)
      yield True
    yield False

  def draw_line(self, cr, x1, y1, x2, y2):
    cr.move_to(x1, y1)
    cr.line_to(x2, y2)
    cr.stroke()

  def draw(self, cr):
    (width, height) = self.darea_size

    # blank the scene
    cr.rectangle(0, 0, width, height)
    cr.set_source_rgb(1, 1, 1)
    cr.fill()

    # draw the maze
    cr.set_source_rgb(0, 0, 0)
    (rows, columns) = self.maze.size
    wallsize = min(width, height) // max(rows, columns)
    starty = (height - wallsize * rows) / 2
    for i in xrange(rows):
      if i == 0: y = (height - wallsize * rows) / 2
      else: y += wallsize
      for j in xrange(columns):
        if j == 0: x = (width - wallsize * columns) / 2
        else: x += wallsize
        walls = self.maze[(i, j)].walls
        if walls - NORTH >= 0:
          self.draw_line(cr, x, y, x + wallsize, y)
          walls -= NORTH
        if walls - EAST >= 0:
          self.draw_line(cr, x + wallsize, y, x + wallsize, y + wallsize)
          walls -= EAST
        if walls - SOUTH >= 0:
          self.draw_line(cr, x + wallsize, y + wallsize, x, y + wallsize)
          walls -= SOUTH
        if walls - WEST >= 0:
          self.draw_line(cr, x, y + wallsize, x, y)
          walls -= WEST

    self.queue_draw()

  def mainloop(self):
    self.show_all()
    gtk.main()

def main(argv):
  if len(argv) != 3:
    print "Usage: %s <rows> <columns>" % argv[0]
    return 1
  (rows, columns) = map(int, argv[1:3])
  Window(rows, columns).mainloop()

if __name__ == '__main__':
  sys.exit(main(sys.argv))
