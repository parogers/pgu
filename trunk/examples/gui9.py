"""<title>Menus, Toolboxes, a full Application</title>
Most all widgets are used in this example.  A full custom widget
is included.  A number of connections are used to make the application
function.
"""
import pygame
from pygame.locals import *

# the following line is not needed if pgu is installed
import sys; sys.path.insert(0, "..")

from pgu import gui

from gui6 import AboutDialog
from gui7 import ColorDialog
from gui8 import NewDialog

class HelpDialog(gui.Dialog):
    def __init__(self,**params):
        title = gui.Label("Help")
        
        doc = gui.Document(width=400)
        
        space = title.style.font.size(" ")
        
        doc.block(align=-1)
        doc.add(gui.Image("cuzco.png"),align=1)
        for word in """Cuzco's Paint is a revolutionary new paint program it has all the awesome features that you need to paint really great pictures.""".split(" "): 
            doc.add(gui.Label(word))
            doc.space(space)
        doc.br(space[1])
        
        doc.block(align=-1)    
        for word in """This help isn't really here for any other reason than to have a help dialog.""".split(" "): 
            doc.add(gui.Label(word))
            doc.space(space)

        gui.Dialog.__init__(self,title,doc)
        
class QuitDialog(gui.Dialog):
    def __init__(self,**params):
        title = gui.Label("Quit")
        
        t = gui.Table()
        
        t.tr()
        t.add(gui.Label("Are you sure you want to quit?"),colspan=2)
        
        t.tr()
        e = gui.Button("Okay")
        e.connect(gui.CLICK,self.send,gui.QUIT)
        t.td(e)
        
        e = gui.Button("Cancel")
        e.connect(gui.CLICK,self.close,None)
        t.td(e)
        
        gui.Dialog.__init__(self,title,t)

class WelcomeDialog(gui.Dialog):
    def __init__(self,**params):
        title = gui.Label("Welcome")
        
        doc = gui.Document(width=400)
        
        space = title.style.font.size(" ")

        doc.block(align=-1)
        doc.add(gui.Image("cuzco.png"),align=1)
        for word in """Welcome to Cuzco's Paint.  Cuzco's Paint is a demo of the features of Phil's Pygame GUI.  Cuzco's Paint only supports saving in the .TGA format.""".split(" "): 
            doc.add(gui.Label(word))
            doc.space(space)

        gui.Dialog.__init__(self,title,doc)

class OpenDialog(gui.Dialog):
    def __init__(self,**params):
        title = gui.Label("Open Picture")
        
        t = gui.Table()
        
        self.value = gui.Form()
        
        t.tr()
        t.td(gui.Label("Open: "))
        t.td(gui.Input(name="fname"),colspan=3)
        
        t.tr()
        e = gui.Button("Okay")
        e.connect(gui.CLICK,self.send,gui.CHANGE)
        t.td(e,colspan=2)
        
        e = gui.Button("Cancel")
        e.connect(gui.CLICK,self.close,None)
        t.td(e,colspan=2)
        
        gui.Dialog.__init__(self,title,t)

class SaveDialog(gui.Dialog):
    def __init__(self,**params):
        title = gui.Label("Save As...")
        
        t = gui.Table()
        
        self.value = gui.Form()
        
        t.tr()
        t.td(gui.Label("Save: "))
        t.td(gui.Input(name="fname"),colspan=3)
        
        t.tr()
        e = gui.Button("Okay")
        e.connect(gui.CLICK,self.send,gui.CHANGE)
        t.td(e,colspan=2)
        
        e = gui.Button("Cancel")
        e.connect(gui.CLICK,self.close,None)
        t.td(e,colspan=2)
        
        gui.Dialog.__init__(self,title,t)


class Painter(gui.Widget):
    def __init__(self,**params):
        gui.Widget.__init__(self,**params)
        
        self.surface = None
        self.state = 0
        self.cuzco = pygame.image.load("cuzco.png")
        
    def init(self,v):
        self.surface = pygame.Surface((int(v['width']),int(v['height'])))
        color = v['color']
        if v['color'] == 'custom': 
            color = v['custom']
        else: color = pygame.Color(color)
        self.surface.fill(color)
        self.overlay = pygame.Surface((int(v['width']),int(v['height'])),pygame.SRCALPHA,32)
        self.repaint()
        
    def event(self,e):
        if not self.surface: return
        
        if e.type == gui.MOUSEBUTTONDOWN:
            if hasattr(self,app.mode.value+"_down"):
                action = getattr(self,app.mode.value+"_down")
                action(e)
        if e.type == gui.MOUSEMOTION:
            if hasattr(self,app.mode.value+"_motion"):
                action = getattr(self,app.mode.value+"_motion")
                action(e)
        if e.type is gui.MOUSEBUTTONUP:
            if hasattr(self,app.mode.value+"_up"):
                action = getattr(self,app.mode.value+"_up")
                action(e)
    
    ##The Painter class has its own paint method to render the painting surface and overlay.
    ##::
    def paint(self,s):
        s.blit(self.surface,(0,0))
        s.blit(self.overlay,(0,0))
    ##
                            
    def draw_down(self,e):
        self.state = 1
        self.pos = e.pos
        self.draw_motion(e)
    def draw_motion(self,e):
        if self.state == 0: return
        pygame.draw.line(self.surface,app.color.value,self.pos,e.pos,2)
        self.pos = e.pos
        self.repaint()
    def draw_up(self,e):
        self.state = 0
        
    def cuzco_down(self,e):
        self.state = 1
        self.cuzco_motion(e)
    def cuzco_motion(self,e):
        if self.state == 0: return
        img = self.cuzco
        self.overlay.fill((0,0,0,0))
        self.overlay.blit(img,(e.pos[0]-img.get_width()/2,e.pos[1]-img.get_height()/2))
        self.repaint()
    def cuzco_up(self,e):
        self.state = 0
        self.surface.blit(self.overlay,(0,0))
        self.overlay.fill((0,0,0,0))
        self.repaint()
        
    def box_down(self,e):
        self.state = 1
        self.pos = e.pos
        self.box_motion(e)
    def box_motion(self,e):
        if self.state == 0: return
        self.overlay.fill((0,0,0,0))
        pygame.draw.rect(self.overlay,app.color.value,(self.pos[0],self.pos[1],e.pos[0]-self.pos[0],e.pos[1]-self.pos[1]))
        self.repaint()
    def box_up(self,e):
        self.state = 0
        self.surface.blit(self.overlay,(0,0))
        self.overlay.fill((0,0,0,0))
        self.repaint()
        
    
    def circle_down(self,e):
        self.state = 1
        self.pos = e.pos
        self.circle_motion(e)
    def circle_motion(self,e):
        if self.state == 0: return
        self.overlay.fill((0,0,0,0))
        r = pygame.Rect(self.pos[0],self.pos[1],e.pos[0]-self.pos[0],e.pos[1]-self.pos[1])
        r.x -= r.w
        r.w *= 2
        r.y -= r.h
        r.h *= 2
        r.normalize()
        pygame.draw.ellipse(self.overlay,app.color.value,r)
        self.repaint()
    def circle_up(self,e):
        self.state = 0
        self.surface.blit(self.overlay,(0,0))
        self.overlay.fill((0,0,0,0))
        self.repaint()
        
        

