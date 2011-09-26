"""<title>an example html forms and scripting</title>"""
import pygame
from pygame.locals import *

# the following line is not needed if pgu is installed
import sys; sys.path.insert(0, "..")

from pgu import gui
from pgu import html

app = gui.Desktop(width=780,height=800)

##::
data = """


<img src='logo.gif' align='center'>
<center>
<h1>pgu forms and scripting demo</h1>
</center>
<hr>

<form id='form'>

<h2 align='center'>Name</h2>


</table>

<table align='center' style='border:1px; border-color: #000088; background: #ccccff; margin: 8px; padding: 8px;'>
<tr><td>



<tr><td>First Name<td style='padding-left:8px'><input type='text' name='firstname' onchange='form["fullname"].value = "%s, %s"%(form["lastname"].value,form["firstname"].value)'>
<tr><td>Last Name<td style='padding-left:8px'><input type='text' name='lastname'
onchange='form["fullname"].value = "%s, %s"%(form["lastname"].value,form["firstname"].value)'>
<tr><td>Full Name<td style='padding-left:8px'><input type='text' name='fullname'>
</table>

<h2 align='center'>Address</h2>
<table align='center' style='border:1px; border-color: #000088; background: #ccccff; margin: 8px; padding: 8px;'>
<tr><td>Address 1<td style='padding-left:8px'><input type='text' name='address1'>
<tr><td>Address 2<td style='padding-left:8px'><input type='text' name='address2'>
<tr><td>City<td style='padding-left:8px'><input type='text' name='city'>
<tr><td>State<td style='padding-left:8px' align=left><input type='text' name='state' size=4> Zip: <input type='text' name='zip' size=10>
</table>

<h2 align='center'>Demographics</h2>
<table align='center' style='border:1px; border-color: #000088; background: #ccccff; margin: 8px; padding: 8px;'>
<tr><td>Age<td style='padding-left:8px' align=left><input type='text' name='age' size=5> Weight: 
<input type='text' name='weight' size=5>
<tr><td>Sex<td style='padding-left:8px' align=left><input type='radio' name='sex' value='male'>Male <input type='radio' name='sex' value='female'>Female
<tr><td>Color<td style='padding-left:8px' align=left><select name='color' onchange='cview.value=self.value'>
<option value='#000000'>Black
<option value='#0000ff'>Blue
<option value='#00ff00'>Green
<option value='#00ffff'>Cyan
<option value='#ff0000'>Red
<option value='#ff00ff'>Purple
<option value='#ffff00'>Yellow
<option value='#ffffff'>White
</select>
 <object type='gui.Color' width=80 height=20 border=1 id='cview'>
<tr><td>Pets<td style='padding-left:8px' align=left>
<table><tr><td align=left><input type='checkbox' name='pets' value='goat'> Goat <td align=left><input type='checkbox' name='pets' value='horse'> Horse <tr><td align=left><input type='checkbox' name='pets' value='hog'> Hog <td align=left><input type='checkbox' name='pets' value='cow'> Cow </table>
</table>

<center>
<input type='submit' value='Submit' onclick='print(form.results())'>
</center>

</form>

"""
##

doc = html.HTML(data,align=-1,valign=-1)

app.connect(gui.QUIT,app.quit,None)
app.run(doc)
