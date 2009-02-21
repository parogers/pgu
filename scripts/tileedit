#!/usr/bin/python
"""<title>a simple tile editor for pygame</title>
<pre>

usage: tileedit tiles.tga [tile_w] [tile_h]
windows: python tileedit tiles.tga [tile_w] [tile_h]

options:
  -h, --help            show this help message and exit
  --sw=SCREEN_W         screen width (app)
  --sh=SCREEN_H         screen height (app)
  --tw=TILE_W           tile width (image)
  --th=TILE_H           tile height (image)
  --width=WIDTH         new width (image)
  --height=HEIGHT       new height (image)
  -pPALETTE, --pal=PALETTE
                        filename of palette (image)
  -d, --defaults        set default settings (image)

example:
tileedit tiles.tga 16 16

note:
the editor can only edit tga files.

you may edit default options in tileedit.ini

interface:
- menus for common commands
- toolbox
- tile edit area
    left click to use current tool
    right click to select color
- tile select area
    left click to select a tile
    right click to select any region
- color select area
    click to select a color

keys:
s - save
d - reload

z - undo
x - cut selection
c - copy selection
v - paste clipboard
delete - delete selection
f - fill selection
e - draw ellipse in selection
a - select all

[ - rotate -90
] - rotate +90
, - flip horizontal
. - flip vertical

arrows - change tile
F10 - toggle fullscreen
</pre>
"""

import os,sys    
from optparse import OptionParser
from ConfigParser import ConfigParser
import pygame
from pygame.locals import *

# try:
#     import Image
#     have_pil=True
# except:
#     print "import Image failure; PIL not found."
#     have_pil=False

have_pil = False

# the following line is not needed if pgl is installed
import sys; sys.path.insert(0, "..")
import shutil

from pgu import gui, html


#whatever...
ini_fname = "tileedit.ini"
ini = ConfigParser()

cfg = {}

class _app(gui.Container):
    def __init__(self):
        gui.Container.__init__(self)
        #self.cls = "desktop"
        #self.background = gui.Box(self.style.background)
        
        self.screen_w = cfg['screen_w']
        self.screen_h = cfg['screen_h']
        self.screen = pygame.display.set_mode((self.screen_w,self.screen_h),SWSURFACE)
        
        self.fname = cfg['fname']

        if self.fname != None:
            if have_pil==True:

                im = Image.open(self.fname)
                mode = im.mode
                size = im.size
                data = im.tostring()

                assert mode in ("RGB", "RGBA")

                self.tiles = pygame.image.fromstring(data, size, mode)

            else:
                self.tiles = pygame.image.load(self.fname) # old tga-only method
        else:
            w,h = cfg['width'],cfg['height']
            s = pygame.Surface((w,h),SWSURFACE|SRCALPHA,32)
            s.fill((0,0,0,0))
            self.tiles = s

        self.tiles_w, self.tiles_h = self.tiles.get_width(),self.tiles.get_height()
            
        
        self.tile_w, self.tile_h = cfg['tile_w'],cfg['tile_h'] 
        self.tile = self.tiles.subsurface((0,0,self.tile_w,self.tile_h))
        
        self.color = (255,255,255,255)
        self.mode = 'draw'
        self.clipboard = None
        self.select = Rect(0,0,self.tile_w,self.tile_h)
        self.history = []
        self.dirty = 0
        
    def archive(self):
        h = self.history
        if len(h) >= 32:
            del h[0]
        c = pygame.Surface((self.tile_w,self.tile_h),SWSURFACE,self.tile)
        c.fill((0,0,0,0))
        c.blit(self.tile,(0,0))
        h.append((c,self.tile.get_offset()))
        self.dirty = 1
        
    def undo(self):
        if len(self.history) == 0: return
        c,off = self.history.pop()
        self.tiles.fill((0,0,0,0),(off[0],off[1],self.tile_w,self.tile_h))
        self.tiles.blit(c,off)
        self.tdraw.repaint()
        self.tpicker.repaint()
        self.dirty = 1
        
    def __setattr__(self,k,v):
        self.__dict__[k] = v
        
        if k == 'color':
            if hasattr(self,'cpreview'): self.cpreview.repaint()
        if k == 'tile':
            if hasattr(self,'tdraw'): self.tdraw.repaint()
            if hasattr(self,'tpicker'): self.tpicker.repaint()
            if hasattr(self,'tpreview'): self.tpreview.repaint()
    def event(self,e):
        if e.type is KEYDOWN:
            for key,cmd,value in keys:
                if e.key == key:
                    cmd(value)
                    return
        return gui.Container.event(self,e)
    
class cpreview(gui.Widget):
    def __init__(self,w,h):
        gui.Widget.__init__(self)
        self.style.width = w 
        self.style.height = h
        
    def paint(self,s):
        s.fill((128,128,128))
        s.fill(app.color)

        
