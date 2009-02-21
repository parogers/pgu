"""<title>Containers and more Connections</title>
A container is added, and centered a button within that
container.
"""
import pygame
from pygame.locals import *

# the following line is not needed if pgu is installed
import sys; sys.path.insert(0, "..")

from pgu import gui

##Using Desktop instead of App provides the GUI with a background.
##::
app = gui.Desktop()
app.connect(gui.QUIT,app.quit,None)
##

##The container is a table
##::
c = gui.Table(width=200,height=120)
##

##The button CLICK event is connected to the app.close method.  The button will fill the whole table cell.
##::
e = gui.Button("Quit")
e.connect(gui.CLICK,app.quit,None)
c.add(e,0,0)
##

app.run(c)
