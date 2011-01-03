"""Some handy algorithms for use in games, etc.

Please note that this file is alpha, and is subject to modification in
future versions of pgu!
"""

# The manhattan distance metric
def manhattan_dist(a,b):
    return abs(a[0]-b[0]) + abs(a[1]-b[1])
    
class node:
    def __init__(self, prev, pos, dest, dist):
        self.prev,self.pos,self.dest = prev,pos,dest
        if self.prev == None: self.g = 0
        else: self.g = self.prev.g + 1
        self.h = dist(pos,dest)
        self.f = self.g+self.h


def astar(start,end,layer,dist=manhattan_dist):
    """Uses the a* algorithm to find a path, and returns a list of positions 
    from start to end.

    Arguments:
        start -- start position
        end -- end position
        layer -- a grid where zero cells are open and non-zero cells are walls
        dist -- a distance function dist(a,b) - manhattan distance is used 
            by default
    
    """

    w,h = len(layer[0]),len(layer)
    if start[0] < 0 or start[1] < 0 or start[0] >= w or start[1] >= h: 
        return [] #start outside of layer
    if end[0] < 0 or end[1] < 0 or end[0] >= w or end[1] >= h:
        return [] #end outside of layer

    if layer[start[1]][start[0]]:
        return [] #start is blocked
    if layer[end[1]][end[0]]:
        return [] #end is blocked

    opens = []
    open = {}
    closed = {}
    cur = node(None, start, end, dist)
    open[cur.pos] = cur
    opens.append(cur)
    while len(open):
        cur = opens.pop(0)
        if cur.pos not in open: continue
        del open[cur.pos]
        closed[cur.pos] = cur
        if cur.pos == end: break
        for dx,dy in [(0,-1),(1,0),(0,1),(-1,0)]:#(-1,-1),(1,-1),(-1,1),(1,1)]:
            pos = cur.pos[0]+dx,cur.pos[1]+dy
            # Check if the point lies in the grid
            if (pos[0] < 0 or pos[1] < 0 or 
                pos[0] >= w or pos[1] >= h or
                layer[pos[0]][pos[1]]):
                continue
            #check for blocks of diagonals
            if layer[cur.pos[1]+dy][cur.pos[0]]: continue
            if layer[cur.pos[1]][cur.pos[0]+dx]: continue
            new = node(cur, pos, end, dist)
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
    """Returns a path of points from a to b

    Arguments:    
        a -- starting point
        b -- ending point

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

