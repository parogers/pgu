# theme.py

"""
"""

try:
    from StringIO import StringIO
except:
    from io import StringIO

import os, re
import pygame

try:
    from configparser import ConfigParser
except:
    from ConfigParser import ConfigParser

from .const import *
from . import widget
from . import surface
from .errors import StyleError
from .basic import parse_color, is_color

__file__ = os.path.abspath(__file__)

class Theme(object):
    """Theme interface.
    
    If you wish to create your own theme, create a class with this interface, and 
    pass it to gui.App via gui.App(theme=MyTheme()).
    
    """

    # The cache of style information hashed by the tuple (cls, pcls, attr) where
    #   cls = the class name (eg button)
    #   pcls = the psuedo-class name (eg hover)
    #   attr = the attribute name (eg font)
    config = None

    # A cache of previously created font instances hashed by name and size. This is
    # maintained in addition to the 'config' cache, since the same font (and size)
    # can be used by multiple widgets.
    fontCache = None

    # The directory where the loaded theme is located
    baseThemePath = None

    # Image extensions automatically recognized by the theme class
    image_extensions = (".gif", ".jpg", ".bmp", ".png", ".tga")

    def __init__(self,dirs='default'):
        """Theme constructor.

        Keyword arguments:
            dirs -- Name of the theme dir to load a theme from.  May be an 
                absolute path to a theme, if pgu is not installed, or if you 
                created your own theme.  May include several dirs in a list if 
                data is spread across several themes.
        
        Example:
            theme = gui.Theme("default")
            theme = gui.Theme(["mytheme","mytheme2"])

        """
        self.config = {}
        self._loaded = []
        self.cache = {}
        self._preload(dirs)
        pygame.font.init()
    
    def _preload(self,ds):
        if not isinstance(ds, list):
            ds = [ds]
        for d in ds:
            if d not in self._loaded:
                self._load(d)
            self._loaded.append(d)
    
    def _load(self, name):
        #try to load the local dir, or absolute path
        dnames = [name]
        
        #if the package isn't installed and people are just
        #trying out the scripts or examples
        dnames.append(os.path.join(os.path.dirname(__file__),"..","..","data","themes",name))
        
        #if the package is installed, and the package is installed
        #in /usr/lib/python2.3/site-packages/pgu/
        #or c:\python23\lib\site-packages\pgu\
        #the data is in ... lib/../share/ ...
        dnames.append(os.path.join(os.path.dirname(__file__),"..","..","..","..","share","pgu","themes",name))
        dnames.append(os.path.join(os.path.dirname(__file__),"..","..","..","..","..","share","pgu","themes",name))
        dnames.append(os.path.join(os.path.dirname(__file__),"..","..","share","pgu","themes",name)) 
        for dname in dnames:
            if os.path.isdir(dname): break

        if not os.path.isdir(dname): 
            raise Exception("Could not find theme: %s" % name)

        # Normalize the path to make it look nicer (gets rid of the ..'s)
        dname = os.path.normpath(dname)

        # Empty the font cache
        self.fontCache = {}

        # Try parsing the theme data as an ini file
        fname = os.path.join(dname, "style.ini")
        if os.path.isfile(fname):
            self.baseThemePath = dname
            txt = open(fname).read()
            self.configure(txt, path=dname)
            return

        # Fall back to  parsing the theme in the custom txt file format
        fname = os.path.join(dname,"config.txt")
        if os.path.isfile(fname):
            self.baseThemePath = dname
            try:
                f = open(fname)
                for line in f.readlines():
                    args = line.strip().split()

                    if len(args) < 3:
                        continue

                    pcls = ""
                    (cls, attr, vals) = (args[0], args[1], args[2:])
                    if (":" in cls):
                        (cls, pcls) = cls.split(":")

                    self.config[cls, pcls, attr] = (dname, " ".join(vals))
            finally:
                f.close()
            return

        # The folder probably doesn't contain a theme
        raise IOError("Cannot load theme: missing style.ini")

    def _get(self, cls, pcls, attr):
        key = (cls, pcls, attr)
        if not key in self.config:
            return

        if key in self.cache:
            # This property is already in the cache
            return self.cache[key]

        (dname, value) = self.config[key]

        if (os.path.splitext(str(value).lower())[1] in self.image_extensions):
            # This is an image attribute
            v = pygame.image.load(os.path.join(dname, value))

        elif (attr == "color" or attr == "background"):
            # This is a color value
            v = parse_color(value)

        elif (attr == "font"):
            # This is a font value
            args = value.split()
            name = args[0]
            size = int(args[1])
            try:
                v = self.fontCache[name, size]
            except KeyError:
                if (name.lower().endswith(".ttf")):
                    # Load the font from a file
                    v = pygame.font.Font(os.path.join(dname, name), size)
                else:
                    # Must be a system font
                    v = pygame.font.SysFont(name, size)
                # Cache the font for later
                self.fontCache[name, size] = v

        else:
            try:
                v = int(value)
            except:
                v = value
        self.cache[key] = v
        return v

    # TODO - obsolete, use 'getstyle' below instead
    def get(self,cls,pcls,attr):
        try:
            return self.getstyle(cls, pcls, attr)
        except StyleError:
            return 0

    # Returns the style information, given the class, sub-class and attribute names. 
    # This raises a StylError if the style isn't found.
    def getstyle(self, cls, pcls, attr):
        """Interface method -- get the value of a style attribute.
        
        Arguments:
            cls -- class, for example "checkbox", "button", etc.
            pcls -- pseudo class, for example "hover", "down", etc.
            attr -- attribute, for example "image", "background", "font", "color", etc.
        
        This method is called from gui.style

        """

        if not self._loaded: 
            # Load the default theme
            self._preload("default")

        o = (cls, pcls, attr)
        
        v = self._get(cls, pcls, attr)
        if v: 
            return v
        
        v = self._get(cls, "", attr)
        if v: 
            return v
        
        v = self._get("default", "", attr)
        if v: 
            return v
        
        # The style doesn't exist
        #self.cache[o] = 0
        raise StyleError("Style not defined: '%s', '%s', '%s'" % o)

    def putstyle(self, cls, pcls, attr, *values):
        self.config[cls, pcls, attr] = [".", values]

    def configure(self, txt, path=None):
        if (not path):
            path = self.baseThemePath
        cfg = ConfigParser()
        cfg.readfp(StringIO(txt))
        for section in cfg.sections():
            cls = section
            pcls = ''
            if cls.find(":")>=0:
                cls,pcls = cls.split(":")
            for attr in cfg.options(section):
                value = cfg.get(section,attr).strip()
                key = (cls,pcls,attr)
                self.config[key] = (path, value)
                if (key in self.cache):
                    # Remove the style from the cache
                    del self.cache[key]

    # Draws a box around the surface in the given style
    def box(self, style, surf, rect):
        color = style.border_color
        if (not color):
            color = (0, 0, 0)
        (x, y) = rect.topleft
        (w, h) = rect.size

        surf.fill(color, (x, y, rect.width, style.border_top))
        surf.fill(color, (x, y+h-style.border_bottom, w, style.border_bottom))
        surf.fill(color, (x, y, style.border_left, h))
        surf.fill(color, (x+w-style.border_right, y, style.border_right, h))

    def getspacing(self,w):
        # return the top, right, bottom, left spacing around the widget
        if not hasattr(w,'_spacing'): #HACK: assume spacing doesn't change re pcls
            s = w.style
            xt = s.margin_top+s.border_top+s.padding_top
            xr = s.padding_right+s.border_right+s.margin_right
            xb = s.padding_bottom+s.border_bottom+s.margin_bottom
            xl = s.margin_left+s.border_left+s.padding_left
            w._spacing = xt,xr,xb,xl
        return w._spacing
        
    def resize(self,w,func):
        # Returns the rectangle expanded in each direction
        def expand_rect(rect, left, top, right, bottom):
            return pygame.Rect(rect.x - left, 
                               rect.y - top, 
                               rect.w + left + right, 
                               rect.h + top + bottom)

        def theme_resize(width=None,height=None):
            s = w.style
            
            pt,pr,pb,pl = (s.padding_top,s.padding_right,
                           s.padding_bottom,s.padding_left)
            bt,br,bb,bl = (s.border_top,s.border_right,
                           s.border_bottom,s.border_left)
            mt,mr,mb,ml = (s.margin_top,s.margin_right,
                           s.margin_bottom,s.margin_left)
            # Calculate the total space on each side
            top = pt+bt+mt
            right = pr+br+mr
            bottom = pb+bb+mb
            left = pl+bl+ml
            ttw = left+right
            tth = top+bottom
            
            tilew,tileh = None,None
            if width != None: tilew = width-ttw
            if height != None: tileh = height-tth
            tilew,tileh = func(tilew,tileh)

            if width == None: width = tilew
            if height == None: height = tileh
            
            #if the widget hasn't respected the style.width,
            #style height, we'll add in the space for it...
            width = max(width-ttw, tilew, w.style.width)
            height = max(height-tth, tileh, w.style.height)
            
            #width = max(tilew,w.style.width-tw)
            #height = max(tileh,w.style.height-th)

            r = pygame.Rect(left,top,width,height)
            
            w._rect_padding = expand_rect(r, pl, pt, pr, pb)
            w._rect_border = expand_rect(w._rect_padding, bl, bt, br, bb)
            w._rect_margin = expand_rect(w._rect_border, ml, mt, mr, mb)

            # align it within it's zone of power.   
            rect = pygame.Rect(left, top, tilew, tileh)
            dx = width-rect.w
            dy = height-rect.h
            rect.x += (w.style.align+1)*dx/2
            rect.y += (w.style.valign+1)*dy/2

            w._rect_content = rect

            return (w._rect_margin.w, w._rect_margin.h)
        return theme_resize


    def paint(self,w,func):
        # The function that renders the widget according to the theme, then calls the 
        # widget's own paint function.
        def theme_paint(s):
