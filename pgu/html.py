"""Code for html rendering
"""

import sys

# Import the html parser code, maintaing compatibility with older versions of python
if (sys.version_info[0] < 3):
    # Import the old style htmllib parser
    import htmllib
    from htmllib import HTMLParser
else:
    # Import the new html.parser module
    from html.parser import HTMLParser
    htmllib = None

import re
import pygame
from pygame.locals import *

from pgu import gui

_amap = {'left':-1,'right':1,'center':0,None:None,'':None,}
_vamap = {'top':-1,'bottom':1,'center':0,'middle':0,None:None,'':None,}

# Used by the HTML parser to load external resources (like images). This 
# class loads content from the local file system. But you can pass your own 
# resource loader to the HTML parser to find images by other means.
class ResourceLoader(object):
    # Loads an image and returns it as a pygame image
    def load_image(this, path):
        return pygame.image.load(path)

class _dummy:
    pass

class _flush:
    def __init__(self):
        self.style = _dummy()
        self.style.font = None
        self.style.color = None
        self.cls = None
    def add(self,w): pass
    def space(self,v): pass
    
class _hr(gui.Color):
    def __init__(self,**params):
        gui.Color.__init__(self,(0,0,0),**params)
    def resize(self,width=None,height=None):
        w,h = self.style.width,self.style.height
        #if width != None: self.rect.w = width
        #else: self.rect.w = 1
        
        #xt,xr,xb,xl = self.getspacing()

        if width != None: w = max(w,width)
        if height != None: h = max(h,height)        
        w = max(w,1)
        h = max(h,1)
        
        return w,h #self.container.rect.w,h
        
        #self.rect.w = max(1,width,self.container.rect.w-(xl+xr))
        
        #print self.rect
        #self.rect.w = 1

class _html(HTMLParser):
    def init(self,doc,font,color,_globals,_locals,loader=None):
        self.mystack = []
        self.document = doc
        if (loader):
            self.loader = loader
        else:
            # Use the default resource loader
            self.loader = ResourceLoader()
        self.myopen('document',self.document)
        
        self.myfont = self.font = font
        self.mycolor = self.color = color
        
        self.form = None
        
        self._globals = _globals
        self._locals = _locals
        
    def myopen(self,type_,w):
    
        self.mystack.append((type_,w))
        self.type,self.item = type_,w
        
        self.font = self.item.style.font
        self.color = self.item.style.color
        
        if not self.font: self.font = self.myfont
        if not self.color: self.color = self.mycolor
        
    def myclose(self, tag):
        self.mydone()
        n = len(self.mystack)-1
        while (n >= 0):
            (t, w) = self.mystack[n]
            if (t == tag):
                # Found the tag in the stack. Drop everything from that tag onwards
                # from the stack.
                self.mystack = self.mystack[0:n]
                # Pop off the parent element, then add it back on to set the
                # font, color, etc.
                # TODO - tacky
                t,w = self.mystack.pop()
                self.myopen(t,w)
                break
            n -= 1

