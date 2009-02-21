#!/usr/bin/python
"""<title>a simple level editor for pygame</title>
<pre>
usage: leveledit level.tga [tiles.tga] [codes.tga] [tile_w] [tile_h]
windows: python leveledit level.tga [tiles.tga] [codes.tga] [tile_w] [tile_h]

options:
  -h, --help            show this help message and exit
  -tTILES, --tiles=TILES
                        filename of the tiles image
  -cCODES, --codes=CODES
                        file name of the codes image
  --tw=TILE_W           tile width
  --th=TILE_H           tile height
  --vw=VIEW_W           view width
  --vh=VIEW_H           view height
  --sw=SCREEN_W         screen width
  --sh=SCREEN_H         screen height
  --c=CLASS             class (e.g. pgu.tilevid.Tilevid)
  --tile                use pgu.tilevid.Tilevid
  --iso                 use pgu.isovid.Isovid
  --hex                 use pgu.hexvid.Hexvid
  -a, --app             set application level defaults

example:
leveledit level.tga tiles.tga codes.tga 16 16

note:
the editor can only edit tga files.  the output files will
have the "tile" layer in the red channel, the "bkgr" layer
in the green channel, and the "code" layer in the blue channel.

you may edit default options in leveledit.ini

interface:
- menus for common commands
- toolbox
- tile edit area
    left click to use current tool
    right click to select a tile
    middle drag to move around the level
- tile select area
    click to select a tile
- code select area
    click to select a code

keys:
l - load
s - save
p - preview

a - select all
z - undo
c - copy selection to clipboard
v - paste clipboard at selection origin
delete - delete selection
f - fill selection

t - switch tile & bkgr layers

arrows - change tile
shift+arrows - scroll screen by 1/8 screen size jumps
ctrl+arrows - scroll screen by full screen size jumps
return - toggle fullscreen
</pre>
"""

import os,sys    
from optparse import OptionParser
from ConfigParser import ConfigParser
import pygame
from pygame.locals import *

# the following line is not needed if pgu is installed
import sys; sys.path.insert(0, "..")

from pgu import gui, html, tilevid, isovid, hexvid



#whatever...
ini_fname = "leveledit.ini"
ini = ConfigParser()
cfg = {}

