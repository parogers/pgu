"""Hexagonal tile engine.

Note -- this engine is not finished.  Sprites are not supported.  It
can still be useful for using the level editor, and for rendering hex
terrains, however.  If you are able to update it and use it in a real game,
help would be greatly appreciated!

Please note that this file is alpha, and is subject to modification in
future versions of pgu!

"""
print 'pgu.hexvid','This module is alpha, and is subject to change.'

from pgu.vid import *
import pygame


class Hexvid(Vid):
    """Create an hex vid engine.  See [[vid]]"""
    def update(self,screen):
        return self.paint(screen)
    
    def paint(self,screen):
        sw,sh = screen.get_width(),screen.get_height()
        self.view.w,self.view.h = sw,sh
        
        tlayer = self.tlayer
        blayer = self.blayer
        #zlayer = self.zlayer
        w,h = len(tlayer[0]),len(tlayer)
        
        #iso_w,iso_h,iso_z,tile_w,tile_h,base_w,base_h = self.iso_w,self.iso_h,self.iso_z,self.tile_w,self.tile_h,self.base_w,self.base_h
        
        tile_w,tile_h = self.tile_w,self.tile_h
        tile_w2,tile_h2 = tile_w/2,tile_h/2
        
        view = self.view
        adj = self.adj = pygame.Rect(-self.view.x,-self.view.y,0,0)
        
        w,h = len(tlayer[0]),len(tlayer)
        tiles = self.tiles
        
        #""
        if self.bounds == None:
            tmp,y1 = self.tile_to_view((0,0))
            x1,tmp = self.tile_to_view((0,h+1))
            tmp,y2 = self.tile_to_view((w+1,h+1))
            x2,tmp = self.tile_to_view((w+1,0))
            self.bounds = pygame.Rect(x1,y1,x2-x1,y2-y1)
            print self.bounds
        #""
        
        if self.bounds != None: self.view.clamp_ip(self.bounds)

        ox,oy = self.screen_to_tile((0,0))
        sx,sy = self.tile_to_view((ox,oy))
        dx,dy = sx - self.view.x,sy - self.view.y
        
        bot = 1
        
        tile_wi = tile_w + tile_w/2
        tile_wi2 = tile_wi/2
        
        #dx += tile_w/2
        
        for i2 in xrange(-bot,self.view.h/tile_h2+bot*3): #NOTE: 3 seems a bit much, but it works.
            tx,ty = ox + i2/2 + i2%2,oy + i2/2
            x,y = (i2%2)*tile_wi2 + dx,i2*tile_h2 + dy
            
            #to adjust for the -1 in i1
            x,tx,ty = x-tile_wi,tx-1,ty+1
            
            x -= tile_w/2
            for i1 in xrange(-1,self.view.w/tile_wi+1):
                if ty >= 0 and ty < h and tx >= 0 and tx < w:
                    if blayer != None:
                        n = blayer[ty][tx]
                        if n != 0:
                            t = tiles[n]
                            if t != None and t.image != None:
                                screen.blit(t.image,(x,y))
                    n = tlayer[ty][tx]
                    if n != 0:
                        t = tiles[n]
                        if t != None and t.image != None:
                            screen.blit(t.image,(x,y))
                            
            
                tx += 1
                ty -= 1
                x += tile_wi 

        return [pygame.Rect(0,0,screen.get_width(),screen.get_height())]
    
    def view_to_tile(self,pos):
        x,y = pos
        #x = x + (self.tile_w*1/2)
        
        x,y = int(x*4/(self.tile_w*3)), y*2/self.tile_h
        nx = (x + y) / 2
        ny = (y - x) / 2
        return nx,ny
    
    def tile_to_view(self,pos):
        x,y = pos
        nx = x - y
        ny = x + y
        nx,ny = int(nx*(self.tile_w*3)/4), ny*self.tile_h/2
        
        #nx = nx - (self.tile_w*1/2)
        return nx,ny
            
    def screen_to_tile(self,pos): #NOTE HACK : not sure if the 3/8 is right or not, but it is pretty close...
        pos = pos[0]+self.view.x + self.tile_w*3/8,pos[1]+self.view.y
        pos = self.view_to_tile(pos)
        return pos
    
    def tile_to_screen(self,pos):
        pos = self.tile_to_view(pos)
        pos = pos[0]-self.view.x,pos[1]-self.view.y
        return pos
    
        
    def tga_load_tiles(self,fname,size,tdata={}):
        Vid.tga_load_tiles(self,fname,size,tdata)
        
        self.tile_w,self.tile_h = size
