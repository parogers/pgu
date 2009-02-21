"""Classes for handling high score tables.
"""

import os

def High(fname,limit=10):
    """Create a Highs object and returns the default high score table.
    
    <pre>High(fname,limit=10)</pre>
    
    <dl>
    <dt>fname <dd>filename to store high scores in
    <dt>limit <dd>limit of scores to be recorded, defaults to 10
    </dl>
    """
    return Highs(fname,limit)['default']
    
class _Score:
    def __init__(self,score,name,data=None):
        self.score,self.name,self.data=score,name,data
    
class _High:
    """A high score table.  These objects are passed to the user, but should not be created directly.
    
    <p>You can iterate them:</p>
    <code>
    for e in myhigh:
        print e.score,e.name,e.data
    </code>
        
    <p>You can modify them:</p>
    <code>
    myhigh[0].name = 'Cuzco'
    </code>
    
    <p>You can find out their length:</p>
    <code>
    print len(myhigh)
    </code>
    """
    
    def __init__(self,highs,limit=10):
        self.highs = highs
        self._list = []
        self.limit = limit
        
    def save(self):
        """Save the high scores.
        
        <pre>_High.save()</pre>
        """
        self.highs.save()
        
    def submit(self,score,name,data=None):
        """Submit a high score to this table.
        
        <pre>_High.submit(score,name,data=None)</pre>
        
        <p>return -- the position in the table that the score attained.  None if the score did not attain a position in the table.</p>
        """
        n = 0
        for e in self._list:
            if score > e.score:
                self._list.insert(n,_Score(score,name,data))
                self._list = self._list[0:self.limit]
                return n
            n += 1
        if len(self._list) < self.limit:
            self._list.append(_Score(score,name,data))
            return len(self._list)-1
    
    def check(self,score):
        """Check if a score will attain a position in the table.
        
        <pre>_High.check(score)</pre>
        
        <p>return -- the position the score will attain, else None</p>
        """
        n = 0
        for e in self._list:
            if score > e.score:
                return n
            n += 1
        if len(self._list) < self.limit:
            return len(self._list)
        
        
    def __iter__(self):
        return self._list.__iter__()
        
    def __getitem__(self,key):
        return self._list[key]
        
    def __len__(self):
        return self._list.__len__()
        

class Highs:
    """The high score object.
    
    <pre>Highs(fname,limit=10)</pre>
    <ul>
    <dt>fname <dd>filename to store high scores in
    <dt>limit <dd>limit of scores to be recorded, defaults to 10
    </ul>
    
    <p>You may access _High objects through this object:</p>
   
    <code> 
    my_easy_hs = highs['easy']
    my_hard_hs = highs['hard']
    </code>
    
    """
    def __init__(self,fname,limit=10):
        self.fname = fname
        self.limit = limit
        self.load()
        
    def load(self):
        """Re-load the high scores.
        
        <pre>Highs.load()</pre>
        """
        
        self._dict = {}
        try:
            f = open(self.fname)
            for line in f.readlines():
                key,score,name,data = line.strip().split("\t")
                if key not in self._dict:
                    self._dict[key] = _High(self,self.limit)
                high = self._dict[key]
                high.submit(int(score),name,data)
            f.close()
        except:
            pass
    
    def save(self):
        """Save the high scores.
        
        <pre>Highs.save()</pre>
        """
        
        f = open(self.fname,"w")
        for key,high in self._dict.items():
            for e in high:
                f.write("%s\t%d\t%s\t%s\n"%(key,e.score,e.name,str(e.data)))
        f.close()
        
    def __getitem__(self,key):
        if key not in self._dict:
            self._dict[key] = _High(self,self.limit)
        return self._dict[key]