class _app(gui.Container):
    def __init__(self):
        gui.Container.__init__(self)
        #self.cls = "desktop"
        #self.background = gui.Box(self.style.background)

        self.screen_w = cfg['screen_w']
        self.screen_h = cfg['screen_h']
        self.screen = pygame.display.set_mode((self.screen_w,
            self.screen_h), SWSURFACE)

        self.fname = cfg['fname']
        
        k = cfg['class']
        parts = k.split(".")
        n = ".".join(parts[:-1])
        m = __import__(n,globals(),locals(),parts[-1])
        c = getattr(m,parts[-1])
        self.level = c()

        #self.level = pygame.image.load(self.level_fname)
        #self.level = tilevid.Tilevid()
        #g = self.level = isovid.Isovid()
        
    
        if self.fname != None:
            self.level.tga_load_level(self.fname,1)
        else:
            self.level.resize((cfg['width'],cfg['height']),1)
        #self.level_w, self.level_h = (self.level.get_width(), self.level.get_height())
        self.level_w, self.level_h = len(self.level.tlayer[0]),len(self.level.tlayer)

        self.tiles_last_ctime = None
        self.codes_last_ctime = None

        self.load_tiles_and_codes()
        



        
        
        self.tile = 0
        self.code = 0
        
        self.mode = 'tile'
        self.clipboard = None
        self.history = []
        #self.modrect = pygame.Rect(0xffff,0xffff,-0xffff,-0xffff)
        
        self.changes = []
        self.dirty = 0
        

    def load_tiles_and_codes(self):
        #
        #

        self.tile_w, self.tile_h = cfg['tile_w'], cfg['tile_h']

        self.tiles_fname = cfg['tiles']
        if os.path.isfile(self.tiles_fname):
            # we check to see if the ctime is the same.

            newctime = os.stat(self.tiles_fname)[9]
            if newctime <= self.tiles_last_ctime:
                #nothing to do, so we return.
                return

            self.tiles_last_ctime = newctime

            self.tiles = pygame.image.load(self.tiles_fname)
        else:
            self.tiles = hex_image(self)
        self.tiles_w, self.tiles_h = (self.tiles.get_width(),
            self.tiles.get_height())
        self.level.tga_load_tiles(self.tiles,(self.tile_w,self.tile_h))

        self.codes_fname = cfg['codes']
        if os.path.isfile(self.codes_fname):
            newctime = os.stat(self.codes_fname)[9]
            if newctime <= self.codes_last_ctime:
                #nothing to do, so we return.
                return
            self.codes_last_ctime = newctime

            self.codes = pygame.image.load(self.codes_fname)
        else:
            self.codes = hex_image(self)
                        
        self.codes_w, self.codes_h = (self.codes.get_width(),
            self.codes.get_height())

        
        tmp = self.level.tiles
        self.level.tiles = [None for i in xrange(0,256)]
        self.level.tga_load_tiles(self.codes,(self.tile_w,self.tile_h))
        self.level.codes = self.level.tiles
        self.level.tiles = tmp






    def mod(self,rect):
        self.dirty = 1
        self.changes.append((pygame.Rect(rect),self.copy(rect)))
    

    def view_init(self,dw,dh):        
        
        self.view_w = dw #/ self.tile_w
        self.view_h = dh #/ self.tile_h
        
        if 'view_w' in cfg and cfg['view_w'] != 0:
            self.view_w = min(self.view_w, cfg['view_w'])
        if 'view_h' in cfg and cfg['view_h'] != 0:
            self.view_h = min(self.view_h, cfg['view_h'])
        
        #self.view_w = min(self.level.size[0],self.view_w)
        #self.view_h = min(self.level.size[1],self.view_h)
        
        #print self.view_w,self.view_h
        
        #self.view = self.level.subsurface((0,0,self.view_w,self.view_h))
        self.select = Rect(0,0,self.level.size[0],self.level.size[1]) #self.view_w,self.view_h)
        
    def fill(self,rect,v):
        lvl = self.level
        w,h = lvl.size
        
        for layer,n in [ (lvl.tlayer,0), (lvl.blayer,1), (lvl.clayer,2) ]:
            for y in range(0,rect.h):
                for x in range(0,rect.w):
                    tx,ty = x+rect.x,y+rect.y
                    if tx >= 0 and tx < w and ty >= 0 and ty < h: layer[ty][tx] = v[n]
        
    def copy(self,rect):
        data = [[[None for x in range(0,rect.w)] for y in range(0,rect.h)] for l in range(0,4)] 

        lvl = self.level
        w,h = lvl.size
        
        for layer,n in [ (lvl.tlayer,0), (lvl.blayer,1), (lvl.clayer,2) ]:
            for y in range(0,rect.h):
                for x in range(0,rect.w):
                    tx,ty = x+rect.x,y+rect.y
                    if tx >= 0 and tx < w and ty >= 0 and ty < h: data[n][y][x] = layer[ty][tx]
        return data
                
    def paste(self,rect,data):
        lvl = self.level
        w,h = lvl.size
        
        for layer,n in [ (lvl.tlayer,0), (lvl.blayer,1), (lvl.clayer,2) ]:
            for y in range(0,rect.h):
                for x in range(0,rect.w):
                    tx,ty = x+rect.x,y+rect.y
                    v = data[n][y][x]
                    if v != None and tx >= 0 and tx < w and ty >= 0 and ty < h: layer[ty][tx] = v
        
        
    def archive(self):
        if not len(self.changes): return
        
        self.dirty = 1
        h = self.history
        if len(h) >= 32:
            del h[0]
        #c = pygame.Surface((self.view_w,self.view_h),SWSURFACE,self.view)
        #c.fill((0,0,0,0))
        #c.blit(self.view,(0,0))
        
        lvl = self.level
        #ox,oy = lvl.screen_to_tile((0,0))
        #bx,by = lvl.screen_to_tile((self.vdraw.rect.w,self.vdraw.rect.h))
        
        #rect = pygame.Rect(ox,oy,bx-ox,by-oy)
        #print self.modrect
        
        h.append(self.changes)
        self.changes = []
        
    def undo(self):
        if len(self.changes): self.archive()
            
        if len(self.history) == 0: return
        
        self.dirty = 1
        changes = self.history.pop()
        
        changes.reverse()
        for rect,data in changes:
            self.paste(rect,data)
            
        self.vdraw.repaint()
        self.tpicker.repaint() #huh?
        
        self.changes = []
        return
        
        self.level.fill((0,0,0,0),(off[0],off[1],self.view_w,self.view_h))
        self.level.blit(c,off)
        self.vdraw.repaint()
        self.tpicker.repaint()
        
    def __setattr__(self,k,v):
        self.__dict__[k] = v
        
        if k == 'view':
            if hasattr(self,'vdraw'): self.vdraw.repaint()
        
        if k == 'tile':
            if hasattr(self,'tpicker'): self.tpicker.repaint()
                
        if k == 'code':
            if hasattr(self,'cpicker'): self.cpicker.repaint()
        
            
    def event(self,e):
        if e.type is KEYDOWN:
            for key,cmd,value in keys:
                if e.key == key:
                    cmd(value)
                    return
        return gui.Container.event(self,e)
    

def hex_image(self):
    if not hasattr(self,'tiles_w'): self.tiles_w = 256
    if not hasattr(self,'tiles_h'): self.tiles_h = 256
    rimg = pygame.Surface((self.tiles_w,self.tiles_h)).convert_alpha()
    rimg.fill((0,0,0,0))
    w,h = self.tiles_w / self.tile_w, self.tiles_h / self.tile_h
    n = 0
    fnt = pygame.font.SysFont("helvetica",self.tile_h-1)
    for y in range(0,h):
        for x in range(0,w):
            n = x+y*w
            if n != 0:
                xx,yy = x*self.tile_w,y*self.tile_h
                img = fnt.render("%02X"%n,0,(0,0,0))
                img = pygame.transform.scale(img,(self.tile_w-1,self.tile_h-1))
                rimg.blit(img,(xx+1,yy+1))
                img = fnt.render("%02X"%n,0,(255,255,255))
                img = pygame.transform.scale(img,(self.tile_w-1,self.tile_h-1))
                rimg.blit(img,(xx,yy))
    return rimg


class tpicker(gui.Widget):
    def __init__(self):
        gui.Widget.__init__(self)
        self.style.width = app.tiles_w
        self.style.height = app.tiles_h
        
    def paint(self,s):
        s.fill((128,128,128))
        s.blit(app.tiles,(0,0))
        w = app.tiles_w/app.tile_w
        x,y = app.tile%w,app.tile/w
        off = x*app.tile_w,y*app.tile_h
        pygame.draw.rect(s,(255,255,255),(off[0],off[1],app.tile_w,app.tile_h),2)
        
    def event(self,e):
        if (e.type is MOUSEBUTTONDOWN and e.button == 1) or (e.type is MOUSEMOTION and e.buttons[0] == 1 and self.container.myfocus == self):
            w = app.tiles_w/app.tile_w
            x,y = e.pos[0]/app.tile_w,e.pos[1]/app.tile_h
            n = x+y*w
            self.set(n)
            if app.mode not in ('tile','bkgr'):
                app.tools['tile'].click()
    
    def set(self,n):
        if n < 0 or n >= len(app.level.tiles) or app.level.tiles[n] == None: return
        app.tile = n


