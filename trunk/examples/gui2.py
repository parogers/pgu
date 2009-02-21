"""<title>Connections</title>
Same as the first -- but now you can click on the close window button
in your windowing system to close out the example.
"""

import pygame
from pygame.locals import *

# the following line is not needed if pgu is installed
import sys; sys.path.insert(0, "..")

from pgu import gui

app = gui.App()
##The gui.QUIT event is connected to the app.close method.
##::
app.connect(gui.QUIT,app.quit,None)
##

e = gui.Button("This is a really long button.")

app.run(e)