class App(gui.Desktop):
    def __init__(self,**params):
        gui.Desktop.__init__(self,**params)
        
        self.connect(gui.QUIT,self.quit,None)
        
        c = gui.Container(width=640,height=480)
        spacer = 8
        
        self.fname = 'untitled.tga'
        
        self.new_d = NewDialog()
        self.new_d.connect(gui.CHANGE,self.action_new,None)
        self.open_d = OpenDialog()
        self.open_d.connect(gui.CHANGE,self.action_open,None)
        self.save_d = SaveDialog()
        self.save_d.connect(gui.CHANGE,self.action_saveas,None)
        self.quit_d = QuitDialog()
        self.quit_d.connect(QUIT,self.quit,None)
        
        self.help_d = HelpDialog()
        self.about_d = AboutDialog()
        
        ##Initializing the Menus, we connect to a number of Dialog.open methods for each of the dialogs.
        ##::
        menus = gui.Menus([
            ('File/New',self.new_d.open,None),
            ('File/Open',self.open_d.open,None),
            ('File/Save',self.action_save,None),
            ('File/Save As',self.save_d.open,None),
            ('File/Exit',self.quit_d.open,None),
            ('Help/Help',self.help_d.open,None),
            ('Help/About',self.about_d.open,None),
            ])
        ##
        c.add(menus,0,0)
        menus.rect.w,menus.rect.h = menus.resize()
        #print 'menus',menus.rect
        
        ##We utilize a Toolbox.  The value of this widget determins how drawing is done in the Painter class.
        ##::
        self.mode = mode = gui.Toolbox([
            ('Draw','draw'),
            ('Box','box'),
            ('Circle','circle'),
            ('Cuzco','cuzco'),
            ],cols=1,value='draw')
        ##
        c.add(mode,0,menus.rect.bottom+spacer)
        mode.rect.x,mode.rect.y = mode.style.x,mode.style.y
        mode.rect.w,mode.rect.h = mode.resize()
        #mode._resize()
        
        default = "#000000"
        self.color = color = gui.Color(default,width=mode.rect.w,height=mode.rect.w)
        self.color_d = ColorDialog(default)
        
        color.connect(gui.CLICK,self.color_d.open,None)

        # Updates the toolbox color picker with the value in the color dialog box
        def change_cb(*args):
            self.color.value = self.color_d.value
        self.color_d.connect(gui.CHANGE, change_cb)

        c.add(self.color,0,mode.rect.bottom+spacer)
        self.color.rect.w,self.color.rect.h = self.color.resize()
        #self.color._resize()

        self.painter = Painter(width=c.rect.w-mode.rect.w-spacer*2,height=c.rect.h-menus.rect.h-spacer*2,style={'border':1})
        c.add(self.painter,mode.rect.w+spacer,menus.rect.h+spacer)
        self.painter.init({'width':256,'height':256,'color':'#ffffff'})
        self.painter.rect.w,self.painter.rect.h = self.painter.resize()
        #self.painter._resize()

        welcome_d = WelcomeDialog()
        self.connect(gui.INIT,welcome_d.open,None)
        
        self.widget = c
        
    def action_new(self,value):
        self.new_d.close()
        self.fname = 'untitled.tga'
        self.painter.init(self.new_d.value.results())
        
    def action_save(self,value):
        pygame.image.save(self.painter.surface,self.fname)
        
    def action_saveas(self,value):
        self.save_d.close()
        self.fname = self.save_d.value['fname'].value
        pygame.image.save(self.painter.surface,self.fname)
        
    def action_open(self,value):
        self.open_d.close()
        self.fname = self.open_d.value['fname']
        self.painter.surface = pygame.image.load(self.fname)
        self.painter.repaint()
        
        
app = App()
app.run()
