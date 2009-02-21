import os,sys
import re

todo = [
    ('Scripts','scripts',
        ['tileedit','leveledit','tganew','levelfancy']),
    ('Reference','pgu',
        ['algo','ani','engine','fonts','high','html','layout','text','timer','vid',]),
    ('Tutorials','examples',
        ['tilevid1','tilevid2','tilevid3','tilevid4','tilevid5',]),

    ('GUI Ref.','pgu',[
        'gui.theme',
        'gui.style',
        'gui.widget',
        'gui.surface',
        'gui.const',]),
    
    ('Containers','pgu',[
        'gui.container',
        'gui.app',
        'gui.table',
        'gui.document',
        #'gui.html',
        'gui.area',
        ]),
        
    ('Forms','pgu',[
        'gui.form',
        'gui.group',
        ]),
        
    ('Widgets','pgu',[
        'gui.basic',
        'gui.button',
        'gui.input',
        'gui.keysym',
        'gui.slider',
        'gui.select',
        'gui.misc',
        ]),
        
    ('Other','pgu',[
        'gui.menus',
        'gui.dialog',
        ]),

    ('Tutorials','examples',
        ['gui1','gui2','gui3','gui4','gui5','gui6','gui7','gui8','gui9','gui10',]),
    
    ]
    


class Handler:
    """Handler interface, for handling doc parsing."""
    def line_(self,data):
        pass
        
    def class_(self,name,data):
        pass
        
    def method_(self,name,data):
        pass
        
    def function_(self,name,data):
        pass
        
    def doc_(self,indent,data):
        pass
    
    def code_(self,n,data):
        pass
    
    def comment_(self,data):
        pass
        
        

class TestHandler: 
    def line_(self,data):
        print 'line',data
        
    def class_(self,name,data):
        print 'class',name,data
        
    def method_(self,name,data):
        print 'method',name,data
        
    def function_(self,name,data):
        print 'function',name,data
        
    def doc_(self,indent,data):
        print 'doc',indent,data
        
def doc_indent(indent,data):
    r = []
    n = 0
    for line in data.split('\n'):
        if not n: r.append(line)
        else: r.append(indent+line)
        n += 1
    return indent+'"""'+('\n'.join(r))+'"""'

           
class BasicHandler(Handler):
    def line_(self,data):
        print data
        
    def doc_(self,indent,data):
        print doc_indent(indent,data)

        
class NameHandler(Handler):
    def __init__(self):
        self.name = ''
        self.level = 0
        self.sections = []

    def class_(self,name,data):
        self._class = name
        self.name = "%s"%(self._class)
        self.level = 1
        self.sections.append((self.level,self.name))
        
    def method_(self,name,data):
        self._method = name
        self.name = "%s.%s"%(self._class,self._method)
        self.level = 2
        self.sections.append((self.level,self.name))
        
    def function_(self,name,data):
        self._function = name
        self.name = "%s"%(self._function)
        self.level = 1
        self.sections.append((self.level,self.name))
    
class ReplaceHandler(NameHandler):
    def __init__(self,replace):
        NameHandler.__init__(self)
        self.replace = replace
    
    def line_(self,data):
        print data
    
    def doc_(self,indent,data):
        if self.name in self.replace: 
            data = self.replace[self.name]
        print doc_indent(indent,data)
    
    
class HTMLHandler(NameHandler):
    def __init__(self):
        NameHandler.__init__(self)
        
    def doc_(self,indent,data):
        l = self.level+1
        if l > 1: print '<h%d>%s</h%d>'%(l,self.name,l)
        print data

class FancyHTMLHandler(NameHandler):
    def __init__(self):
        NameHandler.__init__(self)
        
    def doc_(self,indent,data):
        l = self.level+1
        print '<a name="%s">'%self.name
        if l > 1: print '<h%d>%s</h%d>'%(l,self.name,l)
        print '<div class="h%d">'%l
        data = data.replace("<code>","<pre>")
        data = data.replace("</code>","</pre>")
        print data
        print '</div>'
        
    def code_(self,n,data):
        print '<pre>'
        for line in data:
            print '%4d:%s'%(n,line)
            n += 1
        print '</pre>'
    def comment_(self,data):
        #print '%s<br>'%data
        print data
              
def _parse_remove_indent(indent,line):
    end = 0
    for n in xrange(0,min(len(indent),len(line))):
        if line[n] == ' ': end = n+1
    return line[end:]
        
