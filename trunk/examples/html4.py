"""<title>an example of a custom html dialog with python connections</title>"""
import pygame
from pygame.locals import *

# the following line is not needed if pgu is installed
import sys; sys.path.insert(0, "..")

from pgu import gui
from pgu import html

from gui7 import ColorDialog

class NewDialog(gui.Dialog):
    def __init__(self,**params):
        title = gui.Label("New Picture...")
        
        ##Note how the global variables are set for the scripting of HTML
        ##::        
        picker = ColorDialog("#ffffff")
        doc = html.HTML(globals={'gui':gui,'dialog':self,'picker':picker},data="""
<form id='form'>

<table>

<tr><td colspan='2' align='center'>
Size
<tr><td colspan='2' align='center'>
<table>
<tr><td align=right>Width: <td><input type='text' size='4' value='256' name='width'>
<tr><td align=right>Height: <td><input type='text' size='4' value='256' name='height'>
</table>

<tr><td>Format<td>Background

<tr><td>
<input type='radio' name='format' value='rgb' checked> RGB<br>
<input type='radio' name='format' value='bw'> Grayscale
<td>
<input type='radio' name='background' value='#000000'> Black<br>
<input type='radio' name='background' value='#ffffff' checked> White<br>
<input type='radio' name='background' value='custom'> <object type='gui.Color' width=48 height=16 value='#ffffff' name='custom' border=1 onclick='picker.open()'>

<tr><td colspan=2><input type='button' value='Okay' onclick='dialog.send(gui.CHANGE)'> <input type='button' value='Cancel' onclick='dialog.close()'>

</table>

""")
        gui.Dialog.__init__(self,title,doc)
        
        picker.connect(gui.CHANGE,gui.action_setvalue,(picker,doc['form']['custom']))
        ##
        
        self.value = doc['form']



if __name__ == '__main__':
    app = gui.Desktop()
    app.connect(gui.QUIT,app.quit,None)
    
    c = gui.Table(width=640,height=480)
    
    dialog = NewDialog()
    
    ##The dialog's CHANGE event is connected to this function that will display the form values.
    ##::
    def onchange(value):
        print('-----------')
        for k,v in value.value.items():
            print(k,v)
        value.close()
    
    dialog.connect(gui.CHANGE,onchange,dialog)
    ##
            
    e = gui.Button("New")
    e.connect(gui.CLICK,dialog.open,None)
    c.tr()
    c.td(e)
    
    app.run(c)
    #import profile
    #profile.run('app.run(c)')