class cpicker(gui.Widget):
    def __init__(self,w,h,pal):
        gui.Widget.__init__(self)
        self.style.width = w
        self.style.height = h
        self.palette = pal
        self.palette_w = pal.get_width()
        self.palette_h = pal.get_height()
    
    def paint(self,s):
        s.blit(pygame.transform.scale(self.palette,(self.rect.w,self.rect.h)),(0,0))
            
    def event(self,e):
        if (e.type is MOUSEBUTTONDOWN) or (e.type is MOUSEMOTION and e.buttons[0] == 1 and self.container.myfocus == self):
            x,y = e.pos[0]*self.palette_w/self.rect.w,e.pos[1]*self.palette_h/self.rect.h
            x,y = max(0,x),max(0,y)
            x,y = min(self.palette_w-1,x),min(self.palette_h-1,y)
        
            app.color = self.palette.get_at((x,y))

class tpicker(gui.Widget):
    def __init__(self):
        gui.Widget.__init__(self)
        self.style.width = app.tiles_w
        self.style.height = app.tiles_h
        
    def paint(self,s):
        s.fill((128,128,128))
        s.blit(app.tiles,(0,0))
        off = app.tile.get_offset()
        pygame.draw.rect(s,(255,255,255),(off[0],off[1],app.tile_w,app.tile_h),2)
        
    def pick(self,pos):
        x,y = pos
        while x < 0: x += self.rect.w
        while y < 0: y += self.rect.h
        while x >= self.rect.w: x -= self.rect.w
        while y >= self.rect.h: y -= self.rect.h
        app.tile = app.tiles.subsurface((x,y,app.tile_w,app.tile_h))

    def event(self,e):
        if (e.type is MOUSEBUTTONDOWN and e.button == 1) or (e.type is MOUSEMOTION and e.buttons[0] == 1 and self.container.myfocus == self):
            x,y = e.pos[0]/app.tile_w*app.tile_w,e.pos[1]/app.tile_h*app.tile_h
            self.pick((x,y))
            
        if (e.type is MOUSEBUTTONDOWN and e.button == 3) or (e.type is MOUSEMOTION and e.buttons[2] == 1 and self.container.myfocus == self):
            x,y = e.pos[0]-app.tile_w/2,e.pos[1]-app.tile_h/2
            x = min(self.rect.w-app.tile_w-1,max(0,x))
            y = min(self.rect.h-app.tile_h-1,max(0,y))
            self.pick((x,y))

class tpreview(gui.Widget):
    def __init__(self):
        gui.Widget.__init__(self)
        self.style.width = app.tile_w*3
        self.style.height = app.tile_h*3
    def paint(self, s):
        atw = app.tile_w
        ath = app.tile_h
        s.fill((100,100,100))
        s.blit(app.tile,(0,0))
        s.blit(app.tile,(1*atw,0))
        s.blit(app.tile,(2*atw,0))
        s.blit(app.tile,(0,1*ath))
        s.blit(app.tile,(1*atw,1*ath))
        s.blit(app.tile,(2*atw,1*ath))
        s.blit(app.tile,(0,2*ath))
        s.blit(app.tile,(1*atw,2*ath))
        s.blit(app.tile,(2*atw,2*ath))        