#        t = None
#        while t != type_:
#            if len(self.mystack)==0:
#                # Closing a tag that was never opened
#                break
#            t,w = self.mystack.pop()
#        t,w = self.mystack.pop()
#        self.myopen(t,w)
        
    def myback(self,type_):
        if type(type_) == str: type_ = [type_,]
        self.mydone()
        #print 'myback',type_
        t = None
        while t not in type_:
            #if len(self.mystack)==0: return
            t,w = self.mystack.pop()
        self.myopen(t,w)
        
    def mydone(self):
        #clearing out the last </p>
        if not hasattr(self.item,'layout'): return 
        if len(self.item.layout._widgets) == 0: return 
        w = self.item.layout._widgets[-1]
        if type(w) == tuple:
            del self.item.layout._widgets[-1]

        
    def start_b(self,attrs): self.font.set_bold(1)
    def end_b(self): self.font.set_bold(0)
    def start_i(self,attrs): self.font.set_italic(1)
    def end_i(self): self.font.set_italic(0)
    def start_u(self,attrs): self.font.set_underline(1)
    def end_u(self): self.font.set_underline(0)
    def start_br(self,attrs): self.do_br(attrs)
    def do_br(self,attrs): self.item.br(self.font.size(" ")[1])
    def attrs_to_map(self,attrs):
        k = None
        r = {}
        for k,v in attrs: r[k] = v
        return r
        
    def map_to_params(self,r):
        anum = re.compile("\D")
        
        params = {'style':{}}
        style = params['style']

        if 'bgcolor' in r: 
            style['background'] = gui.parse_color(r['bgcolor'])
        if 'background' in r: 
            style['background'] = self.loader.load_image(r['background'])
        if 'border' in r: style['border'] = int(r['border'])
            
        for k in ['width','height','colspan','rowspan','size','min','max']:
            if k in r: params[k] = int(anum.sub("",r[k]))
            
        for k in ['name','value']:
            if k in r: params[k] = r[k]
        
        if 'class' in r: params['cls'] = r['class']
        
        if 'align' in r: 
            params['align'] = _amap[r['align']]
        if 'valign' in r:
            params['valign'] = _vamap[r['valign']]

        if 'style' in r:
            for st in r['style'].split(";"):
                #print st
                if ":" in st:
                    #print st.split(":")
                    k,v = st.split(":")
                    k = k.replace("-","_")
                    k = k.replace(" ","")
                    v = v.replace(" ","")
                    if k == 'color' or k == 'border_color' or k == 'background':
                        v = gui.parse_color(v)
                    else:
                        v = int(anum.sub("",v))
                    style[k] = v
        return params
        
    def map_to_connects(self,e,r):
        for k,evt in [('onclick',gui.CLICK),('onchange',gui.CHANGE)]: #blah blah blah
            
            if k in r:
                #print k,r[k]
                e.connect(evt,self.myexec,(e,r[k]))

    def start_p(self,attrs):
        r = self.attrs_to_map(attrs)
        align = r.get("align","left")
        
        self.check_p()
        self.item.block(_amap[align])
        
    def check_p(self):
        if len(self.item.layout._widgets) == 0: return
        if type(self.item.layout._widgets[-1]) == tuple:
            w,h = self.item.layout._widgets[-1]
            if w == 0: return
        self.do_br(None)
        
    def end_p(self):
        #print 'end p'
        self.check_p()
        
        
    def start_block(self,t,attrs,align=-1):
        r = self.attrs_to_map(attrs)
        params = self.map_to_params(r)
        if 'cls' in params: params['cls'] = t+"."+params['cls']
        else: params['cls'] = t
        b = gui.Document(**params)
        b.style.font = self.item.style.font
        if 'align' in params:
            align = params['align']
        self.item.block(align)
        self.item.add(b)
        self.myopen(t,b)

        
                
    def end_block(self,t):
        self.myclose(t)
        self.item.block(-1)
        
    def start_div(self,attrs): self.start_block('div',attrs)
    def end_div(self): self.end_block('div')
    def start_center(self,attrs): self.start_block('div',attrs,0)
    def end_center(self): self.end_block('div')
    
    def start_h1(self,attrs): self.start_block('h1',attrs)
    def end_h1(self): self.end_block('h1')
    def start_h2(self,attrs): self.start_block('h2',attrs)
    def end_h2(self): self.end_block('h2')
    def start_h3(self,attrs): self.start_block('h3',attrs)
    def end_h3(self): self.end_block('h3')
    def start_h4(self,attrs): self.start_block('h4',attrs)
    def end_h4(self): self.end_block('h4')
    def start_h5(self,attrs): self.start_block('h5',attrs)
    def end_h5(self): self.end_block('h5')
    def start_h6(self,attrs): self.start_block('h6',attrs)
    def end_h6(self): self.end_block('h6')

    def start_ul(self,attrs): self.start_block('ul',attrs)
    def end_ul(self): self.end_block('ul')
    def start_ol(self,attrs): 
        self.start_block('ol',attrs)
        self.item.counter = 0
    def end_ol(self): self.end_block('ol')
    def start_li(self,attrs): 
        self.myback(['ul','ol'])
        cur = self.item
        self.start_block('li',attrs)
        if hasattr(cur,'counter'):
            cur.counter += 1
            self.handle_data("%d. "%cur.counter)
        else:
            self.handle_data("- ")
    #def end_li(self): self.end_block('li') #this isn't needed because of how the parser works

    def start_pre(self,attrs): self.start_block('pre',attrs)
    def end_pre(self): self.end_block('pre')
    def start_code(self,attrs): self.start_block('code',attrs)
    def end_code(self): self.end_block('code')
            
    def start_table(self,attrs):
        r = self.attrs_to_map(attrs)
        params = self.map_to_params(r)
        
        align = r.get("align","left")
        self.item.block(_amap[align])

        t = gui.Table(**params)
        self.item.add(t)
        
        self.myopen('table',t)
        
    def start_tr(self,attrs):
        self.myback('table')
        self.item.tr()
        
    def _start_td(self,t,attrs):
        r = self.attrs_to_map(attrs)
        params = self.map_to_params(r)
        if 'cls' in params: params['cls'] = t+"."+params['cls']
        else: params['cls'] = t
        b = gui.Document(cls=t)
        
        self.myback('table')
        self.item.td(b,**params)
        self.myopen(t,b)
    
        self.font = self.item.style.font
        self.color = self.item.style.color
        
    def start_td(self,attrs):
        self._start_td('td',attrs)
    
    def start_th(self,attrs):
        self._start_td('th',attrs)
        
    def end_table(self):
        self.myclose('table')
        self.item.block(-1)
        
    def start_form(self,attrs):
        r = self.attrs_to_map(attrs)
        e = self.form = gui.Form()
        e.groups = {}
        
        self._locals[r.get('id',None)] = e
        
    def start_input(self,attrs):
        r = self.attrs_to_map(attrs)
        params = self.map_to_params(r) #why bother
        #params = {}
        
        type_,name,value = r.get('type','text'),r.get('name',None),r.get('value',None)
        f = self.form
        if type_ == 'text':
            e = gui.Input(**params)
            self.map_to_connects(e,r)
            self.item.add(e)
        elif type_ == 'radio':
            if name not in f.groups:
                f.groups[name] = gui.Group(name=name)
            g = f.groups[name]
            del params['name']
            e = gui.Radio(group=g,**params)
            self.map_to_connects(e,r)
            self.item.add(e)
            if 'checked' in r: g.value = value
        elif type_ == 'checkbox':
            if name not in f.groups:
                f.groups[name] = gui.Group(name=name)
            g = f.groups[name]
            del params['name']
            e = gui.Checkbox(group=g,**params)
            self.map_to_connects(e,r)
            self.item.add(e)
            if 'checked' in r: g.value = value

        elif type_ == 'button':
            e = gui.Button(**params)
            self.map_to_connects(e,r)
            self.item.add(e)
        elif type_ == 'submit':
            e = gui.Button(**params)
            self.map_to_connects(e,r)
            self.item.add(e)
        elif type_ == 'file':
            e = gui.Input(**params)
            self.map_to_connects(e,r)
            self.item.add(e)
            b = gui.Button(value='Browse...')
            self.item.add(b)
            def _browse(value):
                d = gui.FileDialog();
                d.connect(gui.CHANGE,gui.action_setvalue,(d,e))
                d.open();
            b.connect(gui.CLICK,_browse,None)

        self._locals[r.get('id',None)] = e

    def start_object(self,attrs):
        r = self.attrs_to_map(attrs)
        params = self.map_to_params(r)
        # Use eval to automagically get the class being refered
        cls = eval(r["type"])
        e = cls(**params)
        self.map_to_connects(e,r)
        self.item.add(e)
        self._locals[r.get('id',None)] = e
    
    def start_select(self,attrs):
        r = self.attrs_to_map(attrs)
        params = {}
        
        name,value = r.get('name',None),r.get('value',None)
        e = gui.Select(name=name,value=value,**params)
        self.map_to_connects(e,r)
        self.item.add(e)
        self.myopen('select',e)
        
    def start_option(self,attrs):
        r = self.attrs_to_map(attrs)
        params = {} #style = self.map_to_style(r)
        
        self.myback('select')
        e = gui.Document(**params)
        self.item.add(e,value=r.get('value',None))
        self.myopen('option',e)
        
        
    def end_select(self):
        self.myclose('select')
        
    def start_hr(self,attrs):
        self.do_hr(attrs)
    def do_hr(self,attrs):
        h = self.font.size(" ")[1]/2
        
        r = self.attrs_to_map(attrs)
        params = self.map_to_params(r)
        params['style']['padding'] = h

        self.item.block(0)
        self.item.add(_hr(**params))
        self.item.block(-1)
        
    def anchor_begin(self,href,name,type_):
        pass

    def anchor_end(self):
        pass
        
    def start_title(self,attrs): self.myopen('title',_flush())
    def end_title(self): self.myclose('title')
            
    def myexec(self,value):
        w,code = value
        g = self._globals
        l = self._locals
        l['self'] = w
        exec(code,g,l)
        
    def handle_image(self,src,alt,ismap,align,width,height):
        try:
            w = gui.Image(self.loader.load_image(src))
            if align != '':
                self.item.add(w,_amap[align])
            else:
                self.item.add(w)
        except:
            print('handle_image: missing %s'%src)
                
    def handle_data(self,txt):
        if self.type == 'table': return 
        elif self.type in ('pre','code'): 
            txt = txt.replace("\t","        ")
            ss = txt.split("\n")
            if ss[-1] == "": del ss[-1]
            for sentence in ss:
                img = self.font.render(sentence,1,self.color)
                w = gui.Image(img)
                self.item.add(w)
                self.item.block(-1)
            return

        txt = re.compile("^[\t\r\n]+").sub("",txt)
        txt = re.compile("[\t\r\n]+$").sub("",txt)
        
        tst = re.compile("[\t\r\n]+").sub("",txt)
        if tst == "": return
        
        txt = re.compile("\s+").sub(" ",txt)
        if txt == "": return
        
        if txt == " ":
            self.item.space(self.font.size(" "))
            return
        
        for word in txt.split(" "):
            word = word.replace(chr(160)," ") #&nbsp;
            #print self.item.cls
            w = gui.Image(self.font.render(word,1,self.color))
            self.item.add(w)
            self.item.space(self.font.size(" "))

