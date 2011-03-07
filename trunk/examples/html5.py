"""<title>an example of loading html from a file</title>"""
import pygame
from pygame.locals import *
import os

# the following line is not needed if pgu is installed
import sys; sys.path.insert(0, "..")

from pgu import gui
from pgu import html

app = gui.Desktop()

##check if the documentation has been built
##::
fname = "../docs/index.html"
if not os.path.isfile(fname):
    print('to run this demo, the documentation must be built')
    print('$ cd docs')
    print('$ python build.py')
##
else:

    ##open the file, hand it to a HTML object and display it
    ##::
    f = open(fname)
    text = "".join(f.readlines())
    f.close()
    
    doc = html.HTML(text,align=-1,valign=-1,width=800)
 
    view = gui.ScrollArea(doc,820,400)
    app.connect(gui.QUIT,app.quit,None)
    app.run(view)
    ##
    