def py_parse(h,fname):
    f = open(fname)
    lines = f.readlines()
    f.close()
    
    isclass = re.compile('^class ([a-zA-Z0-9_]*)\(*(.*?)\)*:')
    ismethod = re.compile('^\s+def ([a-zA-Z0-9_]*)\(self,*(.*)\)')
    isfunction = re.compile('^def ([a-zA-Z0-9_]*)\((.*)\)')
    
    startdoc = re.compile('^(\s*)"""(.*)$')
    linedoc = re.compile('^(\s*)"""(.*)"""$')
    indoc = False
    enddoc = re.compile('^(.*)"""$')
    
    iscomment = re.compile('^\s*##(.*)$')
    incode = False
    
    n = 1
    
    for line in lines:
        line = line.rstrip().replace("\t","    ")
        
        if not indoc:
            m = isclass.match(line)
            if m: h.class_(m.group(1),m.group(2))
            m = ismethod.match(line)
            if m: h.method_(m.group(1),m.group(2))
            m = isfunction.match(line)
            if m: h.function_(m.group(1),m.group(2))

        done = False
        
        if not done:
            m = linedoc.match(line)
            if m:
                indent,doc = m.group(1),m.group(2)
                h.doc_(indent,doc)
                done = True
                
        if not done and indoc == True:       
            m = enddoc.match(line)
            if m:
                doc = doc + "\n" + _parse_remove_indent(indent,m.group(1))
                h.doc_(indent,doc)
                indoc = False
                done = True
        
        if not done and indoc == False:
            m = startdoc.match(line)
            if m: 
                indoc = True
                indent,doc = m.group(1),m.group(2)
                done = True
                
        if not done and indoc == True:
            doc = doc + "\n" + _parse_remove_indent(indent,line)
            done = True
            
        m = iscomment.match(line)
        if not done and m:
            comment = m.group(1)
            if comment == '::':
                incode = True
                code_start = n
                code_lines = []
            elif incode == True:
                h.code_(code_start,code_lines)
                incode = False
            else:
                h.comment_(comment)
            done = True
            
        if not done and incode == True:
            code_lines.append(line)
        
        if not done:
            h.line_(line)
            
        n += 1
        
        
def html_read(fname):
    f = open(fname)
    lines = f.readlines()
    f.close()
    issection = re.compile('<h\d\>(.*)\<\/h\d>')
    r = {}
    name = ''
    doc = ''
    for line in lines:
        line = line.rstrip().replace("\t","    ").replace('"""','***')
        m = issection.match(line)
        if m:
            r[name] = doc.rstrip()
            name = m.group(1)
            doc = ''
        else:
            doc = doc + line + "\n"
    r[name] = doc.rstrip()
    return r

    
class StringStream:
    def __init__(self):
        self._lines = []
    def write(self,line):
        self._lines.append(line)
    def readlines(self): 
        return self._lines
    


class Page: pass

pages = {}

for title,srcdir,names in todo:
    for name in names:
        destdir = '.'
        ext = '.html'
        fnames = [name,os.path.join(*name.split("."))+'.py']
        for fname in fnames: 
            src = os.path.join("..",srcdir,fname)
            if os.path.isfile(src): break
        dest = name+ext
        
        e = Page()
        e.link = e.name = e.title = name
        e.fname = dest
        
        e.link = e.link.replace("gui.","")
        e.link = e.link.replace("gui","")
        e.link = e.link.replace("tilevid","")
        
        _stdout = sys.stdout
        s = sys.stdout = StringStream()
        
        h = FancyHTMLHandler()
        py_parse(h,src)
        
        sys.stdout = _stdout
        e.content = content = ''.join(s.readlines())
        
        sections = []
        for level,nm in h.sections:
                if '>%s<'%nm in content:
                    sections.append((level,nm))
        e.sections = sections

        f = open(dest,'w')
        
        gettitle = re.compile('<title>(.*?)<\/title>')
        m = gettitle.search(content)
        if m:
            content = gettitle.sub("",content)
            e.title = m.group(1)
        e.content = content
        
        pages[name] = e
        #"""
        
        
_stdout = sys.stdout
s = sys.stdout = StringStream()

for title,srcdir,names in todo:
    print "<strong>%s</strong><br>"%title.replace(" ",'&nbsp;')
    pre = ''
    for name in names:
        e = pages[name]
        print pre+'<a href="%s">%s</a>'%(e.fname,e.link)
        pre = ' | '
    print '<br><br>'
    
sys.stdout = _stdout
links = ''.join(s.readlines())
        

e = Page()
e.name = 'index'
e.title = 'Overview'
e.fname = 'index.html'
e.sections = []
_stdout = sys.stdout
s = sys.stdout = StringStream()

for title,srcdir,names in todo:
    print '<h2>'+title+'</h2>'
    for name in names:
        ee = pages[name]
        print '<a href="%s">%s</a> - %s<br>'%(ee.fname,ee.name,ee.title)
    
sys.stdout = _stdout
e.content = ''.join(s.readlines())

pages['index'] = e

        
        
        
for name,e in pages.items():
    reps = {}
    
    reps['__TITLE__'] = e.title
    reps['__NAME__'] = e.name
    reps['%%'] = e.content
    reps['__LINKS__'] = links
    
    _stdout = sys.stdout
    s = sys.stdout = StringStream()
    
    if len(e.sections) > 1:
        print "<table class='sections' align=right>";
        print "<tr><th>sections</th>";
        for level,name in e.sections:
            print "<tr><td class='h%d'><a href='#%s'>%s</a>"%(level,name,name)
        print "</table>"
    
    sys.stdout = _stdout
    reps['__SECTIONS__'] = ''.join(s.readlines())
    
    f = open(os.path.join(destdir,e.fname),'w')
    skin = open(os.path.join('skin','index.html'),'r')
    for line in skin.readlines():
        for k,v in reps.items():
            line = line.replace(k,v)
            line = line.replace('<dd>','<p class="dd">')
        f.write(line)
    skin.close()
    f.close()