class cpicker(gui.Widget):
    def __init__(self):
        gui.Widget.__init__(self)
        self.style.width = app.codes_w
        self.style.height = app.codes_h
        
    def paint(self,s):
        s.fill((128,128,128))
        s.blit(app.codes,(0,0))
        w = app.codes_w/app.tile_w
        x,y = app.code%w,app.code/w
        off = x*app.tile_w,y*app.tile_h
        pygame.draw.rect(s,(255,255,255),(off[0],off[1],app.tile_w,app.tile_h),2)
        
    def event(self,e):
        if (e.type is MOUSEBUTTONDOWN and e.button == 1) or (e.type is MOUSEMOTION and e.buttons[0] == 1 and self.container.myfocus == self):
            w = app.codes_w/app.tile_w
            x,y = e.pos[0]/app.tile_w,e.pos[1]/app.tile_h
            n = x+y*w
            self.set(n)
            app.tools['code'].click()
    
    def set(self,n):
        if n < 0 or n >= len(app.level.codes) or app.level.codes[n] == None: return
        app.code = n



class vwrap(gui.Table):
    def __init__(self,**params):
        gui.Table.__init__(self,**params)
        self.style.width = app.view_w #* app.tile_w
        self.style.height = app.view_h #* app.tile_h
        w,h = self.rect.w,self.rect.h = self.style.width,self.style.height
        
        sw = 16
        
        self.vdraw = e = vdraw(width=w-sw,height=h-sw)
        self.add(e,0,0)
        
        rect = pygame.Rect(0,0,app.level.size[0],app.level.size[1])
        tcorners = [rect.topleft,rect.topright,rect.bottomright,rect.bottomleft] 
        corners = [app.level.tile_to_view(tcorners[n]) for n in range(0,4)]
        
        minx,miny,maxx,maxy = 0xffff,0xffff,-0xffff,-0xffff
        for x,y in corners:
            minx,miny,maxx,maxy = min(minx,x),min(miny,y),max(maxx,x),max(maxy,y)

        minx -= w/2
        maxx -= w/2
        miny -= h/2
        maxy -= h/2
        
        self.vs = e = gui.VSlider(0,miny,maxy,sw*4,width=sw,height=h-sw)
        self.add(e,1,0)
        e.connect(gui.CHANGE,self.move_y,e)
        
        self.hs = e = gui.HSlider(0,minx,maxx,sw*4,width=w-sw,height=sw)
        self.add(e,0,1)
        e.connect(gui.CHANGE,self.move_x,e)
        
    def move_x(self,value):
        v = value.value
        if app.level.view.x != v:
            app.level.view.x = v
            app.vdraw.repaint()
    
    def move_y(self,value):
        v = value.value
        if app.level.view.y != v:
            app.level.view.y = v
            app.vdraw.repaint()
        
    def adjust(self):
        self.vs.value = app.level.view.y
        self.hs.value = app.level.view.x
        

