Phil's pyGame Utilities
-----------------------
A collection of handy utilities and libraries
created by Phil Hassey.

http://www.imitationpickles.org/pgu/
philhassey@yahoo.com

tileedit  -- edit tga based images
leveledit -- edit tga based levels in tile, isometric, and hexagonal formats
tganew    -- create tga files
levelfancy-- prettyify your levels

gui     -- gui with standard widget, dialogs, html, connections, and themes
html    -- html rendering utilities
layout  -- layout utilities
text    -- text rendering utilities

tilevid -- sprite and tile engine
isovid  -- isometric sprite and tile engine
hexvid  -- hexagonal sprite and tile engine (alpha)
engine  -- state engine
timer   -- a timer for games with set-rate FPS
high    -- high score tracking
ani     -- animation helpers
algo    -- helpful pathfinding algoritms
fonts   -- font wrappers, bitmapped fonts

See LICENSE.txt for license details.

Vera.ttf is from:
http://ftp.gnome.org/pub/GNOME/sources/ttf-bitstream-vera/1.10/
see that site for more information about the font.

See docs for more information.  To build documentation:

$ cd docs
$ python build.py
$ your-favorite-browser index.html

To understand pgu.gui -- read:
http://www.w3.org/TR/REC-html40/
(pgu.gui is based heavily on my HTML background)

To understand the pgu.gui default theme -- read:
http://www.w3.org/TR/REC-CSS2/box.html
(the theme uses the css 2 box model)

To see some examples: 

$ cd examples
$ python gui9.py
$ python gui10.py
$ python tilevid5.py
$ python html5.py # must build docs first

THANKS
======
* gal koren -- bugs, draft of html.HTML, suggestions, bug finding, ScrollArea widget, FileDialog, List, Console
* fdarling -- testing, suggestions, bug fixing, code cleanup, menus & slider UI fixes, new Table class, reorganization of pgu.gui into a package

richard jones -- packaging, suggestions, code cleanup
jhofmann -- tiled preview in tileedit and PIL support
Dr. L. Humbert -- gui.Password widget
illume -- added auto-load features to tile & leveledit
python -- suggestions, bug finding, bug fixing (unicode)
Addison Hardy -- added ScrollArea to html5.py
dang`r`us -- testing, suggestions
piman -- testing, suggestions
coca-cola -- testing
tenoften -- testing
