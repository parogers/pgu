"""<title>an example of html within gui</title>"""
import pygame
from pygame.locals import *

# the following line is not needed if pgu is installed
import sys; sys.path.insert(0, "..")

from pgu import gui
from pgu import html

app = gui.Desktop(width=780,height=500)

data = """
<h1>header 1</h1>
<h2>header 2</h2>
<h3>header 3</h3>
<p>this is normal <b>this is bold</b> <i>this is italic</i> <u>this is underline</u></p>

<table border=1 bgcolor='yellow' width=200 align=center>
    <tr>
    <th bgcolor='#ffffee'>pgu
    <th bgcolor='red'>red
    <th bgcolor='green'>green
    <th bgcolor='blue'>blue
    
    <tr>
    <td bgcolor='white' border=1><img src='logo.gif'>
    <td border=1 style='padding:4px'>things:<br>apples,<br>fire trucks,<br>crabs,<br>and cherries
    <td border=1 style='padding:4px'>things: <ul>
        <li>grass
        <li>trees
        <li>snakes
        <li>scum
        </ul>
    <td border=1 style='padding:4px'>things: <ol>
        <li>water
        <li>sky
        <li>goats
        <li>pizza
        </ol>
</table>
    
<pre>    
class Desktop(App):
    def __init__(self,**params):
        params.setdefault('cls','desktop')
        App.__init__(self,**params)
</pre>

<div style='margin: 8px; padding: 8px; border: 1px; border-color: #88ffff; background: #eeffff;' width=700><img src='cuzco.png' align=right>cuzco is my goat. cuzco is my goat. cuzco is my goat. cuzco is my goat. cuzco is my goat. cuzco is my goat. cuzco is my goat. cuzco is my goat. cuzco is my goat. cuzco is my goat. cuzco is my goat. cuzco is my goat. cuzco is my goat. cuzco is my goat. </div>"""

##this example just uses the HTML widget
##::
doc = html.HTML(data)
##

app.connect(gui.QUIT,app.quit,None)
app.run(doc)