class tdraw(gui.Widget):
    def __init__(self,w,h):
        gui.Widget.__init__(self)
        self.rect.w = self.style.width = w
        self.rect.h = self.style.height = h
        self.overlay = pygame.Surface((app.tile_w,app.tile_h)).convert_alpha()
        self.overlay.fill((0,0,0,0))
        s = pygame.Surface((self.rect.w,self.rect.h))
        clrs = [(148,148,148),(108,108,108)]
        for y in range(0,app.tile_h*2):
            for x in range(0,app.tile_w*2):
                s.fill(clrs[(x+y)%2],(
                    self.rect.w*x/(app.tile_w*2),
                    self.rect.h*y/(app.tile_h*2),
                    self.rect.w/(app.tile_w*2)+1,
                    self.rect.h/(app.tile_h*2)+2))
        self.bg = s

        s = pygame.Surface((self.rect.w,self.rect.h)).convert_alpha()
        s.fill((0,0,0,0))
        for x in range(0,app.tile_w):
            pygame.draw.line(s,(0,0,0),(self.rect.w*x/app.tile_w,0),(self.rect.w*x/app.tile_w,self.rect.h))
        for y in range(0,app.tile_h):
            pygame.draw.line(s,(0,0,0),(0,self.rect.h*y/app.tile_h),(self.rect.w,self.rect.h*y/app.tile_h))
        self.grid = s

        
    def paint(self,s):
        s.blit(self.bg,(0,0))
        s.blit(pygame.transform.scale(app.tile,(self.rect.w,self.rect.h)),(0,0))
        s.blit(pygame.transform.scale(self.overlay,(self.rect.w,self.rect.h)),(0,0))
        #if app.mode == 'select':
        s.blit(self.grid,(0,0))
        r = app.select
        pygame.draw.rect(s,(255,255,255,128),Rect(r.x*self.rect.w/app.tile_w,r.y*self.rect.h/app.tile_h,r.w*self.rect.w/app.tile_w,r.h*self.rect.h/app.tile_h),4)
        
    def event(self,e):
        if (e.type is MOUSEBUTTONDOWN and e.button == 3) or (e.type is MOUSEMOTION and e.buttons[2]==1 and self.container.myfocus == self):
            self.picker_down(e)
        if e.type is MOUSEBUTTONDOWN and e.button == 1:
            a = '%s_down'%app.mode
            if hasattr(self,a): getattr(self,a)(e)
        if e.type is MOUSEMOTION and e.buttons[0] and self.container.myfocus == self:
            a = '%s_drag'%app.mode
            if hasattr(self,a): getattr(self,a)(e)
        if e.type is MOUSEBUTTONUP and e.button == 1:
            a = '%s_up'%app.mode
            if hasattr(self,a): getattr(self,a)(e)
            
    #picker
    def picker_down(self,e):
        pos = self.getpos(e)
        c = app.tile.get_at(pos)
        app.color = c
    
    #fill
    def fill_down(self,e):
        app.archive()
        pos = self.getpos(e)
        bg = app.tile.get_at(pos)
        if bg == app.color: return
        self.fill_pixel(pos,bg)
        self.repaint()
        
        
    def fill_pixel(self,pos,bg): #worst algorithm
        c = app.tile.get_at(pos)
        if c != bg: return
        app.tile.set_at(pos,app.color)
        x,y = pos
        if x > 0: self.fill_pixel((x-1,y),bg)
        if x < app.tile_w-1: self.fill_pixel((x+1,y),bg)
        if y > 0: self.fill_pixel((x,y-1),bg)
        if y < app.tile_h-1: self.fill_pixel((x,y+1),bg)
        
    #pixel        
    def pixel_down(self,e):
        app.archive()
        pos = self.getpos(e)
        app.tile.set_at(pos,app.color)
        self.repaint()
        
    #line
    def line_down(self,e):
        pos = self.getpos(e)
        self.pos = pos
        
    def line_drag(self,e):
        self.overlay.fill((0,0,0,0))
        pos = self.getpos(e)
        pygame.draw.line(self.overlay,app.color,self.pos,pos)
        self.repaint()
    
    def line_up(self,e):
        app.archive()
        self.overlay.fill((0,0,0,0))
        pos = self.getpos(e)
        pygame.draw.line(app.tile,app.color,self.pos,pos)
        self.repaint()
        
    #ellipse
    def ellipse_down(self,e):
        pos = self.getpos(e)
        self.pos = pos
        
    def ellipse_drag(self,e):
        self.overlay.fill((0,0,0,0))
        pos = self.getpos(e)
        r = pygame.Rect(self.pos[0],self.pos[1],pos[0]-self.pos[0],pos[1]-self.pos[1])
        r.normalize()
        r.width += 1
        r.height += 1
        r.width,r.height = max(2,r.width),max(2,r.height)
        pygame.draw.ellipse(self.overlay,app.color,r,1)
        self.repaint()
    
    def ellipse_up(self,e):
        app.archive()
        self.overlay.fill((0,0,0,0))
        pos = self.getpos(e)
        r = pygame.Rect(self.pos[0],self.pos[1],pos[0]-self.pos[0],pos[1]-self.pos[1])
        r.normalize()
        r.width += 1
        r.height += 1
        r.width,r.height = max(2,r.width),max(2,r.height)
        pygame.draw.ellipse(app.tile,app.color,r,1)
        self.repaint()
        
    #draw
    def draw_down(self,e):
        app.archive()
        pos = self.getpos(e)
        app.tile.set_at(pos,app.color)
        self.pos = pos
        self.repaint()
        
    def draw_drag(self,e):
        pos = self.getpos(e)
        pygame.draw.line(app.tile,app.color,self.pos,pos)
        self.pos = pos
        self.repaint()
        
    def getpos(self,e):
        x,y = (e.pos[0])*app.tile_w/self.rect.w,(e.pos[1])*app.tile_h/self.rect.h
        x = min(max(0,x),app.tile_w-1)
        y = min(max(0,y),app.tile_h-1)
        return x,y
    
    def getpos2(self,e):
        w = self.rect.w/app.tile_w
        h = self.rect.h/app.tile_h
        x,y = (e.pos[0]+w/2)*app.tile_w/self.rect.w,(e.pos[1]+h/2)*app.tile_h/self.rect.h
        x = min(max(0,x),app.tile_w)
        y = min(max(0,y),app.tile_h)
        return x,y
    
            
    
    #select
    def select_down(self,e):
        pos = self.getpos2(e)
        app.select = Rect(pos[0],pos[1],0,0)
        self.repaint()
        
    def select_drag(self,e):
        pos = self.getpos2(e)
        #pos = (e.pos[0]+app.tile_w/2)/app.tile_w,(e.pos[1]+app.tile_h/2)/app.tile_h
        
        app.select = Rect(app.select.x,app.select.y,pos[0]-app.select.x,pos[1]-app.select.y)
        app.select.w = max(0,app.select.w)
        app.select.h = max(0,app.select.h)
        
        #print app.select
        
        self.repaint()
        

        
    #eraser
    def eraser_down(self,e):
        app.archive()
        pos = self.getpos(e)
        app.tile.set_at(pos,(0,0,0,0))
        self.pos = pos
        self.repaint()
        
    def eraser_drag(self,e):
        pos = self.getpos(e)
        pygame.draw.line(app.tile,(0,0,0,0),self.pos,pos)
        self.pos = pos
        self.repaint()
        