class vdraw(gui.Widget):
    def repaint(self):
        self.container.adjust()
        gui.Widget.repaint(self)
        
    def __init__(self,**params):
        gui.Widget.__init__(self,**params)
        #self.style.width = app.view_w #* app.tile_w
        #self.style.height = app.view_h #* app.tile_h
        self.rect.w,self.rect.h = self.style.width,self.style.height
        
        s = pygame.Surface((self.rect.w,self.rect.h))
        clrs = [(148,148,148),(108,108,108)]
        inc = 7
        for y in range(0,self.rect.w/inc):
            for x in range(0,self.rect.h/inc):
                s.fill(clrs[(x+y)%2],(x*inc,y*inc,inc,inc))
        self.bg = s

        s = pygame.Surface((self.rect.w,self.rect.h)).convert_alpha()
        s.fill((0,0,0,0))
        for x in range(0,app.view_w):
            pygame.draw.line(s,(0,0,0),(self.rect.w*x/app.view_w,0),(self.rect.w*x/app.view_w,self.rect.h))
        for y in range(0,app.view_h):
            pygame.draw.line(s,(0,0,0),(0,self.rect.h*y/app.view_h),(self.rect.w,self.rect.h*y/app.view_h))
        self.grid = s
        
        self.pos = 0,0

        
    def paint(self,s):
        #print s
        #print s.get_width(),s.get_height(),s.get_clip()
        #s.blit(self.bg,(0,0))
        s.fill((128,128,128))

        #make sure to clamp the bounds
        if app.level.bounds != None:
            app.level.view.clamp_ip(app.level.bounds)
        
        #draw border        
        rect = pygame.Rect(0,0,app.level.size[0],app.level.size[1])
        tcorners = [rect.topleft,rect.topright,rect.bottomright,rect.bottomleft]
        corners = [app.level.tile_to_screen(tcorners[n]) for n in range(0,4)]
        pygame.draw.lines(s,(255,255,0),1,corners,2)

        
        #s.fill((0,0,0))
        #0/0
        app.level.paint(s)
        
        tmp_tiles = app.level.tiles
        tmp_tlayer = app.level.tlayer
        tmp_blayer = app.level.blayer
        
        app.level.tiles = app.level.codes
        app.level.tlayer = app.level.clayer
        app.level.blayer = None
        
        app.level.paint(s)
        
        app.level.tiles = tmp_tiles
        app.level.tlayer = tmp_tlayer
        app.level.blayer = tmp_blayer
        
        rect = pygame.Rect(self.pos[0],self.pos[1],1,1)
        tcorners = [rect.topleft,rect.topright,rect.bottomright,rect.bottomleft]
        corners = [app.level.tile_to_screen(tcorners[n]) for n in range(0,4)]
        pygame.draw.lines(s,(196,196,196),1,corners,2)

        rect = pygame.Rect(app.select.x,app.select.y,app.select.w,app.select.h) 
        tcorners = [rect.topleft,rect.topright,rect.bottomright,rect.bottomleft]
        corners = [app.level.tile_to_screen(tcorners[n]) for n in range(0,4)]
        pygame.draw.lines(s,(255,255,255),1,corners,2)


                
        
        #s.blit(self.grid,(0,0))
        #r = app.select
        #pygame.draw.rect(s,(255,255,255,128),Rect(r.x*self.rect.w/app.view_w,r.y*self.rect.h/app.view_h,r.w*self.rect.w/app.view_w,r.h*self.rect.h/app.view_h),4)
        
    def event(self,e):
        if e.type is MOUSEMOTION:
            self.getpos(e)
        if (e.type is MOUSEBUTTONDOWN and e.button == 3) or (e.type is MOUSEMOTION and e.buttons[2]==1 and self.container.myfocus == self):
            self.picker_down(e)
        if e.type is MOUSEBUTTONDOWN and e.button == 1:
            self.getpos(e)
            a = '%s_down'%app.mode
            if hasattr(self,a): getattr(self,a)(e)
        if e.type is MOUSEMOTION and e.buttons[0] and self.container.myfocus == self:
            a = '%s_drag'%app.mode
            if hasattr(self,a): getattr(self,a)(e)
        if e.type is MOUSEBUTTONUP and e.button == 1:
            a = '%s_up'%app.mode
            if hasattr(self,a): getattr(self,a)(e)
        if e.type is MOUSEBUTTONDOWN and e.button == 2:
            self.move_down(e)
        if e.type is MOUSEMOTION and e.buttons[1] and self.container.myfocus == self:
            self.move_drag(e)
    
    #move
    def move_down(self,e):
        self.moff = app.level.view.x,app.level.view.y
        self.m1 = e.pos
        
    def move_drag(self,e):
        m1 = self.m1
        m2 = e.pos
        #app.view = app.level.subsurface((x,y,app.view_w,app.view_h))
        app.level.view.x,app.level.view.y = self.moff[0] + m1[0]-m2[0], self.moff[1]+m1[1]-m2[1]
        self.repaint()
            
    #picker
    def picker_down(self,e):
        pos = self.getpos(e)
        #tx,ty = app.level.screen_to_tile(e.pos)
        #r,g,b,a = app.view.get_at(pos)
        if pos == None: return 
        tx,ty = pos
        
        if app.mode == 'tile':
            app.tile = app.level.tlayer[ty][tx]
        if app.mode == 'bkgr':
            app.tile = app.level.blayer[ty][tx]
        app.code = app.level.clayer[ty][tx]
        
    
    
    #tile
    def tile_down(self,e):
        app.archive()
        self.tile_drag(e)
    
    def tile_drag(self,e):
        pos = self.getpos(e)
        #r,g,b,a = app.view.get_at(pos)
        #r = app.tile
        #app.view.set_at(pos,(r,g,b))
        
        if pos == None: return
        tx,ty = pos
        app.mod(pygame.Rect(tx,ty,1,1))
        app.level.tlayer[ty][tx] = app.tile
        self.repaint()
        
    #bkgr
    def bkgr_down(self,e):
        app.archive()
        self.bkgr_drag(e)
    
    def bkgr_drag(self,e):
        pos = self.getpos(e)
        #r,g,b,a = app.view.get_at(pos)
        #g = app.tile
        #app.view.set_at(pos,(r,g,b))
        if pos == None: return
        tx,ty = pos
        app.mod(pygame.Rect(tx,ty,1,1))
        app.level.blayer[ty][tx] = app.tile
        self.repaint()
        
        
    #code
    def code_down(self,e):
        app.archive()
        self.code_drag(e)
    
    def code_drag(self,e):
        pos = self.getpos(e)
        #r,g,b,a = app.view.get_at(pos)
        #b = app.code
        #app.view.set_at(pos,(r,g,b))
        if pos == None: return
        tx,ty =  pos
        app.mod(pygame.Rect(tx,ty,1,1))
        app.level.clayer[ty][tx] = app.code
        self.repaint()
        
    #eraser
    def eraser_down(self,e):
        app.archive()
        self.eraser_drag(e)
    
    def eraser_drag(self,e):
        pos = self.getpos(e)
        if pos == None: return
        tx,ty = pos
        app.mod(pygame.Rect(tx,ty,1,1))
        app.level.tlayer[ty][tx] = 0
        app.level.blayer[ty][tx] = 0
        app.level.clayer[ty][tx] = 0
        #app.view.set_at(pos,(0,0,0))
        self.repaint()
        
    def getpos(self,e):
        tx,ty = app.level.screen_to_tile(e.pos)
        
        if tx < 0 or ty < 0 or tx >= app.level.size[0] or ty >= app.level.size[1]: return None
        
        if (tx,ty) != self.pos:
            self.pos = tx,ty
            self.repaint()
        return tx,ty
        
        x,y = e.pos[0]/app.tile_w,e.pos[1]/app.tile_h
        x = min(max(0,x),app.view_w-1)
        y = min(max(0,y),app.view_h-1)
        return x,y
    
    def getpos2(self,e):
        tx,ty = app.level.screen_to_tile(e.pos)
        
        return tx+1,ty+1
        
        w = app.tile_w
        h = app.tile_h
        x,y = (e.pos[0]+w/2)/app.tile_w,(e.pos[1]+h/2)/app.tile_h
        x = min(max(0,x),app.view_w)
        y = min(max(0,y),app.view_h)
        return x,y
    
    #select
    def select_down(self,e):
        pos = self.getpos2(e)
        pos = pos[0]-1,pos[1]-1
        app.select = Rect(pos[0],pos[1],1,1)
        self.repaint()
        
    def select_drag(self,e):
        pos = self.getpos2(e)
        app.select = Rect(app.select.x,app.select.y,pos[0]-app.select.x,pos[1]-app.select.y)
        app.select.w = max(1,app.select.w)
        app.select.h = max(1,app.select.h)

        self.repaint()
        

