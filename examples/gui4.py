"""<title>Custom Widgets</title>
Same functionality as gui3, however gui.Button is subclassed.  The
subclassed version is a fully featured Quit button.
"""
import pygame
from pygame.locals import *

# the following line is not needed if pgu is installed
import sys; sys.path.insert(0, "..")

from pgu import gui

app = gui.Desktop()
app.connect(gui.QUIT,app.quit,None)

c = gui.Table(width=200,height=120)

##::
class Quit(gui.Button):
    def __init__(self,**params):
        params['value'] = 'Quit'
        gui.Button.__init__(self,**params)
        self.connect(gui.CLICK,app.quit,None)
##

##Adding the button to the container.  By using the td method to add it, the button
##is placed in a sub-container, and it will not have to fill the whole cell.
##::
c.tr()
e = Quit()
c.td(e)
##

app.run(c)
