"""<title>Dialogs and Documents</title>
"""
import pygame
from pygame.locals import *

# the following line is not needed if pgu is installed
import sys; sys.path.insert(0, "..")

from pgu import gui

##Documents layout widgets like words and images in a HTML document.  This
##example also demonstrates the ScrollBox container widget.
##::
class AboutDialog(gui.Dialog):
    def __init__(self,**params):
        title = gui.Label("About Cuzco's Paint")
        
        width = 400
        height = 200
        doc = gui.Document(width=width)
        
        space = title.style.font.size(" ")
        
        doc.block(align=0)
        for word in """Cuzco's Paint v1.0 by Phil Hassey""".split(" "): 
            doc.add(gui.Label(word))
            doc.space(space)
        doc.br(space[1])
        
        doc.block(align=-1)
        doc.add(gui.Image("cuzco.png"),align=1)
        for word in """Cuzco's Paint is a revolutionary new paint program it has all the awesome features that you need to paint really great pictures.""".split(" "): 
            doc.add(gui.Label(word))
            doc.space(space)
        doc.br(space[1])
        
        doc.block(align=-1)
        for word in """Cuzco's Paint will drive you wild!  Cuzco's Paint was made as a demo of Phil's Pygame Gui.  We hope you enjoy it!""".split(" "): 
            doc.add(gui.Label(word))
            doc.space(space)
            
        for i in range(0,10):
            doc.block(align=-1)
            for word in """This text has been added so we can show off our ScrollArea widget.  It is a very nice widget built by Gal Koren!""".split(" "):
                doc.add(gui.Label(word))
                doc.space(space)
            doc.br(space[1])
                
        gui.Dialog.__init__(self,title,gui.ScrollArea(doc,width,height))
##
        
        
if __name__ in '__main__':
    app = gui.Desktop()
    app.connect(gui.QUIT,app.quit,None)
    
    c = gui.Table(width=640,height=480)
    
    ##The button CLICK event is connected to the dialog.open method.
    ##::
    dialog = AboutDialog()
            
    e = gui.Button("About")
    e.connect(gui.CLICK,dialog.open,None)
    ##
    c.tr()
    c.td(e)
    
    app.run(c)
