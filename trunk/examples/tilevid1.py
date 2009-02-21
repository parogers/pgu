"""<title>tutorial on how to load tiles and levels</title>

<p>The following tutorial demonstrates how to use tileedit and leveledit via the
command line.  You can just as easily do all these things via the in-program
"File/Open" and "File/New" menu items.

<p>Here's an introduction to using tileedit and leveledit
<pre>$ -- linux, etc instructions
C:\> -- windows instructions</pre>

<p>first you need to be in the examples dir for this tutorial to
work

<pre>$ cd examples
C:\pgu> cd examples

$ tileedit tiles.tga 16 16
C:\pgu\examples> python ../scripts/tileedit tiles.tga 16 16</pre>

<p>the next time you run tileedit, you will not need to provide 
the width and height of the tiles

<pre>$ tileedit codes.tga 16 16
C:\pgu\examples> python ../scripts/tileedit codes.tga 16 16</pre>

<p>the next time you run tileedit, you will not need to provide 
the width and height of the codes

<pre>$ leveledit level.tga tiles.tga codes.tga 16 16
C:\pgu\examples> python ../scripts/leveledit level.tga tiles.tga codes.tga 16 16</pre>

<p>the next time you run leveledit, you will not need to provide
the tiles, codes, and width and height of the tiles

"""




import pygame
from pygame.locals import *

# the following line is not needed if pgu is installed
import sys; sys.path.insert(0, "..")

from pgu import tilevid

SW,SH = 320,240
TW,TH = 16,16

##This is the initialization function I created for
##the game.
##
##I use the tga_ methods to load up the tiles and level I created.
##::
def init():
    g = tilevid.Tilevid()

    g.screen = pygame.display.set_mode((SW,SH),SWSURFACE)
    
    g.tga_load_tiles('tiles.tga',(TW,TH))
    g.tga_load_level('level.tga')

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
