"""<title>Hello World</title>
The simplest possble gui app that can be made.
Unfortunately, you have to CTRL-C from the command line to quit it.
GUI will initialize the screen for you.
"""

import pygame
from pygame.locals import *

# the following line is not needed if pgu is installed
import sys; sys.path.insert(0, "..")

from pgu import gui

##::
app = gui.App()

e = gui.Button("Hello World")

app.connect(gui.QUIT, app.quit)

app.run(e)
##