def cmd_quit(value):
    if app.dirty: _dirty(_cmd_quit,value)
    else: _cmd_quit(value)

def _cmd_quit(value):
    app.top.quit()

def cmd_all(value):
    app.select = Rect(0,0,app.tile_w,app.tile_h)
    app.tdraw.repaint()

def cmd_undo(value):
    app.undo()
    
def cmd_redo(value):
    pass
    
def cmd_copy(value):
    #next version of pygame?
    #app.clipboard = app.tile.subsurface(app.select).copy()
    s = app.tile.subsurface(app.select)
    app.clipboard = pygame.Surface((app.select.w,app.select.h),SWSURFACE,s)
    app.clipboard.fill((0,0,0,0))
    app.clipboard.blit(s,(0,0))
    
def cmd_paste(value):
    if app.clipboard != None:
        app.archive()
        app.tile.fill((0,0,0,0),(app.select.x,app.select.y,app.clipboard.get_width(),app.clipboard.get_height()))
        app.tile.blit(app.clipboard,app.select)
        app.tdraw.repaint()

def cmd_cut(value):
    cmd_copy(value)
    cmd_delete(value)
    
def cmd_fullscreen(value):
    pygame.display.toggle_fullscreen()
    
def cmd_delete(value):
    app.archive()
    app.tile.fill((0,0,0,0),app.select)
    app.tdraw.repaint()

def cmd_fill(value):        
    app.archive()
    app.tile.fill(app.color,app.select)
    app.tdraw.repaint()

#NOTE: this feature is a temporary HACK, to be replaced by
#an ellipse tool in the future
def cmd_ellipse(value):
    app.archive()
    pygame.draw.ellipse(app.tile,app.color,app.select,1)
    app.tdraw.repaint()
        
def cmd_rotate(value):
    a = value
    app.archive()
    s = pygame.transform.rotate(app.tile,a)
    app.tile.fill((0,0,0,0))
    app.tile.blit(s,(0,0))
    app.tdraw.repaint()
    
def cmd_flip(value):
    fh,fv = value
    app.archive()
    s = pygame.transform.flip(app.tile,fh,fv)
    app.tile.fill((0,0,0,0))
    app.tile.blit(s,(0,0))
    app.tdraw.repaint()

def cmd_tpick(value):
    dx,dy = value
    off = app.tile.get_offset()
    app.tpicker.pick((off[0]+dx*app.tile_w,off[1]+dy*app.tile_h))
    
def cmd_mode(value):
    mode = value
    app.mode = mode

def cmd_load(value):
    if app.dirty: _dirty(_cmd_load,value)
    else: _cmd_load(value)


def _cmd_load(value):
    if app.fname == None:
        ErrorDialog("Load failed","Image is untitled.").open()
        return
    raise Restart()
    

def cmd_active_save(value):
    """ we check if we want to save on screen focus...
    """

    if app.save_activeevent_switch.value:
        if app.dirty:
            #"is dirty... saving"
            return cmd_save(value)
    else:
        pass
        #"is not dirty, not saving"




def cmd_save(value):
    if app.fname == None:
        return cmd_saveas(value)
    try:
        # make a temp file... save it there, and then move it in.
        # so as to avoid race with anything reading it.

        temp_file_name = "tmp_" + app.fname
        print temp_file_name
        if have_pil==True:
            stim = pygame.image.tostring(app.tiles, "RGB")
            im=Image.fromstring("RGB", (app.tiles.get_width(),app.tiles.get_height()), stim)
            im.save(temp_file_name)
        else:
            pygame.image.save(app.tiles,temp_file_name)
        #move temp file into place.
        shutil.move(temp_file_name, app.fname)
        cfg_to_ini(['tile_w','tile_h','palette'],app.fname)
        ini_save()
        app.dirty = 0
    except Exception, v:
        ErrorDialog("Save failed.",v).open()
        return
    
def cmd_saveas(value):
    dialog = SaveAsDialog()
    
    def onchange(value):
        value.close()
        vv = value.value
        fname = vv['fname'].value
        if len(fname) == 0:
            ErrorDialog("Save As failed.","File Name too short!").open()
            return
        global cfg
        app.fname = cfg['fname'] = fname
        return cmd_save(None)
        
    dialog.connect(gui.CHANGE,onchange,dialog)
    dialog.open()

def cmd_open(value):
    if app.dirty: _dirty(_cmd_open,value)
    else: _cmd_open(value)

    
