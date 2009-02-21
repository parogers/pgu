"""<title>an example of html usage</title>"""
import pygame
from pygame.locals import *

# the following line is not needed if pgu is installed
import sys; sys.path.insert(0, "..")

from pgu import html

pygame.font.init()

screen = pygame.display.set_mode((320,320),SWSURFACE)
fg = (0,0,0)
bg = (255,255,255)
screen.fill(bg)

font = pygame.font.SysFont("sans", 16)

##::
html.write(screen,font,pygame.Rect(0,0,320,320),"""
<p>Welcome to my humble website.</p>
<p><img src='cuzco.png' align=right>As usual we have an image of
Cuzco included in every location we could possibly think of.</p>
<p align='center'>Cuzco is a <b>very big</b> goat.</p>
<p align='right'><img src='cuzco.png' align=left>
If I wanted to be really silly, I would be sure to add link
ability to this module.  But that would be gold plating.</p>
""")
##

pygame.display.flip()

_quit = 0
while not _quit:
    for e in pygame.event.get():
        if e.type is QUIT: _quit = 1
    pygame.time.wait(10)
