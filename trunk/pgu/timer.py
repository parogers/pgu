"""A timer for games with set-rate FPS.
"""

import pygame
import time


class Clock(object):
    # The game time when one of the clock parameters was last changed
    lastGameTime = None
    # The real time corresponding to the last game time
    lastRealTime = None
    # The game time when 'tick' was last called
    lastTickTime = None

    # Whether the timer is paused or not
    paused = False
    # When this clock was created
    startTime = None
    # The speed which this clock moves at relative to the real clock
    speed = 1

    def __init__(self):
        #self.startTime = time.time()
        self.lastGameTime = 0
        self.lastTickTime = 0
        self.lastRealTime = time.time()
        self.startTime = time.time()

    # Set the rate at which this clock ticks relative to the real clock
    def set_speed(self, n):
        assert(n >= 0)
        self.lastGameTime = self.get_time()
        self.lastRealTime = time.time()
        self.speed = n

    # Pause the clock
    def pause(self):
        if (not self.paused):
            self.lastGameTime = self.get_time()
            self.lastRealTime = time.time()
            self.paused = True

    # Resume the clock
    def resume(self):
        if (self.paused):
            self.paused = False
            self.lastRealTime = time.time()

    def tick(self, fps=0):
        tm = self.get_time()
        dt = tm - self.lastTickTime
        if (fps > 0):
            minTime = 1.0/fps
            if (dt < minTime):
                pygame.time.wait(int((minTime-dt)*1000))
                dt = minTime
        self.lastTickTime = tm
        return dt

    # Returns the amount of 'game time' that has passed since creating
    # the clock (paused time does not count).
    def get_time(self):
        if (self.paused):
            return self.lastGameTime
        return self.speed*(time.time()-self.lastRealTime) + self.lastGameTime

    def get_real_time(self):
        return (time.time()-self.startTime)


class Timer:
    """A timer for games with set-rate FPS."""
    
    def __init__(self,fps):
        if fps == 0: 
            self.tick = self._blank
            return
        self.wait = 1000/fps
        self.nt = pygame.time.get_ticks()
        pygame.time.wait(0)
        
    def _blank(self):
        pass
        
    def tick(self):
        """Wait correct amount of time each frame.  Call this once per frame."""
        self.ct = pygame.time.get_ticks()
        if self.ct < self.nt:
            pygame.time.wait(self.nt-self.ct)
            self.nt+=self.wait
        else: 
            self.nt = pygame.time.get_ticks()+self.wait


class Speedometer:
    """A timer replacement that returns out FPS once a second.
    
    Attributes:
        fps -- always set to the current FPS

    """
    def __init__(self):
        self.frames = 0
        self.st = pygame.time.get_ticks()
        self.fps = 0
        
    def tick(self):
        """ Call this once per frame."""
        r = None
        self.frames += 1
        self.ct = pygame.time.get_ticks()
        if (self.ct - self.st) >= 1000: 
            r = self.fps = self.frames
            #print "%s: %d fps"%(self.__class__.__name__,self.fps)
            self.frames = 0
            self.st += 1000
        pygame.time.wait(0) #NOTE: not sure why, but you gotta call this now and again
        return r

            