if (sys.version_info[0] >= 3):
    # These functions are for compatibility with python 3, where it seems that HTMLParser 
    # was rewritten to be more general. There is a problem though, since python pre 3 
    # defines these same functions with an extra argument. So we have to include them
    # conditionally, depending on whether we're using python 2 or 3. Ugh.
    def handle_starttag(this, tag, attrs):
        func = getattr(this, "start_" + tag, None)
        if (not func):
            print("ERROR - unrecognized tag %s" % tag)
            return
        func(attrs)

    def handle_endtag(this, tag):
        func = getattr(this, "end_" + tag, None)
        if (func):
            func()

    def start_img(this, attrs):
#        src = ""
#        align = ""
#        for (key, value) in attrs:
#            if (key == "src"): src = value
#            elif (key == "align"): align = value
        args = this.attrs_to_map(attrs)
        src = args.get("src", "")
        align = args.get("align", "")
        this.handle_image(src, "", "", align, "", "")

    _html.handle_starttag = handle_starttag
    _html.handle_endtag = handle_endtag
    _html.start_img = start_img


class HTML(gui.Document):
    """A gui HTML object

    Arguments:
        data -- html data
        globals -- global variables (for scripting)
        locals -- local variables (for scripting)
        loader -- the resource loader
    
    You may access html elements that have an id via widget[id]

    """
    def __init__(self,data,globals=None,locals=None,loader=None,**params):
        gui.Document.__init__(self,**params)
        # This ensures that the whole HTML document is left-aligned within
        # the rendered surface.
        self.style.align = -1
        
        _globals,_locals = globals,locals
        
        if _globals == None: _globals = {}
        if _locals == None: _locals = {}
        self._globals = _globals
        self._locals = _locals
        
        #font = gui.theme.get("label","","font")
        if (htmllib):
            # The constructor is slightly different
            p = _html(None, 0)
        else:
            p = _html()
        p.init(self,self.style.font,self.style.color,_globals,_locals,
               loader=loader)
        p.feed(data) 
        p.close() 
        p.mydone()
        
        
    def __getitem__(self,k):
        return self._locals[k]

    # Returns a box (pygame rectangle) surrounding all widgets in this document
    def get_bounding_box(this):
        minx = miny = sys.maxint
        maxx = maxy = -sys.maxint
        for e in this.layout.widgets:
            minx = min(minx, e.rect.left)
            miny = min(miny, e.rect.top)
            maxx = max(maxx, e.rect.right+1)
            maxy = max(maxy, e.rect.bottom+1)
        return pygame.Rect(minx, miny, maxx-minx, maxy-miny)


