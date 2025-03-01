
import pygame
from pygame.locals import *

# the following line is not needed if pgu is installed
import sys; sys.path.insert(0, "..")

from pgu import gui

app = gui.App()

e = gui.Button("Hello World")

app.connect(gui.QUIT, app.quit)
app.run(e)
