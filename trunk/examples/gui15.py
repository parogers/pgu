"""an example of fancy event handling, ProgressBars, etc"""

import pygame
from pygame.locals import *

# the following line is not needed if pgu is installed
import sys; sys.path.insert(0, "..")

from pgu import gui
from pgu import html

app = gui.Desktop()

c = gui.Container(width=440,height=420)

c.add(gui.Label("Click on Cuzco's Face!"),0,0)

img = gui.Image("cuzco.png")

def myfnc(_event,_widget,_code,a,b,c):
    print(_event,_widget,_code,a,b,c)
    pos = _event.pos
    img.value.fill((255,0,0),(pos[0],pos[1],2,2))
    img.repaint()
    t.tr()
    t.td(gui.Label(str(("point at ",pos))))
    prog.value += 1
    #box.resize()
    #box.set_vertical_scroll()

img.connect(gui.CLICK,myfnc,1,2,3)

c.add(img,20,20)

t = gui.Table()
box = gui.ScrollArea(t,300,240)
c.add(box,10,120)


            

prog = gui.ProgressBar(10,0,40,width=200)
c.add(prog,50,400)

app.connect(gui.QUIT,app.quit,None)
app.run(c)