#             if w.disabled:
#                 if not hasattr(w,'_disabled_bkgr'):
#                     w._disabled_bkgr = s.convert()
#                 orig = s
#                 s = w._disabled_bkgr.convert()

#             if not hasattr(w,'_theme_paint_bkgr'):
#                 w._theme_paint_bkgr = s.convert()
#             else:
#                 s.blit(w._theme_paint_bkgr,(0,0))
#             
#             if w.disabled:
#                 orig = s
#                 s = w._theme_paint_bkgr.convert()

            if w.disabled:
                if (not (hasattr(w,'_theme_bkgr') and 
                         w._theme_bkgr.get_width() == s.get_width() and 
                         w._theme_bkgr.get_height() == s.get_height())):
                    w._theme_bkgr = s.copy()
                orig = s
                s = w._theme_bkgr
                s.fill((0,0,0,0))
                s.blit(orig,(0,0))
                
            if w.background:
                w.background.paint(surface.subsurface(s,w._rect_border))

            self.box(w.style, s, w._rect_border) #surface.subsurface(s,w._rect_border))
            r = func(surface.subsurface(s,w._rect_content))
            
            if w.disabled:
                s.set_alpha(128)
                orig.blit(s,(0,0))
            
            w._painted = True
            return r
        return theme_paint
    
    def event(self,w,func):
        def theme_event(e):
            rect = w._rect_content
            if (not rect):
                # This should never be the case, but it sometimes happens that _rect_content isn't
                # set before a mouse event is received. In this case we'll ignore the event.
                return func(e)

            if e.type == MOUSEBUTTONUP or e.type == MOUSEBUTTONDOWN:
                sub = pygame.event.Event(e.type,{
                    'button':e.button,
                    'pos':(e.pos[0]-rect.x,e.pos[1]-rect.y)})
            elif e.type == CLICK:
                sub = pygame.event.Event(e.type,{
                    'button':e.button,
                    'pos':(e.pos[0]-rect.x,e.pos[1]-rect.y)})
            elif e.type == MOUSEMOTION:
                sub = pygame.event.Event(e.type,{
                    'buttons':e.buttons,
                    'pos':(e.pos[0]-rect.x,e.pos[1]-rect.y),
                    'rel':e.rel})
            else:
                sub = e
            return func(sub)

        return theme_event
    
    def update(self,w,func):
        def theme_update(s):
            if w.disabled: return []
            r = func(surface.subsurface(s,w._rect_content))
            if type(r) == list:
                dx,dy = w._rect_content.topleft
                for rr in r:
                    rr.x,rr.y = rr.x+dx,rr.y+dy
            return r
        return theme_update
        
    def open(self,w,func):
        def theme_open(widget=None,x=None,y=None):
            if not hasattr(w,'_rect_content'):
                # HACK: so that container.open won't resize again!
                w.rect.w,w.rect.h = w.resize()
            rect = w._rect_content
            ##print w.__class__.__name__, rect
            if x != None: x += rect.x
            if y != None: y += rect.y
            return func(widget,x,y)
        return theme_open

    def decorate(self,widget,level):
        """Interface method -- decorate a widget.
        
        The theme system is given the opportunity to decorate a widget 
        methods at the end of the Widget initializer.

        Arguments:
            widget -- the widget to be decorated
            level -- the amount of decoration to do, False for none, True for 
                normal amount, 'app' for special treatment of App objects.
        
        """        

        w = widget
        if level == False: return
        
        if type(w.style.background) != int:
            w.background = Background(w,self)    
        
        if level == 'app': return
        
        for k,v in list(w.style.__dict__.items()):
            if k in ('border','margin','padding'):
                for kk in ('top','bottom','left','right'):
                    setattr(w.style,'%s_%s'%(k,kk),v)

        w.paint = self.paint(w,w.paint)
        w.event = self.event(w,w.event)
        w.update = self.update(w,w.update)
        w.resize = self.resize(w,w.resize)
        w.open = self.open(w,w.open)

    def render(self,surf,box,r,size=None,offset=None):
        """Renders a box using an image.

        Arguments:
            surf -- the target pygame surface
            box -- pygame surface or color
            r -- pygame rect describing the size of the image to render

        If 'box' is a surface, it is interpreted as a 3x3 grid of tiles. The 
        corner tiles are rendered in the corners of the box. The side tiles 
        are used to fill the top, bottom and sides of the box. The centre tile 
        is used to fill the interior of the box.
        """

        if box == 0: return

        if is_color(box):
            surf.fill(box,r)
            return
        
        x,y,w,h=r.x,r.y,r.w,r.h

        if (size and offset):
            pass
