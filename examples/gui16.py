"""and example of how to implement tabs"""

import pygame
from pygame.locals import *

# the following line is not needed if pgu is installed
import sys; sys.path.insert(0, "..")

from pgu import gui
from pgu import html

app = gui.Desktop()

#####################################
c = gui.Container(width=240,height=120)

def i_disable(value):
    item.disabled = True
    item.blur()
    item.chsize()

item = gui.Button(gui.Label('Disable'))
item.connect(gui.CLICK,i_disable,None)

def c_add(value):
    w = value
    c.add(item,120,45)
    w.value = gui.Label('Remove')
    w.connect(gui.CLICK,c_remove,w)
    
def c_remove(value):
    w = value
    c.remove(item)
    w.value = gui.Label('Add')
    w.connect(gui.CLICK,c_add,w)


w = gui.Button("Add")
w.connect(gui.CLICK,c_add,w)
c.add(w,10,45)

#################################
t = gui.Table(width=240,height=120)

tn = 0
tw = []
def t_add(value):
    global tn
    if (tn%6)==0: t.tr()
    w = gui.Label(str(tn))
    tw.append(w)
    t.td(w)
    tn+=1
    
def t_remove(value):
    if len(tw):
        w = tw.pop()
        t.remove(w)

t.tr()
w = gui.Button('Add')
w.connect(gui.CLICK,t_add,None)
t.td(w,colspan=3)

w = gui.Button('Remove')
w.connect(gui.CLICK,t_remove,None)
t.td(w,colspan=3)

#####################################
d = gui.Document(width=240,height=120)

dn = 0
dw = []
def d_add(value):
    global dn
    w = gui.Label("%d "%dn)
    dw.append(w)
    d.add(w)
    dn+=1
    
def d_remove(value):
    if len(dw):
        w = dw.pop()
        d.remove(w)

w = gui.Button('Add')
w.connect(gui.CLICK,d_add,None)
d.add(w)
d.space((8,8))

w = gui.Button('Remove')
w.connect(gui.CLICK,d_remove,None)
d.add(w)
d.space((8,8))
#######################################

def tab():
    box.widget = g.value
    

g = gui.Group()
g.connect(gui.CHANGE,tab)

tt = gui.Table()
tt.tr()

b = gui.Tool(g,gui.Label("Container"),c)
tt.td(b)
b = gui.Tool(g,gui.Label("Table"),t)
tt.td(b)
b = gui.Tool(g,gui.Label("Document"),d)
tt.td(b)

tt.tr()
spacer = gui.Spacer(240,120)
box = gui.ScrollArea(spacer,height=120)
tt.td(box,style={'border':1},colspan=3)

app.connect(gui.QUIT,app.quit,None)
app.run(tt)
