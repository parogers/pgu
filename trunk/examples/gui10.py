"""<title>Integration with a Game</title>
For games, it is usually preferrable to not have your game within
a GUI framework.  This GUI framework can be placed within your game.
"""

import pygame
from pygame.locals import *

# the following line is not needed if pgu is installed
import sys; sys.path.insert(0, "..")

from pgu import gui
from gui7 import ColorDialog

W,H = 640,480
W2,H2 = 320,240

##You can initialize the screen yourself.
##::
screen = pygame.display.set_mode((640,480),SWSURFACE)
##

form = gui.Form()

class StarControl(gui.Table):
    def __init__(self,**params):
        gui.Table.__init__(self,**params)
        fg = (255,255,255)

        self.tr()
        self.td(gui.Label("Phil's Pygame GUI",color=fg),colspan=2)
        
        self.tr()
        self.td(gui.Label("Speed: ",color=fg),align=1)
        e = gui.HSlider(100,-500,500,size=20,width=100,height=16,name='speed')
        self.td(e)
        
        self.tr()
        self.td(gui.Label("Size: ",color=fg),align=1)
        e = gui.HSlider(2,1,5,size=20,width=100,height=16,name='size')
        self.td(e)
        
        self.tr()
        self.td(gui.Label("Quantity: ",color=fg),align=1)
        e = gui.HSlider(100,1,1000,size=20,width=100,height=16,name='quantity')
        self.td(e)
        
        self.tr()
        self.td(gui.Label("Color: ",color=fg),align=1)
        
        
        default = "#ffffff"
        color = gui.Color(default,width=64,height=10,name='color')
        color_d = ColorDialog(default)
                
        color.connect(gui.CLICK,color_d.open,None)
        color_d.connect(gui.CHANGE,gui.action_setvalue,(color_d,color))
        self.td(color)
        
        self.tr()
        self.td(gui.Label("Full Screen: ",color=fg),align=1)
        self.td(gui.Switch(value=False,name='fullscreen'))
        
        self.tr()
        self.td(gui.Label("Warp Speed: ",color=fg),align=1)
        self.td(gui.Switch(value=False,name='warp'))
        

##Using App instead of Desktop removes the GUI background.  Note the call to app.init()
##::
app = gui.App()
t = StarControl()

c = gui.Container(align=-1,valign=-1)
c.add(t,0,0)

app.init(c)
##

import random
dist = 8192
span = 10
stars = []
def reset():
    global stars
    stars = []
    for i in range(0,form['quantity'].value):
        stars.append([random.randrange(-W*span,W*span),random.randrange(-H*span,H*span),random.randrange(1,dist)])
        
def adjust(n):
    if n < 0:
        for i in range(n,0): stars.pop()
        return
    for i in range(0,n):
        stars.append([random.randrange(-W*span,W*span),random.randrange(-H*span,H*span),random.randrange(1,dist)])
    
        
def render():
    speed,size,color,warp = form['speed'].value,form['size'].value,form['color'].value,form['warp'].value
    colors = []
    for i in range(256,0,-1):
        colors.append((color[0]*i/256,color[1]*i/256,color[2]*i/256))
        
    n = 0
    for x,y,z in stars:
        if warp:
            z1 = max(1,z + speed*2)
            x1 = x*256/z1
            y1 = y*256/z1
            xx1,yy1 = x1+W2,y1+H2
    
        x = x*256/z
        y = y*256/z
        xx,yy = x+W2,y+H2
        c = min(255,z * 255 / dist)
        
        if warp:
            pygame.draw.line(screen,colors[c],(xx1,yy1),(xx,yy),size)
        
        pygame.draw.circle(screen,colors[c],(xx,yy),size)
        
        ch = 0
        z -= speed
        if z <= 0: 
            ch = 1
            z += dist
        if z > dist: 
            ch = 1
            z -= dist
        if ch:
            stars[n][0] = random.randrange(-W*span,W*span)
            stars[n][1] = random.randrange(-H*span,H*span)
        stars[n][2] = z
        
        n += 1
        

##You can include your own run loop.
##::
_form = form.results()
reset()
_quit = 0
while not _quit:
    if form['quantity'].value != _form['quantity']: adjust(form['quantity'].value-_form['quantity'])
    if form['fullscreen'].value != _form['fullscreen']:
        pygame.display.toggle_fullscreen()
    _form = form.results()
    
    screen.fill((0,0,0)) #clear the screen
    render() #renders the starfield
    for e in pygame.event.get():
        if e.type is QUIT: _quit = 1
        if e.type is KEYDOWN and e.key == K_ESCAPE: _quit = 1
        app.event(e)
    app.paint(screen)
    pygame.display.flip()
    pygame.time.wait(10)
##
