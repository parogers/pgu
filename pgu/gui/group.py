"""
"""
from const import *
import widget

class Group(widget.Widget):
    """An object for grouping together Form elements.
    
    When the value changes, an gui.CHANGE event is sent. Although note, 
    that when the value is a list, it may have to be sent by hand via 
    g.send(gui.CHANGE).

    """
    
    def __init__(self,name=None,value=None):
        """Create Group instance.

        Arguments:
        name -- name as used in the Form
        value -- values that are currently selected in the group
    
        """
        widget.Widget.__init__(self,name=name,value=value)
        self.widgets = []
    
    def add(self,w):
        """Add a widget to this group."""
        self.widgets.append(w)
    
    def __setattr__(self,k,v):
        _v = self.__dict__.get(k,NOATTR)
        self.__dict__[k] = v
        if k == 'value' and _v != NOATTR and _v != v:
            self._change()
    
    def _change(self):
        self.send(CHANGE)
        for w in self.widgets:
            w.repaint()