def _cmd_open(value):
    dialog = OpenDialog()
    
    def onchange(value):
        value.close()
        vv = value.value
        ok = 0
        
        try:        
            fname,tile_w,tile_h = vv['fname'].value,int(vv['tile_w'].value),int(vv['tile_h'].value)
            global cfg
            cfg['fname'] = fname
            cfg['tile_w'] = tile_w
            cfg['tile_h'] = tile_h
            ok = 1
        except Exception,v:
            ErrorDialog("Open failed.",v).open()
            
        if ok: raise Restart()

    
    dialog.connect(gui.CHANGE,onchange,dialog)
    dialog.open()


class Restart(Exception):
    pass
def _dirty(fnc,v):
    dialog = DirtyDialog()
    def onchange(value):
        value.close()
        return fnc(v)
    dialog.connect(gui.CHANGE,onchange,dialog)
    dialog.open()
    
def cmd_new(value):
    if app.dirty: _dirty(_cmd_new,value)
    else: _cmd_new(value)
    
        
def _cmd_new(value):
    dialog = NewDialog()
    
    def onchange(value):
        value.close()
        vv = value.value
        ok = 0
        try:        
            width,height,tile_w,tile_h = int(vv['width'].value),int(vv['height'].value),int(vv['tile_w'].value),int(vv['tile_h'].value)
            global cfg
            cfg['fname'] = None
            cfg['width'] = width
            cfg['height'] = height
            cfg['tile_w'] = tile_w
            cfg['tile_h'] = tile_h
            ok = 1
        except Exception, v:
            ErrorDialog("New failed.",v).open()
        if ok:
            raise Restart()
    
    dialog.connect(gui.CHANGE,onchange,dialog)
    dialog.open()


menus = [
    ('File/New',cmd_new,None),
    ('File/Open',cmd_open,None),
    ('File/Save',cmd_save,None),
    ('File/Save As',cmd_saveas,None),
    ('File/Reload',cmd_load,None),
    ('File/Quit',cmd_quit,None),

    ('Edit/Undo',cmd_undo,None),
    #('Edit/Redo',None,None,None),
    ('Edit/Cut',cmd_cut,None),
    ('Edit/Copy',cmd_copy,None),
    ('Edit/Paste',cmd_paste,None),
    ('Edit/Delete',cmd_delete,None),
    ('Edit/Fill',cmd_fill,None),
        ('Edit/Ellipse',cmd_ellipse,None),
    ('Edit/Select All',cmd_all,None),
    
    ('Transform/Rotate 90 CCW',cmd_rotate,90),
    ('Transform/Rotate 90 CW',cmd_rotate,-90),
    ('Transform/Flip Horizontal',cmd_flip,(1,0)),
    ('Transform/Flip Vertical',cmd_flip,(0,1)),
    ]

keys = [
    (K_s,cmd_save,None),
    (K_d,cmd_load,None),

    (K_a,cmd_all,None),
    (K_z,cmd_undo,None),
    #('Edit/Redo',None,None,None),
    (K_c,cmd_copy,None),
    (K_v,cmd_paste,None),
    (K_x,cmd_cut,None),
    (K_DELETE,cmd_delete,None),
    (K_f,cmd_fill,None),
        (K_e,cmd_ellipse,None),
    
    (K_LEFTBRACKET,cmd_rotate,90),
    (K_RIGHTBRACKET,cmd_rotate,-90),
    (K_COMMA,cmd_flip,(1,0)),
    (K_PERIOD,cmd_flip,(0,1)),
    
    (K_UP,cmd_tpick,(0,-1)),
    (K_DOWN,cmd_tpick,(0,1)),
    (K_LEFT,cmd_tpick,(-1,0)),
    (K_RIGHT,cmd_tpick,(1,0)),
    
    (K_F10,cmd_fullscreen,None),
    ]
    

tools = [
    ('draw','draw'),
    ('pixel','pixel'),
    ('line','line'),
    #('ellipse','ellipse'),
    ('fill','fill'),
    ('select','select'),
    ('eraser','eraser'),
    ]


def init_ini():
    ini.read([ini_fname])

def ini_save():
    f = open(ini_fname,"wb")
    ini.write(f)
    f.close()
    

