"""<title>tutorial on how to scroll and use a Timer object</title>"""

import pygame
from pygame.locals import *

# the following line is not needed if pgu is installed
import sys; sys.path.insert(0, "..")

from pgu import tilevid, timer

SW,SH = 320,240
TW,TH = 16,16
SPEED = 2
FPS = 40

def init():
    g = tilevid.Tilevid()
    
    g.screen = pygame.display.set_mode((SW,SH),SWSURFACE)
    
    g.tga_load_tiles('tiles.tga',(TW,TH))
    
    ##In init(), I add bg=1 to tga_load_level so that the background layer is
    ##also loaded.
    ##::
    g.tga_load_level('level.tga',1)
    ##
    
    ##In init(), I also set the bounds of the level.  The view will never go
    ##outside the bounds of the level.
    ##::
    g.bounds = pygame.Rect(TW,TH,(len(g.tlayer[0])-2)*TW,(len(g.tlayer)-2)*TH)
    ##
    
    return g

def run(g): 
    g.quit = 0
    
    ##In run(), I add a Timer so that I can keep a constant framerate of FPS fps.
    ##::
    t = timer.Timer(FPS)
    ##
    
    g.paint(g.screen)
    pygame.display.flip()
    
    while not g.quit:
        for e in pygame.event.get():
            if e.type is QUIT: g.quit = 1
            if e.type is KEYDOWN and e.key == K_ESCAPE: g.quit = 1
            
        ##In run(), each frame I move the view to the right by SPEED pixels.
        ##::
        g.view.x += SPEED
        ##
        
        g.loop()
        updates = g.update(g.screen)
        pygame.display.update(updates)
        
        ##In run(), at the end of each frame, I give the timer a tick.  The timer will delay the 
        ##appropriate length.
        ##::
        t.tick()
        ##
    
run(init())
