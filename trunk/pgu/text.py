"""a collection of text rendering functions
"""
def write(s,font,pos,color,text,border=1):
    """write text to a surface with a black border
    
    <pre>write(s,font,pos,color,text,border=1)</pre>
    """
    i = font.render(text,1,(0,0,0))
    si = border
    dirs = [(-1,-1),(-1,0),(-1,1),(0,-1),(0,1),(1,-1),(1,0),(1,1)]
    for dx,dy in dirs: s.blit(i,(pos[0]+dx*si,pos[1]+dy*si))
    i = font.render(text,1,color)
    s.blit(i,pos)

def writec(s,font,color,text,border=1):
    """write centered text to a surface with a black border
    
    <pre>writec(s,font,color,text,border=1)</pre>
    """
    w,h = font.size(text)
    x = (s.get_width()-w)/2
    y = (s.get_height()-h)/2
    write(s,font,(x,y),color,text,border)
    
def writepre(s,font,rect,color,text):
    """write preformatted text
    
    <pre>writepre(s,font,rect,color,text)</pre>
    """
    r,c,txt = rect,color,text
    txt = txt.replace("\t","        ")
    i = font.render(" ",1,c)
    sw,sh = i.get_width(),i.get_height()
    y = r.top
    for sentence in txt.split("\n"):
        x = r.left
        i = font.render(sentence,1,c)
        s.blit(i,(x,y))
        y += sh

def writewrap(s,font,rect,color,text):
    """write wrapped text
    
    <pre>writewrap(s,font,rect,color,text)</pre>
    """
    r,c,txt = rect,color,text
    txt = txt.replace("\t","        ")
    i = font.render(" ",1,c)
    sw,sh = i.get_width(),i.get_height()
    y = r.top
    for sentence in txt.split("\n"):
        x = r.left
        for word in sentence.split(" "):
            i = font.render(word,1,c)
            iw,ih = i.get_width(),i.get_height()
            if x+iw > r.right: x,y = r.left,y+sh
            s.blit(i,(x,y))
            x += iw+sw
        y += sh

# vim: set filetype=python sts=4 sw=4 noet si :
