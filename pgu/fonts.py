"""Some handy font-like objects.

Please note that this file is alpha, and is subject to modification in
future versions of pgu!
"""

print('pgu.fonts - This module is alpha, and is subject to change.')

import pygame
from pygame.locals import *

# Quick fix for python3
try:
    xrange
except:
    xrange = range

class TileFont:
    """Creates an instance of the TileFont class.  Interface compatible 
    with pygame.Font
    
    TileFonts are fonts that are stored in a tiled image.  Where the image 
    opaque, it assumed that the font is visible.  Font color is changed 
    automatically, so it does not work with fonts with stylized coloring.
    
    Arguments:
        size -- the dimensions of the characters
        hints -- a string of hints "abcdefg..."
        scale -- size to scale font to
        sensitive -- case sensitivity

    """

    def __init__(self,fname,size,hints,scale=None,sensitive=False):
        
        self.image = pygame.image.load(fname)
        
        w,h = self.image.get_width(),self.image.get_height()
        tw,th = size
        if not scale: scale = size
        self._size = size
        self.scale = scale
        
        self.chars = {}
        x,y = 0,0
        self.sensitive = sensitive
        if not self.sensitive: hints = hints.lower()
        for c in hints:
            if c not in ('\r','\n','\t'):
                img = self.image.subsurface(x,y,tw,th)
                self.chars[c] = img
                x += tw
                if x >= w: x,y = 0,y+th
                
        self.colors = {}
                
    def size(self,text):
        tw,th = self.scale
        return len(text)*tw,th
        
    def render(self,text,antialias=0,color=(255,255,255),background=None):
        size = self.size(text)
        scale = self.scale
        tw,th = self._size
        if background == None:
            s = pygame.Surface(size).convert_alpha()
            s.fill((0,0,0,0))
        else:
            s = pygame.Surface(size).convert()
            s.fill(background)
            
        if not self.sensitive: text = text.lower()
        
        if color not in self.colors: self.colors[color] = {}
        colored = self.colors[color]
        
        x,y = 0,0
        for c in text:
            if c in self.chars:
                if c not in colored:
                    img = self.chars[c].convert_alpha()
                    for yy in xrange(0,th):
                        for xx in xrange(0,tw):
                            r,g,b,a = img.get_at((xx,yy))
                            if a > 128:
                                img.set_at((xx,yy),color)
                    colored[c] = img
                img = colored[c]
                if scale != (tw,th): img = pygame.transform.scale(img,scale)
                s.blit(img,(x,y))
            x += scale[0]
        return s
        
        
class BorderFont: 
    """A decorator for normal fonts, adds a border. Interface compatible with pygame.Font.
    
    Arguments:
        size -- width of border; defaults 0
        color -- color of border; default (0,0,0)

    """
    def __init__(self,font,size=1,color=(0,0,0)):
        
        self.font = font
        self._size = size
        self.color = color
                
    def size(self,text):
        w,h = self.font.size(text)
        s = self._size
        return w+s*2,h+s*2
        
    def render(self,text,antialias=0,color=(255,255,255),background=None):
        size = self.size(text)
        
        if background == None:
            s = pygame.Surface(size).convert_alpha()
            s.fill((0,0,0,0))
        else:
            s = pygame.Surface(size).convert()
            s.fill(background)
            
        bg = self.font.render(text,antialias,self.color)
        fg = self.font.render(text,antialias,color)
        
        si = self._size
        dirs = [(-1,-1),(-1,0),(-1,1),(0,-1),(0,1),(1,-1),(1,0),(1,1)]
        for dx,dy in dirs: s.blit(bg,(si+dx*si,si+dy*si))
        s.blit(fg,(si,si))

        return s


