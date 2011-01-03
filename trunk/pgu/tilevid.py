"""Square tile based engine."""

from pgu.vid import *
import pygame

class Tilevid(Vid):
    """Based on [[vid]] -- see for reference."""
    def paint(self,s):
        sw,sh = s.get_width(),s.get_height()
        self.view.w,self.view.h = sw,sh
        
        tiles = self.tiles
        tw,th = tiles[0].image.get_width(),tiles[0].image.get_height()
        w,h = self.size
        
        if self.bounds != None: self.view.clamp_ip(self.bounds)
        
        ox,oy = self.view.x,self.view.y
        tlayer = self.tlayer
        blayer = self.blayer
        alayer = self.alayer
        sprites = self.sprites
        
        blit = s.blit
        yy = - (self.view.y%th) 
        my = (oy+sh)/th
        if (oy+sh)%th: my += 1
        
        if blayer != None:
            for y in xrange(oy/th,my):
                if y >=0 and y < h:
                    trow = tlayer[y]
                    brow = blayer[y]
                    arow = alayer[y]
                    xx= - (self.view.x%tw)
                    mx = (ox+sw)/tw
                    #if (ox+sh)%tw: mx += 1
                    for x in xrange(ox/tw,mx+1):
                        if x >=0and x<w:
                            blit(tiles[brow[x]].image,(xx,yy))
                            blit(tiles[trow[x]].image,(xx,yy))
                            arow[x]=0
                        xx += tw
                yy+=th
        else:
            for y in xrange(oy/th,my):
                if y >=0 and y<h:
                    trow = tlayer[y]
                    arow = alayer[y]
                    xx= - (self.view.x%tw)
                    mx = (ox+sw)/tw
                    #if (ox+sh)%tw: mx += 1
                    for x in xrange(ox/tw,mx+1):
                        if x >=0 and x<w:
                            blit(tiles[trow[x]].image,(xx,yy))
                            arow[x]=0
                        xx += tw
                yy+=th

        for s in sprites:
            s.irect.x = s.rect.x-s.shape.x
            s.irect.y = s.rect.y-s.shape.y
            blit(s.image,(s.irect.x-ox,s.irect.y-oy))
            s.updated=0
            s._irect = Rect(s.irect)
            #s._rect = Rect(s.rect)

        self.updates = []
        self._view = pygame.Rect(self.view)
        return [Rect(0,0,sw,sh)]
        
    def update(self,s):
        sw,sh = s.get_width(),s.get_height()
        self.view.w,self.view.h = sw,sh
        
        if self.bounds != None: self.view.clamp_ip(self.bounds)
        if self.view.x != self._view.x or self.view.y != self._view.y: 
            return self.paint(s)
        
        ox,oy = self.view.x,self.view.y
        sw,sh = s.get_width(),s.get_height()
        w,h = self.size
        tlayer = self.tlayer
        blayer = self.blayer
        alayer = self.alayer
        tiles = self.tiles
        tw,th = tiles[0].image.get_width(),tiles[0].image.get_height()
        sprites = self.sprites
        blit = s.blit
        
        us = []
        
        #mark places where sprites have moved, or been removed
        
        ss = self.sprites.removed
        self.sprites.removed = []
        ss.extend(sprites)
        for s in ss: 
            #figure out what has been updated.
            s.irect.x = s.rect.x-s.shape.x
            s.irect.y = s.rect.y-s.shape.y
            if (s.irect.x != s._irect.x or s.irect.y != s._irect.y
                     or s.image != s._image):
                 #w,h can be skipped, image covers that...
                 s.updated = 1
            if s.updated:
                r = s._irect
                y = max(0,r.y/th)
                yy = min(h,r.bottom/th+1)
                while y < yy:
                    x = max(0,r.x/tw)
                    xx = min(w,r.right/tw+1)
                    while x < xx:
                        if alayer[y][x] == 0:
                            self.updates.append((x,y))
                        alayer[y][x]=1
                        x += 1
                    y += 1

                r = s.irect
                y = max(0,r.y/th)
                yy = min(h,r.bottom/th+1)
                while y < yy:
                    x = r.x/tw
                    xx = min(w,r.right/tw+1)
                    while x < xx:
                        if alayer[y][x]==0:
                            alayer[y][x]=2
                            self.updates.append((x,y))
                        x += 1
                    y += 1
                    

        #mark sprites that are not being updated that need to be updated because
        #they are being overwritte by sprites / tiles
        for s in sprites:
            if s.updated==0:
                r = s.irect
                y = max(0,r.y/th)
                yy = min(h,r.bottom/th+1)
                while y < yy:
                    x = max(0,r.x/tw)
                    xx = min(w,r.right/tw+1)
                    while x < xx:
                        if alayer[y][x]==1:
                            s.updated=1
                        x += 1
                    y += 1

        
        for u in self.updates:
            x,y=u
            xx,yy=x*tw-ox,y*th-oy
            if alayer[y][x] == 1:
                if blayer != None: blit(tiles[blayer[y][x]].image,(xx,yy))
                blit(tiles[tlayer[y][x]].image,(xx,yy))
            alayer[y][x]=0
            us.append(Rect(xx,yy,tw,th))
        
        for s in sprites:
            if s.updated:
                blit(s.image,(s.irect.x-ox, s.irect.y-oy))
                s.updated=0
                s._irect = Rect(s.irect)
                s._image = s.image
                
        self.updates = []
        return us

    def view_to_tile(self,pos):
        x,y = pos
        tiles = self.tiles
        tw,th = tiles[0].image.get_width(),tiles[0].image.get_height()
        return x/tw,y/th
        
    def tile_to_view(self,pos):
        x,y = pos
        tiles = self.tiles
        tw,th = tiles[0].image.get_width(),tiles[0].image.get_height()
        x,y = x*tw, y*th 
        return x,y
        
                    
    def screen_to_tile(self,pos):
        x,y = pos
        x,y = x+self.view.x,y+self.view.y
        return self.view_to_tile((x,y))
        
    def tile_to_screen(self,pos):
        x,y = pos
        x,y = self.tile_to_view(pos)
        x,y = x - self.view.x, y - self.view.y
        return x,y
                    