#        destx = x
#        desty = y

        # Calculate the size of each tile
        tilew, tileh = int(box.get_width()/3), int(box.get_height()/3)
        xx, yy = x+w, y+h
        src = pygame.rect.Rect(0, 0, tilew, tileh)
        dest = pygame.rect.Rect(0, 0, tilew, tileh)

        # Render the interior of the box
        surf.set_clip(pygame.Rect(x+tilew, y+tileh, w-tilew*2, h-tileh*2))
        src.x,src.y = tilew,tileh
        for dest.y in range(y+tileh,yy-tileh,tileh):
            for dest.x in range(x+tilew,xx-tilew,tilew): 
                surf.blit(box,dest,src)

        # Render the top side of the box
        surf.set_clip(pygame.Rect(x+tilew,y,w-tilew*2,tileh))
        src.x,src.y,dest.y = tilew,0,y
        for dest.x in range(x+tilew, xx-tilew*2+tilew, tilew): 
            surf.blit(box,dest,src)
        
        # Render the bottom side
        surf.set_clip(pygame.Rect(x+tilew,yy-tileh,w-tilew*2,tileh))
        src.x,src.y,dest.y = tilew,tileh*2,yy-tileh
        for dest.x in range(x+tilew,xx-tilew*2+tilew,tilew): 
            surf.blit(box,dest,src)

        # Render the left side
        surf.set_clip(pygame.Rect(x,y+tileh,xx,h-tileh*2))
        src.y,src.x,dest.x = tileh,0,x
        for dest.y in range(y+tileh,yy-tileh*2+tileh,tileh): 
            surf.blit(box,dest,src)

        # Render the right side
        surf.set_clip(pygame.Rect(xx-tilew,y+tileh,xx,h-tileh*2))
        src.y,src.x,dest.x=tileh,tilew*2,xx-tilew
        for dest.y in range(y+tileh,yy-tileh*2+tileh,tileh): 
            surf.blit(box,dest,src)

        # Render the upper-left corner
        surf.set_clip()
        src.x,src.y,dest.x,dest.y = 0,0,x,y
        surf.blit(box,dest,src)
        
        # Render the upper-right corner
        src.x,src.y,dest.x,dest.y = tilew*2,0,xx-tilew,y
        surf.blit(box,dest,src)
        
        # Render the lower-left corner
        src.x,src.y,dest.x,dest.y = 0,tileh*2,x,yy-tileh
        surf.blit(box,dest,src)
        
        # Render the lower-right corner
        src.x,src.y,dest.x,dest.y = tilew*2,tileh*2,xx-tilew,yy-tileh
        surf.blit(box,dest,src)


class Background(widget.Widget):
    def __init__(self,value,theme,**params):
        params['decorate'] = False
        widget.Widget.__init__(self,**params)
        self.value = value
        self.theme = theme
    
    def paint(self, s, size=None, offset=None):
        r = pygame.Rect(0,0,s.get_width(),s.get_height())
        v = self.value.style.background
        self.theme.render(s,v,r, size=size, offset=offset)

