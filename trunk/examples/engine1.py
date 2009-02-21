"""<title>an example of engine usage</title>"""

import pygame
from pygame.locals import *

# the following line is not needed if pgu is installed
import sys; sys.path.insert(0, "..")

from pgu import engine

pygame.font.init()

screen = pygame.display.set_mode((320,240),SWSURFACE)

class Red(engine.State):
    def paint(self,s): 
        s.fill((255,0,0))
        pygame.display.flip()
    def event(self,e): 
        if e.type is KEYDOWN: return Green(self.game)
        
class Green(engine.State):
    def paint(self,s): 
        s.fill((0,255,0))
        pygame.display.flip()
    def event(self,e): 
        if e.type is KEYDOWN: return Blue(self.game)

##A state may subclass engine.State.
##::
class Blue(engine.State):
    ##
    ##The init method should load data, etc.  The __init__ method
    ##should do nothing but record the parameters.  If the init method
    ##returns a value, it becomes the new state.
    ##::
    def init(self):
        self.image = pygame.image.load("cuzco.png")
        self.pos = 0,0
        self._pos = self.pos
    ##
    ##The paint method is called once.  If you call repaint(), it
    ##will be called again.
    ##::
    def paint(self,s): 
        s.fill((0,0,255))
        s.blit(self.image,self.pos)
        pygame.display.flip()
    ##
    ##Every time an event occurs, event is called.  If the event method
    ##returns a value, it will become the new state.
    ##::
    def event(self,e): 
        if e.type is KEYDOWN: return Red(self.game)
    ##
    ##Loop is called once a frame.  It should contain all the
    ##logic.  If the loop method returns a value it will become the
    ##new state.
    ##::
    def loop(self):
        self._pos = self.pos
        self.pos = self.pos[0]+1,self.pos[1]+1
    ##
    ##Update is called once a frame.  It should update the display.
    ##::
    def update(self,screen):
        screen.fill((0,0,255),pygame.Rect(self._pos[0],self._pos[1],self.image.get_width(),self.image.get_height()))
        screen.blit(self.image,self.pos)
        pygame.display.flip() #better to do updates
    ##
        
game = engine.Game()
game.run(Red(game),screen)