def cmd_all(value):
    app.select = Rect(0,0,app.level.size[0],app.level.size[1])
    app.vdraw.repaint()
    
    #print 'deprecated in v0.5'
    
def cmd_shrink(value):    
    if app.select.w <= 2 or app.select.h <= 2: return
    app.select.x += 1
    app.select.y += 1
    app.select.w -= 2
    app.select.h -= 2

def cmd_undo(value):
    app.undo()
    
def cmd_redo(value):
    pass
    
def cmd_copy(value):
    #next version of pygame?
    #app.clipboard = app.tile.subsurface(app.select).copy()
    
    data = app.copy(app.select)
    app.clipboard = pygame.Rect(app.select),data
    return
    
    #s = app.view.subsurface(app.select)
    #app.clipboard = pygame.Surface((app.select.w,app.select.h),SWSURFACE,s)
    #app.clipboard.fill((0,0,0,0))
    #app.clipboard.blit(s,(0,0))
    
    print app.clipboard.get_at((0,0))
    
def cmd_paste(value):
    if app.clipboard != None:
        app.archive()
        #app.view.fill((0,0,0,0),(app.select[0],app.select[1],app.clipboard.get_width(),app.clipboard.get_height()))
        #app.view.blit(app.clipboard,app.select)
        #app.vdraw.repaint()
        
        rect,data = app.clipboard
        rect = pygame.Rect(app.select.x,app.select.y,rect.w,rect.h)
        
        app.mod(rect)
        app.paste(rect,data)
        app.vdraw.repaint()

class Restart(Exception):
    pass
    
def _dirty(fnc,v):
    dialog = DirtyDialog()
    def onchange(value):
        value.close()
        return fnc(v)
    dialog.connect(gui.CHANGE,onchange,dialog)
    dialog.open()

def cmd_new(value):
    if app.dirty: _dirty(_cmd_new,value)
    else: _cmd_new(value)
    
def _cmd_new(value):
    dialog = NewDialog()
    
    def onchange(value):
        value.close()
        vv = value.value
        ok = 0
        try:        
            width,height,tile_w,tile_h,codes,tiles,klass = int(vv['width'].value),int(vv['height'].value),int(vv['tile_w'].value),int(vv['tile_h'].value),vv['codes'].value,vv['tiles'].value,vv['class'].value
            global cfg
            cfg['fname'] = None
            cfg['width'] = width
            cfg['height'] = height
            cfg['tile_w'] = tile_w
            cfg['tile_h'] = tile_h
            cfg['codes'] = codes
            cfg['tiles'] = tiles
            cfg['class'] = klass
            ok = 1
        except Exception, v:
            ErrorDialog("New failed.",v).open()
        if ok:
            raise Restart()
    
    dialog.connect(gui.CHANGE,onchange,dialog)
    dialog.open()

    
def cmd_open(value):
    if app.dirty: _dirty(_cmd_open,value)
    else: _cmd_open(value)

def _cmd_open(value):
    dialog = OpenDialog()
    
    def onchange(value):
        value.close()
        vv = value.value
        ok = 0
        
        try:        
            
            fname,tile_w,tile_h,codes,tiles,klass = vv['fname'].value,int(vv['tile_w'].value),int(vv['tile_h'].value),vv['codes'].value,vv['tiles'].value,vv['class'].value
            global cfg
            cfg['fname'] = fname
            cfg['tile_w'] = tile_w
            cfg['tile_h'] = tile_h
            cfg['codes'] = codes
            cfg['tiles'] = tiles
            cfg['class'] = klass

            
            ok = 1
        except Exception,v:
            ErrorDialog("Open failed.",v).open()
            
        if ok: raise Restart()

    
    dialog.connect(gui.CHANGE,onchange,dialog)
    dialog.open()

def cmd_saveas(value):
    dialog = SaveAsDialog()
    
    def onchange(value):
        value.close()
        vv = value.value
        fname = vv['fname'].value
        if len(fname) == 0:
            ErrorDialog("Save As failed.","File Name too short!").open()
            return
        global cfg
        app.fname = cfg['fname'] = fname
        return cmd_save(None)
        
    dialog.connect(gui.CHANGE,onchange,dialog)
    dialog.open()
        
def cmd_cut(value):
    cmd_copy(value)
    cmd_delete(value)

def cmd_fullscreen(value):
    pygame.display.toggle_fullscreen()
    
def cmd_delete(value):
    app.archive()
    #app.view.fill((0,0,0,0),app.select)
    app.mod(app.select)
    app.fill(app.select,(0,0,0,0))
    app.vdraw.repaint()
        
#NOTE: this function is a temporary HACK, to be replaced
#with layer editing in the future, maybe.
def cmd_tswitch(value):
    blayer = app.level.blayer
    tlayer = app.level.tlayer
    for ty in xrange(0,app.level.size[1]):
        for tx in xrange(0,app.level.size[0]):
            tmp = blayer[ty][tx]
            blayer[ty][tx] = tlayer[ty][tx]
            tlayer[ty][tx] = tmp
    app.vdraw.repaint()
    

def cmd_fill(value):
    pass

