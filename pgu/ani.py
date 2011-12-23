"""animation loading and manipulating functions.

Please note that this file is alpha, and is subject to modification in
future versions of pgu!
"""

print ('pgu.ani - This module is alpha, and is subject to change.')

import math
import pygame

def _ani_load(tv,name,parts,frames,shape):
    l = len(frames)
    n = parts.pop()
    if len(parts):
        s = l/n
        for i in xrange(0,n):
            _ani_load(tv,name + ".%d"%i,parts[:],frames[s*i:s*(i+1)],shape)
        return
    
    for i in xrange(0,n):
        tv.images[name+".%d"%i] = frames[i],shape

def ani_load(tv,name,img,size,shape,parts):
    """Load an animation from an image

    Arguments:    
        tv -- vid to load into
        name -- prefix name to give the images
        image -- image to load anis from
        size -- w,h size of image
        shape -- shape of image (usually a subset of 0,0,w,h) used for collision detection
        parts -- list of parts to divide the animation into 
            for example parts = [4,5] would yield 4 animations 5 frames long, 20 total
            for example parts = [a,b,c] would yield ... images['name.a.b.c'] ..., a*b*c total
    
    """
    parts = parts[:]
    parts.reverse()
    w,h = size
    frames = []
    for y in xrange(0,img.get_height(),h):
        for x in xrange(0,img.get_width(),w):
            frames.append(img.subsurface(x,y,w,h))
    _ani_load(tv,name,parts,frames,shape)
    
    
def image_rotate(tv,name,img,shape,angles,diff=0):
    """Rotate an image and put it into tv.images
    
    Arguments:
        tv -- vid to load into
        name -- prefix name to give the images
        image -- image to load anis from
        shape -- shape fimage (usually a subset of 0,0,w,h) used for collision detection
        angles -- a list of angles to render in degrees
        diff -- a number to add to the angles, to correct for source image not actually being at 0 degrees

    """
    w1,h1 = img.get_width(),img.get_height()
    shape = pygame.Rect(shape)
    ps = shape.topleft,shape.topright,shape.bottomleft,shape.bottomright
    for a in angles:
        img2 = pygame.transform.rotate(img,a+diff)
        w2,h2 = img2.get_width(),img2.get_height()
        minx,miny,maxx,maxy = 1024,1024,0,0
        for x,y in ps:
            x,y = x-w1/2,y-h1/2
            a2 = math.radians(a+diff)
            #NOTE: the + and - are switched from the normal formula because of
            #the weird way that pygame does the angle...
            x2 = x*math.cos(a2) + y*math.sin(a2) 
            y2 = y*math.cos(a2) - x*math.sin(a2)
            x2,y2 = x2+w2/2,y2+h2/2
            minx = min(minx,x2)
            miny = min(miny,y2)
            maxx = max(maxx,x2)
            maxy = max(maxy,y2)
        r = pygame.Rect(minx,miny,maxx-minx,maxy-miny)
        #((ww-w)/2,(hh-h)/2,w,h)
        tv.images["%s.%d"%(name,a)] = img2,r
        

