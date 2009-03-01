"""an example of add, remove for several container types"""

#this example contains a bit of a HACK
#when something is added/removed, chsize() may need to be called
#to ensure proper refresh of the screen, etc
#this may be fixed in the future, but for now, chsize must be called
#by hand

import pygame
from pygame.locals import *

# the following line is not needed if pgu is installed
import sys; sys.path.insert(0, "..")

from pgu import gui
from pgu import html

app = gui.Desktop()

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
    # Note - we need to disconnect the old signal handler first
    w.disconnect(gui.CLICK)
    w.connect(gui.CLICK,c_remove,w)
    
def c_remove(value):
    w = value
    c.remove(item)
    w.value = gui.Label('Add')
    # Note - we need to disconnect the old signal handler first
    w.disconnect(gui.CLICK)
    w.connect(gui.CLICK,c_add,w)


w = gui.Button("Add")
w.connect(gui.CLICK,c_add,w)
c.add(w,10,45)


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


tt = gui.Table()
tt.tr()
tt.td(gui.Label("Container"))
tt.tr()
tt.td(c,style={'border':1})

tt.tr()
tt.td(gui.Label("Table"))
tt.tr()
tt.td(t,style={'border':1})

tt.tr()
tt.td(gui.Label("Document"))
tt.tr()
tt.td(d,style={'border':1})

app.connect(gui.QUIT,app.quit,None)
app.run(tt)
