"""<title>Custom Actions</title>"""
import pygame
from pygame.locals import *

# the following line is not needed if pgu is installed
import sys; sys.path.insert(0, "..")

from pgu import gui

class ColorDialog(gui.Dialog):
    def __init__(self,value,**params):
        self.value = list(gui.parse_color(value))
        
        title = gui.Label("Color Picker")
        
        main = gui.Table()
        
        main.tr()
        
        self.color = gui.Color(self.value,width=64,height=64)
        main.td(self.color,rowspan=3,colspan=1)
        
        ##The sliders CHANGE events are connected to the adjust method.  The 
        ##adjust method updates the proper color component based on the value
        ##passed to the method.
        ##::
        main.td(gui.Label(' Red: '),1,0)
        e = gui.HSlider(value=self.value[0],min=0,max=255,size=32,width=128,height=16)
        e.connect(gui.CHANGE,self.adjust,(0,e))
        main.td(e,2,0)
        ##

        main.td(gui.Label(' Green: '),1,1)
        e = gui.HSlider(value=self.value[1],min=0,max=255,size=32,width=128,height=16)
        e.connect(gui.CHANGE,self.adjust,(1,e))
        main.td(e,2,1)

        main.td(gui.Label(' Blue: '),1,2)
        e = gui.HSlider(value=self.value[2],min=0,max=255,size=32,width=128,height=16)
        e.connect(gui.CHANGE,self.adjust,(2,e))
        main.td(e,2,2)
                        
        gui.Dialog.__init__(self,title,main)
        
    ##The custom adjust handler.
    ##::
    def adjust(self,value):
        (num, slider) = value
        self.value[num] = slider.value
        self.color.repaint()
        self.send(gui.CHANGE)
    ##

if __name__ == '__main__':
    app = gui.Desktop()
    app.connect(gui.QUIT,app.quit,None)
    
    c = gui.Table(width=640,height=480)
    
    dialog = ColorDialog("#00ffff")
            
    e = gui.Button("Color")
    e.connect(gui.CLICK,dialog.open,None)
    c.tr()
    c.td(e)
    
    app.run(c)

