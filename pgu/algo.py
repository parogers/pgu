"""Some handy algorithms for use in games, etc.

<p>please note that this file is alpha, and is subject to modification in
future versions of pgu!</p>
"""
print 'pgu.algo','This module is alpha, and is subject to change.'

#def dist(a,b):
#    return abs(a[0]-b[0]) + abs(a[1]-b[1])
    
class node:
    def __init__(self,prev,pos,dest):
        self.prev,self.pos,self.dest = prev,pos,dest
        if self.prev == None: self.g = 0
        else: self.g = self.prev.g + 1
        self.h = dist(pos,dest)
        self.f = self.g+self.h


def astar(start,end,layer,_dist):
    """uses the a* algorithm to find a path
    
    <pre>astar(start,end,layer,dist): return [list of positions]</pre>
    
    <dl>
    <dt>start<dd>start position
    <dt>end<dd>end position
    <dt>layer<dd>a grid where zero cells are open and non-zero cells are walls
    <dt>dist<dd>a distance function dist(a,b)
    </dl>
    
    <p>returns a list of positions from start to end</p>
    """
    global dist
    dist = _dist
    if layer[start[1]][start[0]]: return [] #start is blocked
    if layer[end[1]][end[0]]: return [] #end is blocked
    w,h = len(layer[0]),len(layer)
    if start[0] < 0 or start[1] < 0 or start[0] >= w or start[1] >= h: return [] #start outside of layer
    if end[0] < 0 or end[1] < 0 or end[0] >= w or end[1] >= h: return [] #end outside of layer

    opens = []
    open = {}
    closed = {}
    cur = node(None,start,end)
    open[cur.pos] = cur
    opens.append(cur)
    while len(open):
        cur = opens.pop(0)
        if cur.pos not in open: continue
        del open[cur.pos]
        closed[cur.pos] = cur
        if cur.pos == end: break
        for dx,dy in [(0,-1),(1,0),(0,1),(-1,0)]:#(-1,-1),(1,-1),(-1,1),(1,1)]:
            x,y = pos = cur.pos[0]+dx,cur.pos[1]+dy
            if layer[y][x]: continue
            #check for blocks of diagonals
            if layer[cur.pos[1]+dy][cur.pos[0]]: continue
            if layer[cur.pos[1]][cur.pos[0]+dx]: continue
            new = node(cur,pos,end)
            if pos in open and new.f >= open[pos].f: continue
            if pos in closed and new.f >= closed[pos].f: continue
            if pos in open: del open[pos]
            if pos in closed: del closed[pos]
            open[pos] = new
            lo = 0
            hi = len(opens)
            while lo < hi:
                mid = (lo+hi)/2
                if new.f < opens[mid].f: hi = mid
                else: lo = mid + 1
            opens.insert(lo,new)
    
    if cur.pos != end: 
        return []
                    
    path = []
    while cur.prev != None:
        path.append(cur.pos)
        cur = cur.prev
    path.reverse()
    return path
    

def getline(a,b):
    """returns a path of points from a to b
    
    <pre>getline(a,b): return [list of points]</pre>
    
    <dl>
    <dt>a<dd>starting point
    <dt>b<dd>ending point
    </dl>
    
    <p>returns a list of points from a to b</p>
    """
           
    path = []
    
    x1,y1 = a
    x2,y2 = b
    dx,dy = abs(x2-x1),abs(y2-y1)

    if x2 >= x1: xi1,xi2 = 1,1
    else: xi1,xi2 = -1,-1
    
    if y2 >= y1: yi1,yi2 = 1,1
    else: yi1,yi2 = -1,-1
    
    if dx >= dy:
        xi1,yi2 = 0,0
        d = dx
        n = dx/2
        a = dy
        p = dx
    else:
        xi2,yi1 = 0,0
        d = dy
        n = dy/2
        a = dx
        p = dy
        
    x,y = x1,y1
    c = 0
    while c <= p:
        path.append((x,y))
        n += a
        if n > d: 
            n -= d
            x += xi1
            y += yi1
        x += xi2
        y += yi2
        c += 1
    return path