def cmd_pick(value):
    dx,dy = value
    
    mods = pygame.key.get_mods()
    
    
    if (mods&KMOD_SHIFT) != 0:
        app.level.view.x += dx*app.vdraw.rect.w/8
        app.level.view.y += dy*app.vdraw.rect.h/8
        app.vdraw.repaint()
        #x,y = app.view.get_offset()
        #x = x + 1*dx
        #y = y + 1*dy
        #x = min(max(x,0),app.level_w-app.view_w)
        #y = min(max(y,0),app.level_h-app.view_h)
        #app.view = app.level.subsurface((x,y,app.view_w,app.view_h))
        
    elif (mods&KMOD_CTRL) != 0:
        app.level.view.x += dx*app.vdraw.rect.w
        app.level.view.y += dy*app.vdraw.rect.h
        app.vdraw.repaint()
        #x,y = app.view.get_offset()
        #x = x + app.view_w*dx
        #y = y + app.view_h*dy
        #x = min(max(x,0),app.level_w-app.view_w)
        #y = min(max(y,0),app.level_h-app.view_h)
        #app.view = app.level.subsurface((x,y,app.view_w,app.view_h))
        
    
    else:
        w = app.tiles_w/app.tile_w
        if app.mode == 'code':
            n = app.code + dx + dy*w
            app.cpicker.set(n)
        else:
            n = app.tile + dx + dy*w
            app.tpicker.set(n)
        
def cmd_mode(value):
    mode = value
    app.mode = mode

def cmd_load(value):
    if app.dirty: _dirty(_cmd_load,value)
    else: _cmd_load(value)

def _cmd_load(value):
    if app.fname == None:
        ErrorDialog("Load failed","Image is untitled.").open()
        return
    raise Restart()

    
def cmd_save(value):
    if app.fname == None:
        return cmd_saveas(value)
    try:
        app.level.tga_save_level(app.fname)
        cfg_to_ini(['class','codes','tiles','tile_w','tile_h'],app.fname)
        ini_save()
        app.dirty = 0
    except Exception, v:
        ErrorDialog("Save failed.",v).open()
        return

    
import os
def cmd_preview(value):
    app.level.tga_save_level("_preview.tga")
    cmd = "python preview.py _preview.tga"
    print cmd
    os.system(cmd)
    
def cmd_quit(value):
    if app.dirty: _dirty(_cmd_quit,value)
    else: _cmd_quit(value)

def _cmd_quit(value):
    app.top.quit()    
    
def cmd_refreshtiles(value):
    app.load_tiles_and_codes()




menus = [
    ('File/New',cmd_new,None),
    ('File/Open',cmd_open,None),
    ('File/Save',cmd_save,None),
    ('File/Save As',cmd_saveas,None),
    ('File/Reload',cmd_load,None),
    ('File/Preview',cmd_preview,None),
    ('File/Quit',cmd_quit,None),

    ('Edit/Undo',cmd_undo,None),
    ('Edit/Cut',cmd_cut,None),
    ('Edit/Copy',cmd_copy,None),
    ('Edit/Paste',cmd_paste,None),
    ('Edit/Delete',cmd_delete,None),
    ('Edit/Select All',cmd_all,None),
    ('Edit/Shrink',cmd_shrink,None),
    #('Edit/Redo',None,None,None),
    #('Edit/Cut',None,None,None),
    #('Edit/Fill',cmd_fill,None),
    
    ]

keys = [
    (K_s,cmd_save,None),
    (K_d,cmd_load,None),
    (K_p,cmd_preview,None),

    (K_a,cmd_all,None),
    (K_z,cmd_undo,None),
    #('Edit/Redo',None,None,None),
    (K_x,cmd_cut,None),
    (K_c,cmd_copy,None),
    (K_v,cmd_paste,None),
    #('Edit/Cut',None,None,None),
    (K_DELETE,cmd_delete,None),
    #(K_f,cmd_fill,None),
        
        (K_t,cmd_tswitch,None),
    
    (K_F10,cmd_fullscreen,None),
    
    (K_UP,cmd_pick,(0,-1)),
    (K_DOWN,cmd_pick,(0,1)),
    (K_LEFT,cmd_pick,(-1,0)),
    (K_RIGHT,cmd_pick,(1,0)),
    ]
    

tools = [
    ('tile','tile'),
    ('bkgr','bkgr'),
    ('code','code'),
    ('select','select'),
    ('eraser','eraser'),
    ]

    
    

class NewDialog(gui.Dialog):
    def __init__(self,**params):
        title = gui.Label("New...")
        
        doc = html.HTML(globals={'gui':gui,'dialog':self},data="""
<form id='form'>

<table>

<tr><td colspan=2>

<table>
<tr><td>Level<br>Type:
<td align=left><input type=radio name='class' value='pgu.tilevid.Tilevid' checked> Tile<br>
<input type=radio name='class' value='pgu.isovid.Isovid'> Isometric<br>
<input type=radio name='class' value='pgu.hexvid.Hexvid'> Hexoganol

<tr><td >Tiles: <td><input type='text' size=20 name='tiles' value='%(tiles)s'>
<tr><td>Codes: <td><input type='text' size=20 name='codes' value='%(codes)s'>
</table>

<tr>
<td align=center>Level Size
<td align=center>Tile Size


<tr><td colspan='1' align='center' style='padding-right:8px;'>
<table>
<tr><td align=right>Width: <td><input type='text' size='4' value='%(width)s' name='width'>
<tr><td align=right>Height: <td><input type='text' size='4' value='%(height)s' name='height'>
</table>

<td colspan='1' align='center'>
<table>
<tr><td align=right>Width: <td><input type='text' size='4' value='%(tile_w)s' name='tile_w'>
<tr><td align=right>Height: <td><input type='text' size='4' value='%(tile_h)s' name='tile_h'>
</table>

<tr><td>&nbsp;

<tr><td colspan=2><input type='button' value='Okay' onclick='dialog.send(gui.CHANGE)'> <input type='button' value='Cancel' onclick='dialog.close()'>

</table>"""%ini_to_dict('None'))
        gui.Dialog.__init__(self,title,doc)
        
        self.value = doc['form']

