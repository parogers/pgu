"""<title>Integration with a Game</title>
For games, it is usually preferrable to not have your game within
a GUI framework.  This GUI framework can be placed within your game.
"""

import time
import random
import pygame
from pygame.locals import *

# the following line is not needed if pgu is installed
import sys; sys.path.insert(0, "..")

from pgu import gui
from gui7 import ColorDialog

# The maximum frame-rate
FPS = 30
WIDTH,HEIGHT = 640,480

##You can initialize the screen yourself.
##::
screen = pygame.display.set_mode((640,480),SWSURFACE)
##

class StarControl(gui.Table):
    def __init__(self,**params):
        gui.Table.__init__(self,**params)

        def fullscreen_changed(btn):
            #pygame.display.toggle_fullscreen()
            print("TOGGLE FULLSCREEN")

        def stars_changed(slider):
            n = slider.value - len(stars)
            if n < 0:
                for i in range(n,0): 
                    stars.pop()
            else:
                for i in range(0,n):
                    stars.append([random.randrange(-WIDTH*span,WIDTH*span),
                                  random.randrange(-HEIGHT*span,HEIGHT*span),
                                  random.randrange(1,dist)])

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
        e.connect(gui.CHANGE, stars_changed, e)
        self.td(e)
        
        self.tr()
        self.td(gui.Label("Color: ",color=fg),align=1)
        
        
        default = "#ffffff"
        color = gui.Color(default,width=64,height=10,name='color')
        color_d = ColorDialog(default)

        color.connect(gui.CLICK,color_d.open,None)
        self.td(color)
        def update_col():
            color.value = color_d.value
        color_d.connect(gui.CHANGE,update_col)
        
        btn = gui.Switch(value=False,name='fullscreen')
        btn.connect(gui.CHANGE, fullscreen_changed, btn)

        self.tr()
        self.td(gui.Label("Full Screen: ",color=fg),align=1)
        self.td(btn)
        
        self.tr()
        self.td(gui.Label("Warp Speed: ",color=fg),align=1)
        self.td(gui.Switch(value=False,name='warp'))
        

##Using App instead of Desktop removes the GUI background.  Note the call to app.init()
##::

form = gui.Form()

app = gui.App()
starCtrl = StarControl()

c = gui.Container(align=-1,valign=-1)
c.add(starCtrl,0,0)

app.init(c)
##

dist = 8192
span = 10
stars = []
def reset():
    global stars
    stars = []
    for i in range(0,form['quantity'].value):
        stars.append([random.randrange(-WIDTH*span,WIDTH*span),
                      random.randrange(-HEIGHT*span,HEIGHT*span),
                      random.randrange(1,dist)])
        

def render(dt):
    speed = form['speed'].value*10
    size = form['size'].value
    color = form['color'].value
    warp = form['warp'].value

    colors = []
    for i in range(256,0,-1):
        colors.append((color[0]*i/256,color[1]*i/256,color[2]*i/256))
        
    n = 0
    for x,y,z in stars:
        if warp:
            z1 = max(1,z + speed*2)
            x1 = x*256/z1
            y1 = y*256/z1
            xx1,yy1 = x1+WIDTH/2,y1+HEIGHT/2
    
        x = x*256/z
        y = y*256/z
        xx,yy = x+WIDTH/2,y+HEIGHT/2
        c = min(255,z * 255 / dist)
        col = colors[int(c)]

        if warp:
            pygame.draw.line(screen,col,
                             (int(xx1),int(yy1)),
                             (int(xx),int(yy)),size)
        
        pygame.draw.circle(screen,col,(int(xx),int(yy)),size)
        
        ch = 0
        z -= speed*dt
        if z <= 0: 
            ch = 1
            z += dist
        if z > dist: 
            ch = 1
            z -= dist
        if ch:
            stars[n][0] = random.randrange(-WIDTH*span,WIDTH*span)
            stars[n][1] = random.randrange(-HEIGHT*span,HEIGHT*span)
        stars[n][2] = z
        
        n += 1
        

##You can include your own run loop.
##::
reset()
clock = pygame.time.Clock()
done = False
while not done:
    for e in pygame.event.get():
        if e.type is QUIT: 
            done = True
        elif e.type is KEYDOWN and e.key == K_ESCAPE: 
            done = True
        else:
            app.event(e)

    # Clear the screen and render the stars
    dt = clock.tick(FPS)/1000.0
    screen.fill((0,0,0))
    render(dt)
    app.paint()
    pygame.display.flip()


