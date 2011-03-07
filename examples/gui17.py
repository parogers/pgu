"""an example a python console"""

import pygame
from pygame.locals import *

# the following line is not needed if pgu is installed
import sys; sys.path.insert(0, "..")

import traceback

from pgu import gui
from pgu import html

class StringStream:
    def __init__(self):
        self._data = ''
    def write(self,data):
        self._data = self._data+data
        _lines = self._data.split("\n")
        for line in _lines[:-1]:
            lines.tr()
            lines.td(gui.Label(str(line)),align=-1)
        self._data = _lines[-1:][0]
        
_locals = {}
def lkey(_event):
    e = _event
    if e.key == K_RETURN:
        _stdout = sys.stdout
        s = sys.stdout = StringStream()
        
        val = line.value
        line.value = ''
        line.focus()
        print('>>> '+val)
        try:
            code = compile(val,'<string>','single')
            eval(code,globals(),_locals)
        except: 
            e_type,e_value,e_traceback = sys.exc_info()
            print('Traceback (most recent call last):')
            traceback.print_tb(e_traceback,None,s)
            print(e_type,e_value)

        sys.stdout = _stdout

app = gui.Desktop()
t = gui.Table(width=500,height=400)

t.tr()
lines = gui.Table()
box = gui.ScrollArea(lines,500,380)
t.td(box)

t.tr()
line = gui.Input(size=49)
line.connect(gui.KEYDOWN,lkey)
t.td(line)

t.tr()
class Hack(gui.Spacer):
    def resize(self,width=None,height=None):
        box.set_vertical_scroll(65535)
        return 1,1
t.td(Hack(1,1))

app.connect(gui.QUIT,app.quit,None)
app.run(t)