class SaveAsDialog(gui.Dialog):
    def __init__(self,**params):
        title = gui.Label("Save As...")
        
        doc = html.HTML(globals={'gui':gui,'dialog':self},data="""
<form id='form'>

<table>

<tr><td colspan=2>File Name: <input type='file' size=20 name='fname' value=''>

<tr><td>&nbsp;

<tr><td colspan=2><input type='button' value='Okay' onclick='dialog.send(gui.CHANGE)'> <input type='button' value='Cancel' onclick='dialog.close()'>

</table>""")
        gui.Dialog.__init__(self,title,doc)
        
        self.value = doc['form']

class OpenDialog(gui.Dialog):
    def __init__(self,**params):
        title = gui.Label("Open...")
        
        def load_vals(fname,form):
            if not ini.has_section(fname): return
            
            for k,v in ini.items(fname):
                if k in form:
                    form[k].value = v

        doc = html.HTML(globals={'load_vals':load_vals,'ini':ini,'gui':gui,'dialog':self},data="""<form id='form'><table>
        
        <tr><td align=right>File Name:&nbsp;<td  align=left><input type='file' size=20 name='fname' value='' onchange='load_vals(self.value,form)'>

        <tr><td align=right>Level&nbsp;<br>Type:&nbsp;
        <td align=left><input type=radio name='class' value='pgu.tilevid.Tilevid' checked> Tile<br><input type=radio name='class' value='pgu.isovid.Isovid'> Isometric<br><input type=radio name='class' value='pgu.hexvid.Hexvid'> Hexoganol
        
        <tr><td align=right>Tiles:&nbsp;<td align=left><input type='text' size=20 name='tiles' value='%(tiles)s'>
        <tr><td align=right>Codes:&nbsp;<td align=left><input type='text' size=20 name='codes' value='%(codes)s'>
        
        <tr><td align=right>Tile Width:&nbsp;<td align=left><input type='text' size='4' value='%(tile_w)s' name='tile_w'>
        <tr><td align=right>Tile Height:&nbsp;<td align=left><input type='text' size='4' value='%(tile_h)s' name='tile_h'>


<tr><td>&nbsp;

<tr><td colspan=2><input type='button' value='Okay' onclick='dialog.send(gui.CHANGE)'> <input type='button' value='Cancel' onclick='dialog.close()'>

</table>"""%ini_to_dict('None'))
        gui.Dialog.__init__(self,title,doc)
        
        self.value = doc['form']

class ErrorDialog(gui.Dialog):
    def __init__(self,tt,data,**params):
        title = gui.Label("Error: "+tt)
        data = str(data)
        
        doc = html.HTML(globals={'gui':gui,'dialog':self},data="""
<form id='form'>

<table>
<tr><td><h1>&lt;!&gt;&nbsp;</h1>
<td>"""+data+"""
<tr><td>&nbsp;
<tr><td colspan=2><input type='button' value='Okay' onclick='dialog.send(gui.CHANGE);dialog.close()'>
</table>""")
        gui.Dialog.__init__(self,title,doc)
        
        self.value = doc['form']

class DirtyDialog(gui.Dialog):
    def __init__(self,**params):
        title = gui.Label("File not yet saved...")
        data = "Your file is not yet saved.<br>Are you sure you want to continue?"
        
        doc = html.HTML(globals={'gui':gui,'dialog':self},data="""
<form id='form'>

<table>
<tr><td><h1>&lt;!&gt;&nbsp;</h1>
<td>"""+data+"""
<tr><td>&nbsp;
<tr><td colspan=2><input type='button' value='Okay' onclick='dialog.send(gui.CHANGE)'> <input type='button' value='Cancel' onclick='dialog.close()'>
</table>""")
        gui.Dialog.__init__(self,title,doc)
        
        self.value = doc['form']


    
        
def init_ini():
    ini.read([ini_fname])

def ini_save():
    f = open(ini_fname,"wb")
    ini.write(f)
    f.close()


