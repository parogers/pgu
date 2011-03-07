#!/usr/bin/env python

import pydoc
import os
import site

site.addsitedir("..")

for name in (
    "pgu",
    "pgu.html",
    "pgu.gui",
    "pgu.gui.basic",
    "pgu.gui.app",
    "pgu.gui.area",
    "pgu.gui.basic",
    "pgu.gui.button",
    "pgu.gui.const",
    "pgu.gui.container",
    "pgu.gui.deprecated",
    "pgu.gui.dialog",
    "pgu.gui.document",
    "pgu.gui.form",
    "pgu.gui.group",
    "pgu.gui.__init__",
    "pgu.gui.input",
    "pgu.gui.keysym",
    "pgu.gui.layout",
    "pgu.gui.menus",
    "pgu.gui.misc",
    "pgu.gui.pguglobals",
    "pgu.gui.select",
    "pgu.gui.slider",
    "pgu.gui.style",
    "pgu.gui.surface",
    "pgu.gui.table",
    "pgu.gui.textarea",
    "pgu.gui.theme",
    "pgu.gui.widget",
    "pgu.algo",
    "pgu.ani",
    "pgu.engine",
    "pgu.fonts",
    "pgu.hexvid",
    "pgu.high",
    "pgu.html",
    "pgu.__init__",
    "pgu.isovid",
    "pgu.layout",
    "pgu.text",
    "pgu.tilevid",
    "pgu.timer",
    "pgu.vid"):
    pydoc.writedoc(name)

# Write the index file
fd = open("index.html", "w")
fd.write("""
<html>
<head>
<meta http-equiv="refresh" content="0;pgu.html"> 
</head>
</html>
""")
fd.close()


