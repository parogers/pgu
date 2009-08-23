#!/usr/bin/env python

# This is not needed if you have PGU installed
import sys
sys.path.insert(0, "..")

import math
import time
import pygame
import pgu
from pgu import gui, timer


class DrawingArea(gui.Widget):
    def __init__(this, width, height):
        gui.Widget.__init__(this, width=width, height=height)
        this.imageBuffer = pygame.Surface((width, height))

    def paint(this, surf):
        # Paint whatever has been captured in the buffer
        surf.blit(this.imageBuffer, (0, 0))

    # Call this function to take a snapshot of whatever has been rendered
    # onto the display over this widget.
    def save_background(this):
        disp = pygame.display.get_surface()
        this.imageBuffer.blit(disp, this.get_abs_rect())

class TestDialog(gui.Dialog):
    def __init__(this):
        title = gui.Label("Some Dialog Box")
        label = gui.Label("Close this window to resume.")
        gui.Dialog.__init__(this, title, label)

class MainGui(gui.Desktop):
    gameAreaHeight = 500
    gameArea = None
    menuArea = None
    # The game engine
    engine = None

    def __init__(this, disp):
        gui.Desktop.__init__(this)

        # Setup the 'game' area where the action takes place
        this.gameArea = DrawingArea(disp.get_width(),
                                    this.gameAreaHeight)
        # Setup the gui area
        this.menuArea = gui.Container(
            height=disp.get_height()-this.gameAreaHeight)

        tbl = gui.Table(height=disp.get_height())
        tbl.tr()
        tbl.td(this.gameArea)
        tbl.tr()
        tbl.td(this.menuArea)

        this.setup_menu()

        this.init(tbl, disp)

    def setup_menu(this):
        tbl = gui.Table(vpadding=5, hpadding=2)
        tbl.tr()

        dlg = TestDialog()

        def click_cb():
            this.engine.pause()
            dlg.open()
            while (dlg.is_open()):
                for ev in pygame.event.get():
                    this.event(ev)
                rects = this.update()
                if (rects):
                    pygame.display.update(rects)
            this.engine.resume()

        btn = gui.Button("Pause clock", height=50)
        btn.connect(gui.CLICK, click_cb)
        tbl.td(btn)

        tbl2 = gui.Table()

        timeLabel = gui.Label("Clock speed")

        tbl2.tr()
        tbl2.td(timeLabel)

        slider = gui.HSlider(value=23,min=0,max=100,size=20,height=16,width=120)

        def update_speed():
            this.engine.clock.set_speed(slider.value/10.0)

        slider.connect(gui.CHANGE, update_speed)

        tbl2.tr()
        tbl2.td(slider)

        tbl.td(tbl2)

        this.menuArea.add(tbl, 0, 0)

    def open(this, w, pos=None):
        # Save whatever has been rendered to the 'game area' so we can
        # render it as a static image while the dialog is open.
        this.gameArea.save_background()
        gui.Desktop.open(this, w, pos)

    def get_render_area(this):
        return this.gameArea.get_abs_rect()


class GameEngine(object):
    def __init__(this, disp):
        this.disp = disp
        this.square = pygame.Surface((400,400)).convert_alpha()
        this.square.fill((255,0,0))
        this.app = MainGui(this.disp)
        this.app.engine = this

    # Pause the game clock
    def pause(this):
        this.clock.pause()

    # Resume the game clock
    def resume(this):
        this.clock.resume()

    def render(this, dest, rect):
        # Draw a rotating square
        angle = this.clock.get_time()*10
        surf = pygame.transform.rotozoom(this.square, angle, 1)
        r = surf.get_rect()
        r.center = rect.center
        dest.fill((0,0,0), rect)
        this.disp.blit(surf, r)

        def draw_clock(name, pt, radius, col, angle):
            pygame.draw.circle(dest, col, pt, radius)
            pygame.draw.line(dest, (0,0,0), pt, 
                             (pt[0]+radius*math.cos(angle),
                              pt[1]+radius*math.sin(angle)), 2)
            tmp = this.font.render(name, True, (255,255,255))
            dest.blit(tmp, (pt[0]-radius, pt[1]+radius+5))

        # Draw the real time clock
        angle = this.clock.get_real_time()*2*math.pi/10.0
        draw_clock("Real time", (30,30), 25, (255,200,100), angle)

        # Now draw the game clock
        angle = this.clock.get_time()*2*math.pi/10.0
        draw_clock("Game time", (90,30), 25, (255,100,255), angle)

        return (rect,)

    def run(this):
        this.app.update()
        pygame.display.flip()

        this.font = pygame.font.SysFont("", 16)

        this.clock = timer.Clock() #pygame.time.Clock()
        done = False
        while not done:
            # Process events
            for ev in pygame.event.get():
                if (ev.type == pygame.QUIT or 
                    ev.type == pygame.KEYDOWN and ev.key == pygame.K_ESCAPE):
                    done = True
                else:
                    # Pass the event off to pgu
                    this.app.event(ev)
            # Render the game
            rect = this.app.get_render_area()
            updates = []
            this.disp.set_clip(rect)
            lst = this.render(this.disp, rect)
            if (lst):
                updates += lst
            this.disp.set_clip()

            #this.clock.tick()

            # Give pgu a chance to update the display
            lst = this.app.update()
            if (lst):
                updates += lst
            pygame.display.update(updates)
            pygame.time.wait(10)


###
disp = pygame.display.set_mode((800, 600))
eng = GameEngine(disp)
eng.run()