def init_opts():
    ini.read([ini_fname])
    
    usage = "usage: %prog level.tga [tiles.tga] [codes.tga] [tile_w] [tile_h]"
    
    parser = OptionParser(usage)
    
    parser.add_option("-t", "--tiles", dest="tiles",
        help="filename of the tiles image (level)")
    parser.add_option("-c", "--codes", dest="codes",
        help="file name of the codes image (level)")

    parser.add_option("--tw", dest="tile_w", help="tile width (level)", type='int')
    parser.add_option("--th", dest="tile_h", help="tile height (level)", type='int')

    parser.add_option("--vw", dest="view_w", help="view width (level)", type='int')
    parser.add_option("--vh", dest="view_h", help="view height (level)", type='int')
        
    parser.add_option("--sw", dest="screen_w", help="screen width (app)", type='int')
    parser.add_option("--sh", dest="screen_h", help="screen height (app)", type='int')
    parser.add_option("--class",dest="class",help="class (e.g. pgu.tilevid.Tilevid) (level)")
    parser.add_option("--tile",action="store_const",const="pgu.tilevid.Tilevid",dest="class",help="use pgu.tilevid.Tilevid")
    parser.add_option("--iso",action="store_const",const="pgu.isovid.Isovid",dest="class",help="use pgu.isovid.Isovid")
    parser.add_option("--hex",action="store_const",const="pgu.hexvid.Hexvid",dest="class",help="use pgu.hexvid.Hexvid")
    
    parser.add_option("--width",dest="width",help="new width (level)",type='int')
    parser.add_option("--height",dest="height",help="new height (level)",type='int')

    parser.add_option("-d","--defaults",dest="defaults",help="set default settings (image)",action="store_true")

    #parser.add_option("-a", "--app", dest="app",
    #    help="set application level defaults", action="store_true")
    
    (opts, args) = parser.parse_args()
    
    if len(args) not in (0,1,2,3,4,5):
        parser.error("incorrect number of arguments")
    
    #parse arguments
    if len(args) == 0:
        opts.fname = "None"
    if len(args) > 0:
        opts.fname = args[0]
    if len(args) > 1:
        opts.tiles = args[1]
    if len(args) in (3,5):
        opts.codes = args[2]
    if len(args) in (4,5):
        n = len(args)-2
        try: opts.tile_w,opts.tile_h = int(args[n]),int(args[n+1])
        except: parser.error("width and height must be integers")
        if opts.tile_w < 1 or opts.tile_h < 1: parser.error("width and height must be greater than 0")
        
    fname = opts.fname
    
    #create all sections
    for k in [fname,"None","app"]:
        if not ini.has_section(k):
            ini.add_section(k)
    
    #set app level defaults
    for k,v in [('screen_w',800),('screen_h',600)]:
        if not ini.has_option('app',k):
            ini.set('app',k,str(v))
    
    #set app level values
    for k in ['screen_w','screen_h']:
        if hasattr(opts,k):
            v = getattr(opts,k)
            if v != None: ini.set('app',k,str(v))

    #set default defaults
    for k,v in [('width',40),('height',30),('tile_w',32),('tile_h',32),('tiles','tiles.tga'),('codes','codes.tga'),('class','pgu.tilevid.Tilevid')]:
        if not ini.has_option('None',k):
            ini.set('None',k,str(v))
    
    #name of keys for normal stuff
    file_ks = ['class','tiles','codes','width','height','tile_w','tile_h']
            
    #set default values
    if opts.defaults:
        for k in file_ks:
            if hasattr(opts,k):
                v = getattr(opts,k)
                if v != None: ini.set('None',k,str(v))
    
    #set fname values
    for k in file_ks:
        if hasattr(opts,k):
            v = getattr(opts,k)
            if v != None: ini.set(fname,k,str(v))
    
    #save the ini
    ini_save()
            
    #convert ini to cfg stuff...
    ini_to_cfg(['app','None',fname])
    if fname == 'None': fname = None
    cfg['fname'] = fname

def ini_to_cfg(sections):
    global cfg
    ik = ['screen_w','screen_h','tile_w','tile_h','width','height']
    for s in sections:
        for k,v in ini.items(s):
            if k in ik: v = int(v)
            cfg[k] = v

def ini_to_dict(section):
    cfg = {}
    ik = ['screen_w','screen_h','tile_w','tile_h','width','height']
    for s in [section]:
        for k,v in ini.items(s):
            if k in ik: v = int(v)
            cfg[k] = v
    return cfg

def cfg_to_ini(ks,section):
    if not ini.has_section(section): ini.add_section(section)
    for k in ks:
        v = cfg[k]
        ini.set(section,k,str(v))

        
def init_gui():
    #themes = cfg['theme'].split(",")
#    themes2 = []
#    for t in themes:
#        if t[0] == "/" or t[0] == ".": themes2.append(t)
#        else: themes2.append(dname+"/"+t)
    #gui.theme.load(themes)
    #gui.theme.load(['default','tools'])
    global top
    top = gui.Desktop(theme=gui.Theme(['default','tools']))
    #top.theme.load(['default','tools'])


    pass

def init_app():
    global app
    app = _app()
    
    #
    ss = 8
        
    #--- top
    x,y,h = 0,0,0
        
    #menus
    e = gui.Menus(menus)
    e.rect.w,e.rect.h = e.resize()
    app.add(e,x,y)
    x,h = x+e.rect.w,max(h,e.rect.h)
    menus_height = e.rect.h
        
    #--- row
    x,y,h = 0,y+h,0
    
    #--- vspace
    y += ss
    
    #--- hspace
    x += ss
    
    #tools
    e = gui.Toolbox(tools,1,0,value='tile')#,"icons48")
    e.rect.w,e.rect.h = e.resize()
    def _set_mode(value): cmd_mode(value.value)
    e.connect(gui.CHANGE,_set_mode,e)
    app.add(e,x,y)
    app.tools = e.tools
    x,h = x+e.rect.w,max(h,e.rect.h)
    toolbox_width = e.rect.w
    
    #--- hspace
    x += ss
    
    #vdraw
    dw = app.screen_w - (toolbox_width+app.tiles.get_width()+ss*4)
    dh = app.screen_h - (menus_height+ss*2)
    app.view_init(dw,dh)
    
    
    e = app.vwrap = vwrap()
    app.vdraw = e.vdraw
    e.rect.w,e.rect.h = e.resize()
    app.add(e,x,y)
    x,h = x+e.rect.w,max(h,e.rect.h)
    
    #--- hspace
    x += ss
    
    #tpicker
    e = app.tpicker = tpicker()
    e.rect.w,e.rect.h = e.resize()
    #--- right
    x = app.screen_w-e.rect.w-ss
    app.add(e,x,y)
    x,h = x+e.rect.w,max(h,e.rect.h)
    tpicker_height = e.rect.h
    
    #cpicker
    e = app.cpicker = cpicker()
    e.rect.w,e.rect.h = e.resize()
    #--- right
    x = app.screen_w-e.rect.w-ss
    app.add(e,x,y+tpicker_height+ss)
    x,h = x+e.rect.w,max(h,e.rect.h)
    



    pygame.key.set_repeat(500,30)
    
    app.screen.fill((255,255,255,255))


def run():
    top.connect(gui.QUIT,cmd_quit,None)
    top.connect(pygame.ACTIVEEVENT, cmd_refreshtiles,None)

    top.init(app,app.screen)
    app.top=top
    top.run()

def main():
    init_ini()
    init_opts()
    init_gui()
    
    restart = 1
    while restart:
        restart = 0
        try:
            init_app()
            run()
        except Restart: restart = 1

main()
# vim: set filetype=python sts=4 sw=4 noet si :
