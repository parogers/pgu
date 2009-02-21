"""<title>an example of text usage</title>"""
import pygame
from pygame.locals import *

# the following line is not needed if pgu is installed
import sys; sys.path.insert(0, "..")

from pgu import text

pygame.font.init()

screen = pygame.display.set_mode((640,480),SWSURFACE)
fg = (0,0,0)
bg = (0,192,255)
screen.fill(bg)
bg = (255,255,255)

font = pygame.font.SysFont("default", 24)

##::
text.write(screen,font,(0,0),bg,"Hello World!")
text.writec(screen,font,bg,"Centered Text")
text.writepre(screen,font,pygame.Rect(160,48,320,100),fg,"""This is some
preformatted
    t e  x   t""")
text.writewrap(screen,font,pygame.Rect(160,268,320,100),fg,"""This is some text that will wrap automatically. This is some text that will wrap automatically.
 
This is some text that will wrap automatically. This is some text that will wrap automatically.""")
##
    
pygame.display.flip()

_quit = 0
while not _quit:
    for e in pygame.event.get():
        if e.type is QUIT: _quit = 1
    pygame.time.wait(10)
