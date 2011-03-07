"""a state engine. 
"""
import pygame
from pygame.locals import *

class State:
    """Template Class -- for a state.

    Arguments:
        game -- The state engine.
        value -- I usually pass in a custom value to a state
    
    For all of the template methods, they should return None unless they return 
    a new State to switch the engine to.

    """
    def __init__(self,game,value=None):
        self.game,self.value = game,value

    def init(self): 
        """Template Method - Initialize the state, called once the first time a state is selected."""
        return

    def paint(self,screen): 
        """Template Method - Paint the screen.  Called once after the state is selected.
        
        State is responsible for calling pygame.display.flip() or whatever.

        """
        return
        
    def repaint(self): 
        """Template Method - Request a repaint of this state."""
        self._paint = 1

    def update(self,screen):
        """Template Method - Update the screen.
        
        State is responsible for calling pygame.display.update(updates) or whatever.

        """
        return

    def loop(self):
        """Template Method - Run a logic loop, called once per frame."""
        return

    def event(self,e):
        """Template Method - Recieve an event."""
        return


class Quit(State):
    """A state to quit the state engine."""
    
    def init(self): 
        self.game.quit = 1


class Game:
    """Template Class - The state engine."""

    def fnc(self,f,v=None):
        s = self.state
        if not hasattr(s,f): return 0
        f = getattr(s,f)
        if v != None: r = f(v)
        else: r = f()
        if r != None:
            self.state = r
            self.state._paint = 1
            return 1
        return 0
        
    def run(self,state,screen=None):
        """Run the state engine, this is a infinite loop (until a quit occurs).
        
        Arguments:
            game -- a state engine
            screen -- the screen

        """
        self.quit = 0
        self.state = state
        if screen != None: self.screen = screen
        
        self.init()
        
        while not self.quit:
            self.loop()

    def loop(self):
        s = self.state
        if not hasattr(s,'_init') or s._init:
            s._init = 0
            if self.fnc('init'): return
        else: 
            if self.fnc('loop'): return
        if not hasattr(s,'_paint') or s._paint:
            s._paint = 0
            if self.fnc('paint',self.screen): return
        else: 
            if self.fnc('update',self.screen): return
        
        for e in pygame.event.get():
            #NOTE: this might break API?
            #if self.event(e): return
            if not self.event(e):
                if self.fnc('event',e): return
        self.tick()
        return
            
    def init(self):
        """Template Method - called at the beginning of State.run() to initialize things."""
        return
        
    def tick(self):
        """Template Method - called once per frame, usually for timer purposes."""
        pygame.time.wait(10)
    
    def event(self,e):
        """Template Method - called with each event, so the engine can capture special events.
        
        Rturn a True value if the event is captured and does not need to be passed onto the current
        state

        """
        if e.type is QUIT: 
            self.state = Quit(self)
            return 1


