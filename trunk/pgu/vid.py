"""Sprite and tile engine.

tilevid, isovid, hexvid are all subclasses of this interface.

Includes support for:

* Foreground Tiles
* Background Tiles
* Sprites
* Sprite-Sprite Collision handling
* Sprite-Tile Collision handling
* Scrolling 
* Loading from PGU tile and sprite formats (optional)
* Set rate FPS (optional)

This code was previously known as the King James Version (named after the
Bible of the same name for historical reasons.)

"""

import pygame
from pygame.rect import Rect
from pygame.locals import *
import math

class Sprite:
    """The object used for Sprites.

    Arguments:
        ishape -- an image, or an image, rectstyle.  The rectstyle will
            describe the shape of the image, used for collision
            detection.
        pos -- initial (x,y) position of the Sprite.
    
    Attributes:
        rect -- the current position of the Sprite
        _rect -- the previous position of the Sprite
        groups -- the groups the Sprite is in
        agroups -- the groups the Sprite can hit in a collision
        hit -- the handler for hits -- hit(g,s,a)
        loop -- the loop handler, called once a frame

    """
    def __init__(self,ishape,pos):
        if not isinstance(ishape, tuple):
            ishape = ishape,None
        image,shape = ishape
        if shape == None:
            shape = pygame.Rect(0,0,image.get_width(),image.get_height())
        if isinstance(shape, tuple): shape = pygame.Rect(shape)
        self.image = image
        self._image = self.image
        self.shape = shape
        self.rect = pygame.Rect(pos[0],pos[1],shape.w,shape.h)
        self._rect = pygame.Rect(self.rect)
        self.irect = pygame.Rect(pos[0]-self.shape.x,pos[1]-self.shape.y,
            image.get_width(),image.get_height())
        self._irect = pygame.Rect(self.irect)
        self.groups = 0
        self.agroups = 0
        self.updated = 1
        
    def setimage(self,ishape):
        """Set the image of the Sprite.
        
        Arguments:
            ishape -- an image, or an image, rectstyle.  The rectstyle will
                      describe the shape of the image, used for collision detection.

        """        
        if not isinstance(ishape, tuple):
            ishape = ishape,None
        image,shape = ishape
        if shape == None:
            shape = pygame.Rect(0,0,image.get_width(),image.get_height())
        if isinstance(shape, tuple):
            shape = pygame.Rect(shape)
        self.image = image
        self.shape = shape
        self.rect.w,self.rect.h = shape.w,shape.h
        self.irect.w,self.irect.h = image.get_width(),image.get_height()
        self.updated = 1

        
class Tile:
    """Tile Object used by TileCollide.
    
    Arguments:
        image -- an image for the Tile.
    
    Attributes:
        agroups -- the groups the Tile can hit in a collision
        hit -- the handler for hits -- hit(g,t,a)

    """
    def __init__(self,image=None):
        self.image = image
        self.agroups = 0
        
    def __setattr__(self,k,v):
        if k == 'image' and v != None:
            self.image_h = v.get_height()
            self.image_w = v.get_width()
        self.__dict__[k] = v

class _Sprites(list):
    def __init__(self):
        list.__init__(self)
        self.removed = []
        
    def append(self,v):
        list.append(self,v)
        v.updated = 1
        
    def remove(self,v):
        list.remove(self,v)
        v.updated = 1
        self.removed.append(v)
        
