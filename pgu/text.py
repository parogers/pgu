"""A collection of text rendering functions"""

def write(s,font,pos,color,text,border=1):
    """Write text to a surface with a black border"""
    # Render the text in black, at various offsets to fake a border
    tmp = font.render(text,1,(0,0,0))
    dirs = [(-1,-1),(-1,0),(-1,1),(0,-1),(0,1),(1,-1),(1,0),(1,1)]
    for dx,dy in dirs: 
        s.blit(tmp,(pos[0]+dx*border,pos[1]+dy*border))
    # Now render the text properly, in the proper color
    tmp = font.render(text,1,color)
    s.blit(tmp,pos)

def writec(s,font,color,text,border=1):
    """Write centered text to a surface with a black border"""
    # Center the text within the destination surface
    w,h = font.size(text)
    x = (s.get_width()-w)/2
    y = (s.get_height()-h)/2
    write(s,font,(x,y),color,text,border)
    
def writepre(s,font,rect,color,text):
    """Write preformatted text on a pygame surface"""
    r,c,txt = rect,color,text
    txt = txt.replace("\t","        ")
    tmp = font.render(" ",1,c)
    sw,sh = tmp.get_size()
    y = r.top
    for sentence in txt.split("\n"):
        x = r.left
        tmp = font.render(sentence,1,c)
        s.blit(tmp,(x,y))
        y += sh

def writewrap(s, font, rect, color, text, maxlines=None, wrapchar=False):
    """Write wrapped text on a pygame surface.

    maxlines -- specifies the maximum number of lines to write 
        before stopping
    wrapchar -- whether to wrap at the character level, or 
        word level
    """
    r,c,txt = rect,color,text
    txt = txt.replace("\t", " "*8)
    tmp = font.render(" ", 1, c)
    sw,sh = tmp.get_size()
    y = r.top
    row = 1
    done = False
    for sentence in txt.split("\n"):
        x = r.left
        if wrapchar:
            words = sentence
        else:
            words = sentence.split(" ")
            
        for word in words:
            if (not wrapchar):
                word += " "
            tmp = font.render(word, 1, c)
            (iw, ih) = tmp.get_size()
            if (x+iw > r.right):
                x = r.left
                y += sh
                row += 1
                if (maxlines != None and row > maxlines):
                    done = True
                    break
            s.blit(tmp, (x, y))
            #x += iw+sw
            x += iw
        if done:
            break
        y += sh
        row += 1
        if (maxlines != None and row > maxlines):
            break

