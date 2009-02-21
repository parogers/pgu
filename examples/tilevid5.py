"""<title>tutorial on how to add Sprite collision hit handlers, custom painting</title>"""

import pygame
from pygame.rect import Rect
from pygame.locals import *
import math
import random

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
    s.groups = g.string2groups('player')
    s.score = 0
    g.player = s
    ##In player_new() I add the shoot handler.
    ##::
    s.shoot = player_shoot
    ##

def player_loop(g,s):
    if s.rect.right < g.view.left: g.quit = 1
    
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
    
    ##In player_loop(), I check for the spacebar.  The spacebar triggers a shot every 8 frames.
    ##::
    if keys[K_SPACE] and g.frame%8==0:
        shot_new(g,s,None)
    ##

##The player_shoot() handler, as well as the shot Sprite functions.  The shot group
##has its agroup set to 'enemy' so it can hit 'enemy' Sprites.
##::
def player_shoot(g,s):
    shot_new(g,s,None)
    
def shot_new(g,t,value):
    s = tilevid.Sprite(g.images['shot'],(t.rect.right,t.rect.centery-2))
    g.sprites.append(s)
    s.agroups = g.string2groups('enemy')
    s.hit = shot_hit
    s.loop = shot_loop

def shot_loop(g,s):
    s.rect.x += 8
    if s.rect.left > g.view.right:
        g.sprites.remove(s)
##    
        
def shot_hit(g,s,a):
    if a in g.sprites: g.sprites.remove(a)
    g.player.score += 500

        
def enemy_new(g,t,value):
    g.clayer[t.ty][t.tx] = 0
    s = tilevid.Sprite(g.images['enemy'],t.rect)
    g.sprites.append(s)
    s.loop = enemy_loop
##In enemy_new(), I've added a lot more detail.
##- A move function to handle the type of movement the enemy will do.
##- A record of the origin and entering frame of the enemy (useful for the move functions.)
##- Set up the groups and agroups and a hit handler for the enemy.
##::
    s.move = value['move']
    s.origin = pygame.Rect(s.rect)
    s.frame = g.frame
    s.groups = g.string2groups('enemy')
    s.agroups = g.string2groups('player')
    s.hit = enemy_hit
##

##When an enemy is hit, the game quits.
##::
def enemy_hit(g,s,a):
    g.quit = 1
##

def enemy_loop(g,s):
    ##In enemy_loop() we call the move handler.
    ##::
    s.move(g,s)
    ##
    if s.rect.right < g.view.left:
        g.sprites.remove(s)

##The enemy movement handlers.
##::
def enemy_move_line(g,s):
    s.rect.x -= 3
    
def enemy_move_sine(g,s):
    s.rect.x -= 2
    s.rect.y = s.origin.y + 65*math.sin((g.frame-s.frame)/10.0)
    
def enemy_move_circle(g,s):
    s.origin.x -= 1
    s.rect.y = s.origin.y + 50*math.sin((g.frame-s.frame)/10.0)
    s.rect.x = s.origin.x + 50*math.cos((g.frame-s.frame)/10.0)
##
        
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

##The codes data has been updated to include information about the appropriate
##movement handlers for enemies.
##::
cdata = {
    1:(player_new,None),
    2:(enemy_new,{'move':enemy_move_line}),
    3:(enemy_new,{'move':enemy_move_sine}),
    4:(enemy_new,{'move':enemy_move_circle}),
    }
##

tdata = {
    0x01:('player',tile_block,{'top':1,'bottom':1,'left':1,'right':1}),
    0x02:('player',tile_block,{'top':1,'bottom':1,'left':1,'right':1}),
    0x20:('player',tile_coin,None),
    0x30:('player',tile_fire,None),
    }
    
def init():
    g = tilevid.Tilevid()
    
    ##In init(), set the g.view size so that all the handlers will work properly.  (The player_loop one depends on view having the correct size.)
    ##::
    g.view.w,g.view.h = SW,SH
    ##
    
    g.screen = pygame.display.set_mode((SW,SH),SWSURFACE)
    g.frame = 0
    
    g.tga_load_tiles('tiles.tga',(TW,TH),tdata)
    ##In init() I no longer have tga_load_level load the background layer, as 
    ##we will generate our own multi-layered starfield.
    ##::
    g.tga_load_level('level.tga')
    ##
    g.bounds = pygame.Rect(TW,TH,(len(g.tlayer[0])-2)*TW,(len(g.tlayer)-2)*TH)
    g.load_images(idata)
    g.run_codes(cdata,(0,0,25,17))
    pygame.font.init()
    g.font = pygame.font.SysFont('helvetica',16)

    return g
    
def run(g): 
    g.quit = 0
    ##In run(), adding a pause variable to the game.
    ##::
    g.pause = 0
    ##
    
    t = timer.Timer(FPS)

    ##In run(), initializing the stars.
    ##::
    stars = []
    NS = 256
    for n in range(0,NS):
        stars.append([random.randrange(0,SW),random.randrange(0,SH),random.randrange(2,8)])
    ##
    
    while not g.quit:
        for e in pygame.event.get():
            if e.type is QUIT: g.quit = 1
            if e.type is KEYDOWN and e.key == K_ESCAPE: g.quit = 1
            ##In run(), in the event loop, checking for F10 for full screen, RETURN for pause.
            ##::
            if e.type is KEYDOWN and e.key == K_F10:
                #g.screen = pygame.display.set_mode((SW,SH),FULLSCREEN|HWSURFACE|DOUBLEBUF)
                pygame.display.toggle_fullscreen()
                
            if e.type is KEYDOWN and e.key == K_RETURN:
                g.pause ^= 1
            ##

        ##In run(), handles pause, and also renders the star field before the
        ##foreground is painted.
        ##::
        if not g.pause:
            g.view.x += SPEED
            g.run_codes(cdata,(g.view.right/TW,0,1,17))
            
            g.loop()
    
            g.screen.fill((0,0,0))
            n = 0
            for n in range(0,NS):
                x,y,s = stars[n]
                if ((g.frame*s)%8) < s:
                    x -= 1
                if x < 0: x += SW
                stars[n][0] = x
                g.screen.set_at((x,y),(255,255,255))

            g.paint(g.screen)
            img = g.font.render('%05d'%g.player.score,1,(0,0,0))
            g.screen.blit(img,(0+1,SH-img.get_height()+1))
            img = g.font.render('%05d'%g.player.score,1,(255,255,255))
            g.screen.blit(img,(0,SH-img.get_height()))
            pygame.display.flip()
            
            g.frame += 1
        ##

        t.tick()
        
    
run(init())