def render_ext(font, rect, text, aa, color, bgcolor=(0,0,0,0), **params):
    """Renders some html and returns the rendered surface, plus the
    HTML instance that produced it.
    """

    htm = HTML(text, font=font, color=color, **params)

    if (rect == -1):
        # Make the surface large enough to fit the rendered text
        htm.resize(width=sys.maxint)
        (width, height) = htm.get_bounding_box().size
        # Now set the proper document width (computed from the bounding box)
        htm.resize(width=width)
    elif (type(rect) == int):
        # Fix the width of the document, while the height is variable
        width = rect
        height = htm.resize(width=width)[1]
    else:
        # Otherwise the width and height of the document is fixed
        (width, height) = rect.size
        htm.resize(width=width)

    # Now construct a surface and paint to it
    surf = pygame.Surface((width, height)).convert_alpha()
    surf.fill(bgcolor)
    htm.paint(surf)
    return (surf, htm)

def render(font, rect, text, aa, color, bgcolor=(0,0,0,0), **params):
    """Renders some html"""
    return render_ext(font, rect, text, aa, color, bgcolor, **params)[0]

def rendertrim(font,rect,text,aa,color,bgcolor=(0,0,0,0),**params):
    """Render html, and make sure to trim the size."""
    # Render the HTML
    (surf, htm) = render_ext(font, rect, text, aa, color, bgcolor, **params)
    return surf.subsurface(htm.get_bounding_box())

    
def write(s,font,rect,text,aa=0,color=(0,0,0), **params):
    """Write html to a surface."""
    htm = HTML(text, font=font, color=color, **params)
    htm.resize(width=rect.w)
    s = s.subsurface(rect)
    htm.paint(s)
    