def init_opts():
    usage = "%prog [tiles.tga] [tile_w] [tile_h]"

    parser = OptionParser(usage)
    parser.add_option("--sw",dest="screen_w",help="screen width (app)",type='int')
    parser.add_option("--sh",dest="screen_h",help="screen height (app)",type='int')
    parser.add_option("--tw",dest="tile_w",help="tile width (image)",type='int')
    parser.add_option("--th",dest="tile_h",help="tile height (image)",type='int')
    parser.add_option("--width",dest="width",help="new width (image)",type='int')
    parser.add_option("--height",dest="height",help="new height (image)",type='int')
    parser.add_option("-p","--pal",dest="palette",help="filename of palette (image)")
    parser.add_option("-d","--defaults",dest="defaults",help="set default settings (image)",action="store_true")
    #parser.add_option("-a","--app",dest="app",help="set application level defaults",action="store_true")
    
    (opts,args) = parser.parse_args()
    
    if len(args) > 3: parser.error("incorrect number of arguments")
    
    #parse arguments
    if len(args) == 0:
        opts.fname = "None"
    elif len(args) == 1:
        opts.fname = args[0]
    elif len(args) == 2:
        opts.fname = "None"
        try: opts.tile_w,opts.tile_h = int(args[0]),int(args[1])
        except: parser.error("tile width and height must be integers")
        if opts.tile_w < 1 or opts.tile_h < 1: parser.error("width and height must be greater than 0")
    else:
        try: opts.fname,opts.tile_w,opts.tile_h = args[0],int(args[1]),int(args[2])
        except: parser.error("tile width and height must be integers")
        if opts.tile_w < 1 or opts.tile_h < 1: parser.error("width and height must be greater than 0")
        
    fname = opts.fname
    
    #create all sections
    for k in [fname,"None","app"]:
        if not ini.has_section(k):
            ini.add_section(k)
    
    #set app level defaults
    for k,v in [('screen_w',800),('screen_h',600)]:
        if not ini.has_option('app',k):
            ini.set('app',k,str(v))
            
    #set app level values
    for k in ['screen_w','screen_h']:
        if hasattr(opts,k):
            v = getattr(opts,k)
            if v != None: ini.set('app',k,str(v))
            
    #set default defaults
    for k,v in [('width',256),('height',256),('tile_w',32),('tile_h',32),('palette','palette.tga')]:
        if not ini.has_option('None',k):
            ini.set('None',k,str(v))
    
    #name of keys for normal stuff
    file_ks = ['width','height','tile_w','tile_h','palette']
        
    #set default values
    if opts.defaults:
        for k in file_ks:
            if hasattr(opts,k):
                v = getattr(opts,k)
                if v != None: ini.set('None',k,str(v))
    
    #set fname values
    for k in file_ks:
        if hasattr(opts,k):
            v = getattr(opts,k)
            if v != None: ini.set(fname,k,str(v))
    
    #save the ini
    ini_save()
            
    #convert ini to cfg stuff...
    ini_to_cfg(['app','None',fname])
    if fname == 'None': fname = None
    cfg['fname'] = fname
    
            
def ini_to_cfg(sections):
    global cfg
    ik = ['screen_w','screen_h','tile_w','tile_h','width','height']
    for s in sections:
        for k,v in ini.items(s):
            if k in ik: v = int(v)
            cfg[k] = v
def ini_to_dict(section):
    cfg = {}
    ik = ['screen_w','screen_h','tile_w','tile_h','width','height']
    for s in [section]:
        for k,v in ini.items(s):
            if k in ik: v = int(v)
            cfg[k] = v
    return cfg

def cfg_to_ini(ks,section):
    if not ini.has_section(section): ini.add_section(section)
    for k in ks:
        v = cfg[k]
        ini.set(section,k,str(v))
        
        
def init_gui():
    #themes = cfg['theme'].split(",")
    #gui.theme.load(themes)
    #gui.theme.load(['default','tools'])
    global top
    top = gui.Desktop(theme=gui.Theme(['default','tools']))

    #top = gui.Desktop()
    #top.theme.load(['default','tools'])


    #pass
    
