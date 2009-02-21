"""<title>tutorial on how to add in tile hit handlers, set up groups and agroups</title>"""

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

def player_new(g,t,value):
    g.clayer[t.ty][t.tx] = 0
    s = tilevid.Sprite(g.images['player'],t.rect)
    g.sprites.append(s)
    s.loop = player_loop
    ##In player_new() I add the player to the 'player' group, and set the score to 0. I also set the game's player to this Sprite.
    ##::
    s.groups = g.string2groups('player')
    s.score = 0
    g.player = s
    ##
    
def player_loop(g,s):
    ##In player_loop(), I now check if the player has gone off screen (due to blocks
    ##in the players way.  If that happens, the game quits.
    ##::
    if s.rect.right < g.view.left: g.quit = 1
    ##
    
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
    
##A few functions are added to handle player/tile hits
##::
def tile_block(g,t,a):
    c = t.config
    if (c['top'] == 1 and a._rect.bottom <= t._rect.top and a.rect.bottom > t.rect.top):
        a.rect.bottom = t.rect.top
    if (c['left'] == 1 and a._rect.right <= t._rect.left and a.rect.right > t.rect.left):
        a.rect.right = t.rect.left
    if (c['right'] == 1 and a._rect.left >= t._rect.right and a.rect.left < t.rect.right):
        a.rect.left = t.rect.right
    if (c['bottom'] == 1 and a._rect.top >= t._rect.bottom and a.rect.top < t.rect.bottom):
        a.rect.top = t.rect.bottom

def tile_coin(g,t,a):
    a.score += 100
    g.set((t.tx,t.ty),0)
    
def tile_fire(g,t,a):
    g.quit = 1
##

idata = [
    ('player','player.tga',(4,4,24,24)),
    ('enemy','enemy.tga',(4,4,24,24)),
    ('shot','shot.tga',(1,2,6,4)),
    ]

cdata = {
    1:(player_new,None),
    2:(enemy_new,None),
    3:(enemy_new,None),
    4:(enemy_new,None),
    }

##Here I initialize the tile data.  The columns are (groups,function,config)
##::
tdata = {
    0x01:('player',tile_block,{'top':1,'bottom':1,'left':1,'right':1}),
    0x02:('player',tile_block,{'top':1,'bottom':1,'left':1,'right':1}),
    0x20:('player',tile_coin,None),
    0x30:('player',tile_fire,None),
    }
##

    
def init():
    g = tilevid.Tilevid()
    
    g.screen = pygame.display.set_mode((SW,SH),SWSURFACE)
    
    ##In init(), this line has been changed to load the tiles with their properties (groups, functions, and config.
    ##::
    g.tga_load_tiles('tiles.tga',(TW,TH),tdata)
    ##
    g.tga_load_level('level.tga',1)
    g.bounds = pygame.Rect(TW,TH,(len(g.tlayer[0])-2)*TW,(len(g.tlayer)-2)*TH)
    g.load_images(idata)
    g.run_codes(cdata,(0,0,25,17))
    pygame.font.init()
    g.font = pygame.font.SysFont('helvetica',16)

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
        g.run_codes(cdata,(g.view.right/TW,0,1,17))
        
        g.loop()

        ##In run(), I have changed the update function to paint, so that
        ##I can display the player's score on the screen at all times.
        ##::
        g.paint(g.screen)
        img = g.font.render('%05d'%g.player.score,1,(0,0,0))
        g.screen.blit(img,(0+1,SH-img.get_height()+1))
        img = g.font.render('%05d'%g.player.score,1,(255,255,255))
        g.screen.blit(img,(0,SH-img.get_height()))
        pygame.display.flip()
        ##

        t.tick()
    
run(init())
