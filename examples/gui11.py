import sys
sys.path.insert(0, '..')


import pygame
from pygame.locals import *
from pgu import gui


_count = 1 # for added items


def clear_list(arg):
    my_list.clear()
    my_list.resize()
    my_list.repaint()

def remove_list_item(arg):
    v = my_list.value
    if v:
        item = v
        my_list.remove(item)
        my_list.resize()
        my_list.repaint()

def add_list_item(arg):
    global _count
    my_list.add("item "+str(_count),value=_count)
    my_list.resize()
    my_list.repaint()
    _count += 1



#theme = gui.Theme('../data/themes/default')
app = gui.Desktop()
app.connect(gui.QUIT,app.quit,None)

main = gui.Container(width=500, height=400) #, background=(220, 220, 220) )


main.add(gui.Label("List Example", cls="h1"), 20, 20)



my_list = gui.List(width=150, height=100)
main.add(my_list, 250, 100)


b = gui.Button("add item", width=150)
main.add(b, 40, 110)
b.connect(gui.CLICK, add_list_item, None)

b = gui.Button("remove selected", width=150)
main.add(b, 40, 140)
b.connect(gui.CLICK, remove_list_item, None)

b = gui.Button("clear", width=150)
main.add(b, 40, 170)
b.connect(gui.CLICK, clear_list, None)





app.run(main)
