"""<title>tutorial on how to load tiles and levels with hexvid</title>
<p>
you should go through the tilevid tutorials before you view these.  hexvid
is just another vid interface.

<pre>$ leveledit hexlevel.tga hextiles.tga hexcodes.tga 32 64 --hex
C:\pgu\examples> python ../scripts/leveledit hexlevel.tga hextiles.tga hexcodes.tga 32 64 --hex</pre>

<p>the next time you run leveledit, you will not need to provide
the tiles, codes, and width and height of the tiles
"""

import pygame
from pygame.locals import *

# the following line is not needed if pgu is installed
import sys; sys.path.insert(0, "..")

from pgu import hexvid

SW,SH = 320,240
TW,TH = 32,28

##This is the initialization function I created for
##the game.
##
##I use the tga_ methods to load up the tiles and level I created.
##::
def init():
    g = hexvid.Hexvid()

    g.screen = pygame.display.set_mode((SW,SH),SWSURFACE)
    
    g.tga_load_tiles('hextiles.tga',(TW,TH))
    g.tga_load_level('hexlevel.tga')
    
    g.view.x = -320
    g.view.y = 200

    return g
##
    
##This is the run function I created for the game.  In this example,
##the level is displayed, but there is no interaction (other than allowing the
##user to quit via ESC or the QUIT signal.
##::
def run(g): 
    g.quit = 0
    
    g.paint(g.screen)
    pygame.display.flip()
    
    while not g.quit:
        for e in pygame.event.get():
            if e.type is QUIT: g.quit = 1
            if e.type is KEYDOWN and e.key == K_ESCAPE: g.quit = 1
        
        g.loop()
        updates = g.update(g.screen)
        pygame.display.update(updates)
##    
    
run(init())
