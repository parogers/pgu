"""Isometric tile engine.

Note -- this engine is not finished, any may not work for your 
particular needs.  If you are able to update it, help would be 
greatly appreciated!

Please note that this file is alpha, and is subject to modification in
future versions of pgu!

"""
print('pgu.isovid - This module is alpha, and is subject to change.')

from pgu.vid import *
import pygame

# Quick fix for python3
try:
    xrange
except:
    xrange = range

class Isovid(Vid):
    """Create an iso vid engine.  See [[vid]]"""
    def update(self,screen):
        return self.paint(screen)
    
    def paint(self,screen):
        sw,sh = screen.get_width(),screen.get_height()
        
        tlayer = self.tlayer
        blayer = self.blayer
        zlayer = self.zlayer
        w,h = len(tlayer[0]),len(tlayer)
        
        iso_w,iso_h,iso_z,tile_w,tile_h,base_w,base_h = self.iso_w,self.iso_h,self.iso_z,self.tile_w,self.tile_h,self.base_w,self.base_h
        
        base_h2 = base_h/2
        base_w2 = base_w/2
        
        bot = tile_h/base_h2
        todo_max = sh/base_h2+bot
        todo = [[] for y in xrange(0,todo_max)]
        
        self.view.w,self.view.h = sw,sh
        view = self.view
        adj = self.adj = pygame.Rect(-self.view.x,-self.view.y,0,0)
        
        for s in self.sprites:
            self.sprite_calc_irect(s)
            x,y = self.iso_to_view((s.rect.centerx,s.rect.centery))
            v = (y+adj.y)/base_h2 - 1
            if v >= 0 and v < todo_max:
                todo[v].append((s.image,s.irect))
            #else: print 'doesnt fit',v
                
        w,h = len(tlayer[0]),len(tlayer)
        tiles = self.tiles
        
        #""
        if self.bounds == None:
            tmp,y1 = self.tile_to_view((0,0))
            x1,tmp = self.tile_to_view((0,h+1))
            tmp,y2 = self.tile_to_view((w+1,h+1))
            x2,tmp = self.tile_to_view((w+1,0))
            self.bounds = pygame.Rect(x1,y1,x2-x1,y2-y1)
        #""
        
        if self.bounds != None: self.view.clamp_ip(self.bounds)

        ox,oy = self.screen_to_tile((0,0))
        sx,sy = self.iso_to_view((ox*iso_w,oy*iso_h))
        dx,dy = sx - self.view.x,sy - self.view.y
        
        for i2 in xrange(-bot,self.view.h//base_h2+bot):
            tx,ty = ox + i2/2 + i2%2,oy + i2/2
            x,y = (i2%2)*base_w2 + dx,i2*base_h2 + dy
            
            #to adjust for the -1 in i1
            x,tx,ty = x-base_w,tx-1,ty+1
            for i1 in xrange(-1,self.view.w//base_w+2): #NOTE: not sure why +2
                if ty >= 0 and ty < h and tx >= 0 and tx < w:
                    z = zlayer[ty][tx]*iso_z
                    if blayer != None:
                        n = blayer[ty][tx]
                        if n != 0:
                            t = tiles[n]
                            if t != None and t.image != None:
                                screen.blit(t.image,(x-base_w2,y+z))
                    n = tlayer[ty][tx]
                    if n != 0:
                        t = tiles[n]
                        if t != None and t.image != None:
                            screen.blit(t.image,(x-base_w2,y-(t.image_h-base_h)+z))
            
                tx += 1
                ty -= 1
                x += base_w
            for img,irect in todo[y/base_h2]:
                screen.blit(img,(irect.x+adj.x,irect.y+adj.y))

        return [pygame.Rect(0,0,screen.get_width(),screen.get_height())]
        
    def iso_to_view(self,pos):
        tlayer = self.tlayer
        w,h = len(tlayer[0]),len(tlayer)
        
        x,y = pos
        
        #nx,ny = (h*self.iso_w + x - y)/2, (0 + x + y)/2
        nx,ny = (x - y)/2, (0 + x + y)/2
        
        return (nx * self.base_w / self.iso_w), (ny * self.base_h / self.iso_h)

    def view_to_iso(self,pos):
        tlayer = self.tlayer
        w,h = len(tlayer[0]),len(tlayer)
        
        x,y = pos
        
        x,y = x*self.iso_w/self.base_w, y*self.iso_h/self.base_h
        
        #x -= (self.iso_w/2) * h
        #x -= (self.iso_w/2) * h
        
        nx = (x+y) 
        ny = y*2-nx
    
        return nx,ny
    
    def tile_to_view(self,pos):
        return self.iso_to_view((pos[0]*self.iso_w,pos[1]*self.iso_h))
    
    def screen_to_tile(self,pos):
        x,y = pos
        x += self.view.x
        y += self.view.y
        x,y = self.view_to_iso((x,y))
        return x/self.iso_w,y/self.iso_h
        
    def tile_to_screen(self,pos):
        x,y = self.iso_to_view((pos[0]*self.iso_w,pos[1]*self.iso_h))
        return x-self.view.x,y-self.view.y
    
    def tga_load_tiles(self,fname,size,tdata={}):
        Vid.tga_load_tiles(self,fname,size,tdata)
        
        self.tile_w,self.tile_h = size
        self.iso_w,self.iso_h,self.iso_z = self.tile_w,self.tile_w,1
        self.base_w,self.base_h = self.tile_w,self.tile_w/2
    

        
    def resize(self,size,bg=0):
        Vid.resize(self,size,bg)
        
        tlayer = self.tlayer
        w,h = len(tlayer[0]),len(tlayer)
        
        self.zlayer = [[0 for x in xrange(0,w)] for y in xrange(0,h)]

        


    def sprite_calc_irect(self,s):
        tlayer = self.tlayer
        w,h = len(tlayer[0]),len(tlayer)
        zlayer = self.zlayer
        
        x,y = self.iso_to_view((s.rect.centerx,s.rect.centery))
        tx,ty = s.rect.centerx/self.iso_w,s.rect.centery/self.iso_h
        z = 0
        if ty >= 0 and ty < h and tx >= 0 and tx < w:
            z = zlayer[ty][tx]*self.iso_z
        
        nx,ny = x - s.shape.centerx, y - s.shape.centery + z
        
        s.irect.x,s.irect.y = nx,ny
        
    def run_codes(self,cdata,rect):
        #HACK to make run_codes work
        w,h = self.iso_w,self.iso_h
         
        img = self.tiles[0].image
        
        self.tiles[0].image = pygame.Surface((w,h))
        r = Vid.run_codes(self,cdata,rect)
        self.tiles[0].image = img
        return r
