"""an example of chsize"""
import pygame
from pygame.locals import *

# the following line is not needed if pgu is installed
import sys; sys.path.insert(0, "..")

from pgu import gui
from pgu import html

app = gui.Desktop()

c = gui.Table(width=500,height=500)
c.tr()

dw = 400
data = """
<div style='margin: 8px; padding: 8px; border: 1px; border-color: #88ffff; background: #eeffff;'><img src='cuzco.png' align=right>cuzco is my goat. cuzco is my goat. cuzco is my goat. cuzco is my goat. cuzco is my goat. cuzco is my goat. cuzco is my goat. cuzco is my goat. cuzco is my goat. cuzco is my goat. cuzco is my goat. cuzco is my goat. cuzco is my goat. cuzco is my goat. </div>"""
doc = html.HTML(data,width=dw)
c.td(doc)

c.tr()
s = gui.HSlider(300,200,450,100,width=dw)
def mychange(value):
    s,doc = value
    doc.style.width = s.value
    doc.chsize()
s.connect(gui.CHANGE,mychange,(s,doc))
c.td(s)

app.connect(gui.QUIT,app.quit,None)
app.run(c)