class Vid:
    """An engine for rendering Sprites and Tiles.
    
    Attributes:
        sprites -- a list of the Sprites to be displayed.  You may append and
                   remove Sprites from it.
        images  -- a dict for images to be put in.  
        size    -- the width, height in Tiles of the layers.  Do not modify.
        view    -- a pygame.Rect of the viewed area.  You may change .x, .y,
                    etc to move the viewed area around.
        bounds  -- a pygame.Rect (set to None by default) that sets the bounds
                    of the viewable area.  Useful for setting certain borders
                    as not viewable.
        tlayer  -- the foreground tiles layer
        clayer  -- the code layer (optional)
        blayer  -- the background tiles layer (optional)
        groups  -- a hash of group names to group values (32 groups max, as a tile/sprites 
                membership in a group is determined by the bits in an integer)

    """
    
    def __init__(self):
        self.tiles = [None for x in xrange(0,256)]
        self.sprites = _Sprites()
        self.images = {} #just a store for images.
        self.layers = None
        self.size = None
        self.view = pygame.Rect(0,0,0,0)
        self._view = pygame.Rect(self.view)
        self.bounds = None
        self.updates = []
        self.groups = {}
    
        
    def resize(self,size,bg=0):
        """Resize the layers.
        
        Arguments:
            size -- w,h in Tiles of the layers
            bg   -- set to 1 if you wish to use both a foreground layer and a
                    background layer

        """
        self.size = size
        w,h = size
        self.layers = [[[0 for x in xrange(0,w)] for y in xrange(0,h)]
            for z in xrange(0,4)]
        self.tlayer = self.layers[0]
        self.blayer = self.layers[1]
        if not bg: self.blayer = None
        self.clayer = self.layers[2]
        self.alayer = self.layers[3]
        
        self.view.x, self.view.y = 0,0
        self._view.x, self.view.y = 0,0
        self.bounds = None
        
        self.updates = []
    
    def set(self,pos,v):
        """Set a tile in the foreground to a value.
        
        Use this method to set tiles in the foreground, as it will make
        sure the screen is updated with the change.  Directly changing
        the tlayer will not guarantee updates unless you are using .paint()
        
        Arguments:
            pos -- (x,y) of tile
            v -- value

        """
        if self.tlayer[pos[1]][pos[0]] == v: return
        self.tlayer[pos[1]][pos[0]] = v
        self.alayer[pos[1]][pos[0]] = 1
        self.updates.append(pos)
        
    def get(self,pos):
        """Get the tlayer at pos.
        
        Arguments:
            pos -- (x,y) of tile

        """
        return self.tlayer[pos[1]][pos[0]]
    
    def paint(self,s):
        """Paint the screen.
        
        Arguments:
            screen -- a pygame.Surface to paint to

        Returns the updated portion of the screen (all of it)

        """
        return []
                
    def update(self,s):
        """Update the screen.
        
        Arguments:
            screen -- a pygame.Rect to update
        
        Returns a list of updated rectangles.

        """
        self.updates = []
        return []

    def tga_load_level(self,fname,bg=0):
        """Load a TGA level.  
        
        Arguments:
            g        -- a Tilevid instance
            fname    -- tga image to load
            bg        -- set to 1 if you wish to load the background layer

        """
        if type(fname) == str: img = pygame.image.load(fname)
        else: img = fname
        w,h = img.get_width(),img.get_height()
        self.resize((w,h),bg)
        for y in range(0,h):
            for x in range(0,w):
                t,b,c,_a = img.get_at((x,y))
                self.tlayer[y][x] = t
                if bg: self.blayer[y][x] = b
                self.clayer[y][x] = c
                
    def tga_save_level(self,fname):
        """Save a TGA level.

        Arguments:
            fname -- tga image to save to

        """
        w,h = self.size
        img = pygame.Surface((w,h),SWSURFACE,32)
        img.fill((0,0,0,0))
        for y in range(0,h):
            for x in range(0,w):
                t = self.tlayer[y][x]
                b = 0
                if self.blayer:
                    b = self.blayer[y][x]
                c = self.clayer[y][x]
                _a = 0
                img.set_at((x,y),(t,b,c,_a))
        pygame.image.save(img,fname)
                
                

    def tga_load_tiles(self,fname,size,tdata={}):
        """Load a TGA tileset.
        
        Arguments:
            g       -- a Tilevid instance
            fname    -- tga image to load
            size    -- (w,h) size of tiles in pixels
            tdata    -- tile data, a dict of tile:(agroups, hit handler, config)

        """
        TW,TH = size
        if type(fname) == str: img = pygame.image.load(fname).convert_alpha()
        else: img = fname
        w,h = img.get_width(),img.get_height()
        
        n = 0
        for y in range(0,h,TH):
            for x in range(0,w,TW):
                i = img.subsurface((x,y,TW,TH))
                tile = Tile(i)
                self.tiles[n] = tile
                if n in tdata:
                    agroups,hit,config = tdata[n]
                    tile.agroups = self.string2groups(agroups)
                    tile.hit = hit
                    tile.config = config
                n += 1


    def load_images(self,idata):
        """Load images.
        
        Arguments:
            idata -- a list of (name, fname, shape)

        """
        for name,fname,shape in idata:
            self.images[name] = pygame.image.load(fname).convert_alpha(),shape

    def run_codes(self,cdata,rect):
        """Run codes.
        
        Arguments:
            cdata -- a dict of code:(handler function, value)
            rect -- a tile rect of the parts of the layer that should have
                 their codes run

        """
        tw,th = self.tiles[0].image.get_width(),self.tiles[0].image.get_height()

        x1,y1,w,h = rect
        clayer = self.clayer
        t = Tile()
        for y in range(y1,y1+h):
            for x in range(x1,x1+w):
                n = clayer[y][x]
                if n in cdata:
                    fnc,value = cdata[n]
                    t.tx,t.ty = x,y
                    t.rect = pygame.Rect(x*tw,y*th,tw,th)
                    fnc(self,t,value)

        
    def string2groups(self,str):
        """Convert a string to groups."""
        if str == None: return 0
        return self.list2groups(str.split(","))

    def list2groups(self,igroups):
        """Convert a list to groups."""
        for s in igroups:
            if not s in self.groups:
                self.groups[s] = 2**len(self.groups)
        v = 0
        for s,n in self.groups.items():
            if s in igroups: v|=n
        return v

    def groups2list(self,groups):
        """Convert a groups to a list."""
        v = []
        for s,n in self.groups.items():
            if (n&groups)!=0: v.append(s)
        return v

    def hit(self,x,y,t,s):
        tiles = self.tiles
        tw,th = tiles[0].image.get_width(),tiles[0].image.get_height()
        t.tx = x
        t.ty = y
        t.rect = Rect(x*tw,y*th,tw,th)
        t._rect = t.rect
        if hasattr(t,'hit'):
            t.hit(self,t,s)

    def loop(self):
        """Update and hit testing loop.  Run this once per frame."""
        self.loop_sprites() #sprites may move
        self.loop_tilehits() #sprites move
        self.loop_spritehits() #no sprites should move
        for s in self.sprites:
            s._rect = pygame.Rect(s.rect)
        
    def loop_sprites(self):
        as_ = self.sprites[:]
        for s in as_:
            if hasattr(s,'loop'):
                s.loop(self,s)

    def loop_tilehits(self):
        tiles = self.tiles
        tw,th = tiles[0].image.get_width(),tiles[0].image.get_height()

        layer = self.layers[0]

        as_ = self.sprites[:]
        for s in as_:
            self._tilehits(s)
    
    def _tilehits(self,s):
        tiles = self.tiles
        tw,th = tiles[0].image.get_width(),tiles[0].image.get_height()
        layer = self.layers[0]
        
        for _z in (0,): 
            if s.groups != 0:

                _rect = s._rect
                rect = s.rect

                _rectx = _rect.x
                _recty = _rect.y
                _rectw = _rect.w
                _recth = _rect.h

                rectx = rect.x
                recty = rect.y
                rectw = rect.w
                recth = rect.h

                rect.y = _rect.y
                rect.h = _rect.h

                hits = []
                ct,cb,cl,cr = rect.top,rect.bottom,rect.left,rect.right
                #nasty ol loops
                y = ct/th*th
                while y < cb:
                    x = cl/tw*tw
                    yy = y/th
                    while x < cr:
                        xx = x/tw
                        t = tiles[layer[yy][xx]]
                        if (s.groups & t.agroups)!=0:
                            #self.hit(xx,yy,t,s)
                            d = math.hypot(rect.centerx-(xx*tw+tw/2),
                                rect.centery-(yy*th+th/2))
                            hits.append((d,t,xx,yy))

                        x += tw
                    y += th
                
                hits.sort()
                #if len(hits) > 0: print self.frame,hits
                for d,t,xx,yy in hits:
                    self.hit(xx,yy,t,s)
                
                #switching directions...
                _rect.x = rect.x
                _rect.w = rect.w
                rect.y = recty
                rect.h = recth

                hits = []
                ct,cb,cl,cr = rect.top,rect.bottom,rect.left,rect.right
                #nasty ol loops
                y = ct/th*th
                while y < cb:
                    x = cl/tw*tw
                    yy = y/th
                    while x < cr:
                        xx = x/tw
                        t = tiles[layer[yy][xx]]
                        if (s.groups & t.agroups)!=0:
                            d = math.hypot(rect.centerx-(xx*tw+tw/2),
                                rect.centery-(yy*th+th/2))
                            hits.append((d,t,xx,yy))
                            #self.hit(xx,yy,t,s)
                        x += tw
                    y += th
                
                hits.sort()    
                #if len(hits) > 0: print self.frame,hits
                for d,t,xx,yy in hits:
                    self.hit(xx,yy,t,s)

                #done with loops
                _rect.x = _rectx
                _rect.y = _recty


    def loop_spritehits(self):
        as_ = self.sprites[:]
        
        groups = {}
        for n in range(0,31):
            groups[1<<n] = []
        for s in as_:
            g = s.groups
            n = 1
            while g:
                if (g&1)!=0: groups[n].append(s)
                g >>= 1
                n <<= 1
                
        for s in as_:
            if s.agroups!=0:
                rect1,rect2 = s.rect,Rect(s.rect)
                #if rect1.centerx < 320: rect2.x += 640
                #else: rect2.x -= 640
                g = s.agroups
                n = 1
                while g:
                    if (g&1)!=0:
                        for b in groups[n]:    
                            if (s != b and (s.agroups & b.groups)!=0
                                    and s.rect.colliderect(b.rect)):
                                s.hit(self,s,b)

                    g >>= 1
                    n <<= 1


    def screen_to_tile(self,pos):
        """Convert a screen position to a tile position."""
        return pos
        
    def tile_to_screen(self,pos):
        """Convert a tile position to a screen position."""
        return pos
                    

