#!/usr/bin/python
"""<title>a magic tool that prettifies your levels for you</title>

<pre>
usage: levelpretty map.tga in.tga out.tga

a basic example:

map.tga contains "base" tiles drawn in the background and pretty tiles drawn in
the foreground.  it should contain all the knowldge needed to infer how to 
pretty up your level.

in.tga contains a level drawn using all "base" tiles (except where the algorithm
doesn't work -- you can put in fancy tiles to fill in those spaces, the algorithm
will back-wards infer what "base" tile the fancy tile is a substitute for)

out.tga will be generated using the map.tga and the in.tga

(to edit in leveledit and switch between background and foreground press 't')

map.tga bg  map.tga fg
..........  ..........
.xxx......  ..789..... 
.x.x......  ..4.6.....
.xxx......  ..123..... 
..........  .......... 

in.tga      out.tga
..........  ..........
.xxx......  .789......
.x.x.xxx..  .4.6.789..
.xxx.x.x..  .123.4.6..
.....xxx..  .....123..

levelpretty takes a level drawn with "base" tiles and auto-magically (using the knowledge
supplied in map.tga) turns a basic level into a fancy level.  this tool is useful for
rapid development of fancy looking levels that only have a few kinds of base tiles
but those base tiles look better when rendered using lots of fancier tiles.
</pre>
"""

import os,sys
from optparse import OptionParser

from pgu.tilevid import Tilevid

scoring = [
    [    1,   10,  100,   10,    1],
    [   10, 1000,10000, 1000,   10],
    [  100,10000,    0,10000,  100],
    [   10, 1000,10000, 1000,   10],
    [    1,   10,  100,   10,    1],
    ]
    
       
def get(l,tx,ty):
    width,height = len(l[0]),len(l)
    if ty >= 0 and ty < height and tx >= 0 and tx < width: return l[ty][tx]
    return None

def get2(l,tx,ty):
    width,height = len(l[0]),len(l)
    if ty >= 0 and ty < height and tx >= 0 and tx < width: return l[ty][tx]
    return 0

def get3(l,tx,ty):
    global used, rmap
    width,height = len(l[0]),len(l)
    if ty >= 0 and ty < height and tx >= 0 and tx < width: 
         v = l[ty][tx]
         if v not in used: 
             if v in rmap: return rmap[v]
             else: return 0
         return v
    return None
    
def diff(a,b):
    r = 0
    for y in range(0,5):
        for x in range(0,5):
            va,vb = a[y][x],b[y][x]
            if va == vb: r += scoring[y][x]
            else: r -= scoring[y][x]
    return r        
    
usage = "usage: %prog map.tga in.tga out.tga"
parser = OptionParser(usage)
(opts, args) = parser.parse_args()
if len(args) != 3:
    parser.error("incorrect number of arguments")
    
m_fname,i_fname, o_fname = args

m_level = Tilevid()
m_level.tga_load_level(m_fname,1)
at = m_level.blayer
bt = m_level.tlayer

i_level = Tilevid()
i_level.tga_load_level(i_fname,1)
it = i_level.tlayer

o_level = Tilevid()
o_level.tga_load_level(i_fname,1)
ot = o_level.tlayer

width,height = m_level.size
lookup = {}
used = []
rmap = {}
for y in range(0,height):
    for x in range(0,width):
        v = get(at,x,y)
        if v not in used: used.append(v)
        
        k = get(bt,x,y)
        rmap[k] = v
            
        #NOTE: optimization
        k = (get2(bt,x,y),get2(bt,x,y-1),get2(bt,x+1,y),get2(bt,x,y+1),get2(bt,x-1,y))
        if k == (0,0,0,0,0): continue 
        
        #NOTE: optimization
        k = (get2(at,x,y),get2(at,x,y-1),get2(at,x+1,y),get2(at,x,y+1),get2(at,x-1,y))
        if k == (0,0,0,0,0): continue
    
        k = (get(at,x,y),get(at,x,y-1),get(at,x+1,y),get(at,x,y+1),get(at,x-1,y))
        
        if k not in lookup: lookup[k] = []
        lookup[k].append((x,y))
        

width,height = i_level.size
for y in range(0,height):
    for x in range(0,width):
        v = get(it,x,y)
        if v in used:
            idata = [[get3(it,tx,ty) for tx in range(x-2,x+3)] for ty in range(y-2,y+3)]
            k = (get3(it,x,y),get3(it,x,y-1),get3(it,x+1,y),get3(it,x,y+1),get3(it,x-1,y))
            if k in lookup:
                v,score = 0,-100000
                for xx,yy in lookup[k]:
                    adata = [[get(at,tx,ty) for tx in range(xx-2,xx+3)] for ty in range(yy-2,yy+3)]
                    _v = get(bt,xx,yy)
                    _score = diff(idata,adata)
                    if _score > score: v,score = _v,_score
        ot[y][x] = v
        
o_level.tga_save_level(o_fname) #save the o_fname