def init_app():
    global app
    app = _app()

    #
    colors_height = 64
    ss = 8
        
    #--- top
    x,y,h = 0,0,0
        
    #menus
    e = gui.Menus(menus)
    e.rect.w,e.rect.h = e.resize()
    app.add(e,x,y)
    x,h = x+e.rect.w,max(h,e.rect.h)
    menus_height = e.rect.h
    
    #--- row
    x,y,h = 0,y+h,0
    
    #--- vspace
    y += ss
    
    #--- hspace
    x += ss
    
    #tools
    e = gui.Toolbox(tools,1,0,value='draw') #,"icons48")
    e.rect.w,e.rect.h = e.resize()
    def _set_mode(value):
        cmd_mode(value.value)
    e.connect(gui.CHANGE,_set_mode,e)
    app.add(e,x,y)

    
    #--- vspace
    y += ss


    #--- switchbox for saving.
    sx, sy = x,y+(max(h,e.rect.h))

    savelabel = gui.Label("Save on")
    app.add(savelabel, sx,sy)
    savelabel2 = gui.Label("focus:")
    app.add(savelabel2, sx,sy+(ss*2))

    #--- vspace
    y += (ss *5)
    sy += (ss *5)

    save_activeevent_switch = gui.Switch(False)
    app.add(save_activeevent_switch, sx,sy)
    app.save_activeevent_switch = save_activeevent_switch

    x,h = x+e.rect.w,max(h,e.rect.h)
    toolbox_width = e.rect.w

    #--- hspace
    x += ss
    y -= ss*6 #undo what was done above to the y val
        
    #tdraw
    #tdraw-calcs
    dw = app.screen_w - (toolbox_width+app.tiles.get_width()+ss*4)
    dh = app.screen_h - (menus_height+colors_height+ss*2)
    if dw/float(app.tile_w) > dh/float(app.tile_h): dw = dh/float(app.tile_h)*app.tile_w
    else: dh = dw/float(app.tile_w)*app.tile_h
    e = app.tdraw = tdraw(dw,dh)
    app.add(e,x,y)
    x,h = x+e.rect.w,max(h,e.rect.h)
    
    #--- hspace
    x += ss
    
    #tpicker
    e = app.tpicker = tpicker()
    e.rect.w,e.rect.h = e.resize()
    #--- right
    x = app.screen_w-e.rect.w-ss
    app.add(e,x,y)
    h = max(h,e.rect.h)

    #tpreview
    y = y+e.rect.h
    e = app.tpreview = tpreview()
    e.rect.w,e.rect.h = e.resize()
    app.add(e,x,y)
    
    #--- bottom
    x,y,h = 0,app.screen_h - colors_height,0
    
    #cpreview
    colors_width = toolbox_width + ss * 2
    e = app.cpreview = cpreview(colors_width,colors_height)
    e.rect.w,e.rect.h = e.resize()
    app.add(e,x,y)
    x,h = x+e.rect.w,max(h,e.rect.h)
    
    #cpicker
    if os.path.isfile(cfg['palette']):
        pal = pygame.image.load(cfg['palette'])
    else:
        #default to EGA / NES palette
        
        pw,ph = 16,6
        pdata = [(0, 0, 0, 255), (0, 0, 170, 255), (0, 170, 0, 255), (0, 170, 170, 255), (170, 0, 0, 255), (170, 0, 170, 255), (170, 85, 0, 255), (170, 170, 170, 255), (85, 85, 85, 255), (85, 85, 255, 255), (85, 255, 85, 255), (85, 255, 255, 255), (255, 85, 85, 255), (255, 85, 255, 255), (255, 255, 85, 255), (255, 255, 255, 255), (0, 0, 0, 255), (0, 0, 0, 255), (0, 0, 0, 255), (0, 0, 0, 255), (0, 0, 0, 255), (0, 0, 0, 255), (0, 0, 0, 255), (0, 0, 0, 255), (0, 0, 0, 255), (0, 0, 0, 255), (0, 0, 0, 255), (0, 0, 0, 255), (0, 0, 0, 255), (0, 0, 0, 255), (0, 0, 0, 255), (0, 0, 0, 255), (255, 255, 255, 255), (173, 243, 255, 255), (223, 214, 255, 255), (255, 190, 255, 255), (255, 176, 255, 255), (255, 177, 237, 255), (255, 191, 185, 255), (255, 217, 145, 255), (237, 246, 128, 255), (185, 255, 138, 255), (145, 255, 173, 255), (128, 255, 223, 255), (138, 255, 255, 255), (197, 197, 197, 255), (0, 0, 0, 255), (0, 0, 0, 255), (255, 255, 255, 255), (129, 200, 255, 255), (179, 171, 255, 255), (231, 146, 255, 255), (255, 132, 244, 255), (255, 133, 194, 255), (255, 148, 141, 255), (244, 173, 101, 255), (194, 202, 84, 255), (141, 227, 94, 255), (101, 240, 129, 255), (84, 240, 179, 255), (94, 225, 231, 255), (120, 120, 120, 255), (0, 0, 0, 255), (0, 0, 0, 255), (192, 192, 192, 255), (57, 128, 200, 255), (108, 99, 217, 255), (160, 74, 207, 255), (200, 61, 172, 255), (217, 61, 122, 255), (207, 76, 70, 255), (172, 102, 30, 255), (122, 130, 13, 255), (70, 155, 23, 255), (30, 169, 57, 255), (13, 168, 108, 255), (23, 153, 160, 255), (61, 61, 61, 255), (0, 0, 0, 255), (0, 0, 0, 255), (128, 128, 128, 255), (16, 87, 159, 255), (67, 58, 176, 255), (119, 34, 166, 255), (159, 20, 131, 255), (176, 20, 81, 255), (166, 35, 29, 255), (131, 61, 0, 255), (81, 89, 0, 255), (29, 114, 0, 255), (0, 128, 16, 255), (0, 127, 67, 255), (0, 112, 119, 255), (0, 0, 0, 255), (0, 0, 0, 255), (0, 0, 0, 255)]

        pal = pygame.Surface((pw,ph),SWSURFACE,32)
        n=0
        for py in range(0,ph):
            for px in range(0,pw):
                pal.set_at((px,py),pdata[n])
                n+=1
        
        
    e = app.cpicker = cpicker(app.screen_w-colors_width,colors_height,pal)
    e.rect.w,e.rect.h = e.resize()
    app.add(e,x,y)
    x,h = x+e.rect.w,max(h,e.rect.h)
    
    pygame.key.set_repeat(500,30)
    
    app.screen.fill((255,255,255,255))
    
