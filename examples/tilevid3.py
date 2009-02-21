"""<title>tutorial on how to load, display, and use Sprites</title>"""

import pygame
from pygame.rect import Rect
from pygame.locals import *

# the following line is not needed if pgu is installed
import sys; sys.path.insert(0, "..")

from pgu import tilevid, timer

SW,SH = 320,240
TW,TH = 16,16
SPEED = 2
FPS = 40

##Here are the various functions I used for the player and enemy logic.
##- After creating a Sprite, I set the clayer to 0 so that more than one player / enemy is created.
##- the Sprite must be added to the sprites list
##- instead of using class methods, I prefer to use set functions for
##the various methods -- loop and hit.
##- Enemies are removed when they go off screen.
##::
def player_new(g,t,value):
    g.clayer[t.ty][t.tx] = 0
    s = tilevid.Sprite(g.images['player'],t.rect)
    g.sprites.append(s)
    s.loop = player_loop
    
def player_loop(g,s):
    s.rect.x += SPEED
    
    keys = pygame.key.get_pressed()
    dx,dy = 0,0
    if keys[K_UP]: dy-=1
    if keys[K_DOWN]: dy+=1
    if keys[K_LEFT]: dx-=1
    if keys[K_RIGHT]: dx+=1
    s.rect.x += dx*5
    s.rect.y += dy*5
    s.rect.clamp_ip(g.view)
    
def enemy_new(g,t,value):
    g.clayer[t.ty][t.tx] = 0
    s = tilevid.Sprite(g.images['enemy'],t.rect)
    g.sprites.append(s)
    s.loop = enemy_loop
    
def enemy_loop(g,s):
    if s.rect.right < g.view.left:
        g.sprites.remove(s)
##
##Here I initialize the image data.  The columns are (name,file_name,shape)
##::
idata = [
    ('player','player.tga',(4,4,24,24)),
    ('enemy','enemy.tga',(4,4,24,24)),
    ('shot','shot.tga',(1,2,6,4)),
    ]
##
##Here I initialize the code data.  The columns are (function, config).
##::
cdata = {
    1:(player_new,None),
    2:(enemy_new,None),
    3:(enemy_new,None),
    4:(enemy_new,None),
    }
##
    
def init():
    g = tilevid.Tilevid()
    
    g.screen = pygame.display.set_mode((SW,SH),SWSURFACE)
    
    g.tga_load_tiles('tiles.tga',(TW,TH))
    g.tga_load_level('level.tga',1)
    g.bounds = pygame.Rect(TW,TH,(len(g.tlayer[0])-2)*TW,(len(g.tlayer)-2)*TH)
    
    ##In init(), loading in the sprite images.
    ##::
    g.load_images(idata)
    ##
    
    ##In init(), running the codes for the initial screen.
    ##::
    g.run_codes(cdata,(0,0,25,17))
    ##
    
    return g
    
def run(g): 
    g.quit = 0
    
    t = timer.Timer(FPS)
    
    g.paint(g.screen)
    pygame.display.flip()
    
    while not g.quit:
        for e in pygame.event.get():
            if e.type is QUIT: g.quit = 1
            if e.type is KEYDOWN and e.key == K_ESCAPE: g.quit = 1
            
        g.view.x += SPEED

        ##In run(), each frame I make sure to run the codes that are on the far
        ##right of the screen.
        ##::
        g.run_codes(cdata,(g.view.right/TW,0,1,17))
        ##
        
        g.loop()
        updates = g.update(g.screen)
        pygame.display.update(updates)
        
        t.tick()
    
run(init())
