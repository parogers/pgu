import sys
sys.path.insert(0, '..')


import pygame
from pygame.locals import *
from pgu import gui


def open_file_browser(arg):
    d = gui.FileDialog()
    d.connect(gui.CHANGE, handle_file_browser_closed, d)
    d.open()
    

def handle_file_browser_closed(dlg):
    if dlg.value: input_file.value = dlg.value



#gui.theme.load('../data/themes/default')
app = gui.Desktop()
app.connect(gui.QUIT,app.quit,None)

main = gui.Container(width=500, height=400) #, background=(220, 220, 220) )


main.add(gui.Label("File Dialog Example", cls="h1"), 20, 20)


td_style = {'padding_right': 10}
t = gui.Table()
t.tr()
t.td( gui.Label('File Name:') , style=td_style )
input_file = gui.Input()
t.td( input_file, style=td_style )
b = gui.Button("Browse...")
t.td( b, style=td_style )
b.connect(gui.CLICK, open_file_browser, None)


main.add(t, 20, 100)

app.run(main)
#import profile
#profile.run('app.run(main)')