class NewDialog(gui.Dialog):
    def __init__(self,**params):
        title = gui.Label("New...")
        
        doc = html.HTML(globals={'gui':gui,'dialog':self},data="""<form id='form'><table>
        <tr>
        <td align=center>Image Size
        <td align=center>Tile Size

        <tr><td colspan='1' align='center' style='padding-right:8px;'><table>
        <tr><td align=right>Width: <td><input type='text' size='4' value='%(width)s' name='width'>
        <tr><td align=right>Height: <td><input type='text' size='4' value='%(height)s' name='height'>
        </table>
        
        <td colspan='1' align='center'><table>
        <tr><td align=right>Width: <td><input type='text' size='4' value='%(tile_w)s' name='tile_w'>
        <tr><td align=right>Height: <td><input type='text' size='4' value='%(tile_h)s' name='tile_h'>
        </table>
        
        <tr><td colspan=2>Palette: <input type='text' size=20 name='palette' value='%(palette)s'>
        
        <tr><td>&nbsp;
        
        <tr><td colspan=2><input type='button' value='Okay' onclick='dialog.send(gui.CHANGE)'> <input type='button' value='Cancel' onclick='dialog.close()'>
        
        </table>"""%ini_to_dict('None'))
        gui.Dialog.__init__(self,title,doc)
        
        self.value = doc['form']

class SaveAsDialog(gui.Dialog):
    def __init__(self,**params):
        title = gui.Label("Save As...")
        
        doc = html.HTML(globals={'gui':gui,'dialog':self},data="""
        <form id='form'>
        
        <table>
        
        <tr><td colspan=2>File Name: <input type='file' size=20 name='fname' value=''>
        
        <tr><td>&nbsp;
        
        <tr><td colspan=2><input type='button' value='Okay' onclick='dialog.send(gui.CHANGE)'> <input type='button' value='Cancel' onclick='dialog.close()'>
        
        </table>""")
        gui.Dialog.__init__(self,title,doc)
        
        self.value = doc['form']

class OpenDialog(gui.Dialog):
    def __init__(self,**params):
        title = gui.Label("Open...")
        
        def load_vals(fname,form):
            if not ini.has_section(fname): return
            
            for k,v in ini.items(fname):
                if k in form:
                    form[k].value = v
        doc = html.HTML(globals={'load_vals':load_vals,'ini':ini,'gui':gui,'dialog':self},data="""<form id='form'><table>
        
        <tr><td align=right>File Name:&nbsp;<td  align=left><input type='file' size=20 name='fname' value='' onchange='load_vals(self.value,form)'>
        <tr><td align=right>Tile Width:&nbsp;<td align=left><input type='text' size='4' value='%(tile_w)s' name='tile_w'>
        <tr><td align=right>Tile Height:&nbsp;<td align=left><input type='text' size='4' value='%(tile_h)s' name='tile_h'>
        
        <tr><td align=right>Palette:&nbsp;<td align=left><input type='text' size=20 name='palette' value='%(palette)s'>
        
        <tr><td>&nbsp;
        
        <tr><td colspan=2><input type='button' value='Okay' onclick='dialog.send(gui.CHANGE)'> <input type='button' value='Cancel' onclick='dialog.close()'>
        
        </table>"""%ini_to_dict('None'))
        gui.Dialog.__init__(self,title,doc)
        
        self.value = doc['form']

class ErrorDialog(gui.Dialog):
    def __init__(self,tt,data,**params):
        title = gui.Label("Error: "+tt)
        data = str(data)
        
        doc = html.HTML(globals={'gui':gui,'dialog':self},data="""
        <form id='form'>
        
        <table>
        <tr><td><h1>&lt;!&gt;&nbsp;</h1>
        <td>"""+data+"""
        <tr><td>&nbsp;
        <tr><td colspan=2><input type='button' value='Okay' onclick='dialog.send(gui.CHANGE);dialog.close()'>
        </table>""")
        gui.Dialog.__init__(self,title,doc)
        
        self.value = doc['form']

class DirtyDialog(gui.Dialog):
    def __init__(self,**params):
        title = gui.Label("File not yet saved...")
        data = "Your file is not yet saved.<br>Are you sure you want to continue?"
        
        doc = html.HTML(globals={'gui':gui,'dialog':self},data="""
        <form id='form'>
        
        <table>
        <tr><td><h1>&lt;!&gt;&nbsp;</h1>
        <td>"""+data+"""
        <tr><td>&nbsp;
        <tr><td colspan=2><input type='button' value='Okay' onclick='dialog.send(gui.CHANGE)'> <input type='button' value='Cancel' onclick='dialog.close()'>
        </table>""")
        gui.Dialog.__init__(self,title,doc)
        
        self.value = doc['form']



def run():
    #top.connect(gui.QUIT,top.quit,None)
    top.connect(gui.QUIT,cmd_quit,None)
    top.connect(pygame.ACTIVEEVENT, cmd_active_save,None)
    top.init(app,app.screen)
    app.top = top
    top.run()
    

def main():
    init_ini()
    init_opts()
    init_gui()
    
    restart = 1
    while restart:
        restart = 0
        try:
            init_app()
            run()
        except Restart: restart = 1
        

        
    
main()
# vim: set filetype=python sts=4 sw=4 noet si :
