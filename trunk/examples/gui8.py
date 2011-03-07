"""<title>Forms</title>"""
import pygame
from pygame.locals import *

# the following line is not needed if pgu is installed
import sys; sys.path.insert(0, "..")

from pgu import gui

from gui7 import ColorDialog

class NewDialog(gui.Dialog):
    def __init__(self,**params):
        title = gui.Label("New Picture...")
        
        ##Once a form is created, all the widgets that are added with a name
        ##are added to that form.
        ##::
        self.value = gui.Form()
        
        t = gui.Table()
        
        t.tr()
        t.td(gui.Label("Size"),align=0,colspan=2)
        
        tt = gui.Table()
        tt.tr()
        tt.td(gui.Label("Width: "),align=1)
        tt.td(gui.Input(name="width",value=256,size=4))
        tt.tr()
        tt.td(gui.Label("Height: "),align=1)
        tt.td(gui.Input(name="height",value=256,size=4))
        t.tr()
        t.td(tt,colspan=2)
        ##
        
        t.tr()
        t.td(gui.Spacer(width=8,height=8))
        t.tr()
        t.td(gui.Label("Format",align=0))
        t.td(gui.Label("Background",align=0))

        t.tr()        
        g = gui.Group(name="format",value="rgb")
        tt = gui.Table()
        tt.tr()
        tt.td(gui.Radio(g,value="rgb"))
        tt.td(gui.Label(" RGB"),align=-1)
        tt.tr()
        tt.td(gui.Radio(g,value="bw"))
        tt.td(gui.Label(" Grayscale"),align=-1)
        t.td(tt,colspan=1)
        
        g = gui.Group(name="color",value="#ffffff")
        tt = gui.Table()
        tt.tr()
        tt.td(gui.Radio(g,value="#000000"))
        tt.td(gui.Label(" Black"),align=-1)
        tt.tr()
        tt.td(gui.Radio(g,value="#ffffff"))
        tt.td(gui.Label(" White"),align=-1)
        tt.tr()
        
        default = "#ffffff"
        radio = gui.Radio(g,value="custom")
        color = gui.Color(default,width=40,height=16,name="custom")
        picker = ColorDialog(default)
        
        color.connect(gui.CLICK,gui.action_open,{'container':t,'window':picker})
        picker.connect(gui.CHANGE,gui.action_setvalue,(picker,color))

        tt.td(radio)
        tt.td(color)
        
        t.td(tt,colspan=1)
        
        t.tr()
        t.td(gui.Spacer(width=8,height=8))
        
        ##The okay button CLICK event is connected to the Dailog's 
        ##send event method.  It will send a gui.CHANGE event.
        ##::
        t.tr()
        e = gui.Button("Okay")
        e.connect(gui.CLICK,self.send,gui.CHANGE)
        t.td(e)
        ##
        
        e = gui.Button("Cancel")
        e.connect(gui.CLICK,self.close,None)
        t.td(e)
        
        gui.Dialog.__init__(self,title,t)

if __name__ == '__main__':
    app = gui.Desktop()
    app.connect(gui.QUIT,app.quit,None)
    
    c = gui.Table(width=640,height=480)
    
    dialog = NewDialog()
    
    ##The dialog's CHANGE event is connected to this function that will display the form values.
    ##::
    def onchange(value):
        print('-----------')
        for k,v in value.value.items():
            print(k,v)
        value.close()
    
    dialog.connect(gui.CHANGE,onchange,dialog)
    ##
            
    e = gui.Button("New")
    e.connect(gui.CLICK,dialog.open,None)
    c.tr()
    c.td(e)
    
    app.run(c)
    #import profile
    #profile.run('app.run(c)')
