PGU - PyGame Utilities
======================

Install
--------

pip install pygame-pgu


*NOTE* PGU is in need of more contributors. Email me (peter.rogers@gmail.com)
or jsobueno@gmail.com if you're interested in evolving the codebase.

I (jsbueno) am giving some care to this code basic, and likely
making a Python-3 only release soon.

A collection of handy utilities and libraries created by Phil Hassey, released
under the LGPL v2.1 (see LICENSE.txt for more details).

The current PGU code base:

    https://github.com/parogers/pgu

Old website location:

    http://www.imitationpickles.org/pgu/
    philhassey@yahoo.com



Modules:

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

Vera.ttf is from:

    http://ftp.gnome.org/pub/GNOME/sources/ttf-bitstream-vera/1.10/
    see that site for more information about the font.

PS. most things citing "TGA" file format will just work
with PNG and other file formats out of the box:
TGA used to be the sole 32bit image format supported
directly by Pygame when the codebase was created. The
codebase does no verification on the filetypes or
requested filenames, just foward it to Pygame -
which nowadays (2024) support a lot of other
image types.

Documentation
=============

To build the PGU documentation, run the build.py script found under docs:

    $ cd docs
    $ python build.py
    $ your-favorite-browser index.html

To understand pgu.gui -- read:
    http://www.w3.org/TR/REC-html40/
    (pgu.gui is based heavily on my HTML background)

To understand the pgu.gui default theme -- read:
    http://www.w3.org/TR/REC-CSS2/box.html
    (the theme uses the css 2 box model)

Example scripts can be found in the examples directory.

THANKS
======

* gal koren -- bugs, draft of html.HTML, suggestions, bug finding, ScrollArea widget, FileDialog, List, Console
* fdarling -- testing, suggestions, bug fixing, code cleanup, menus & slider UI fixes, new Table class, reorganization of pgu.gui into a package
* richard jones -- packaging, suggestions, code cleanup
* jhofmann -- tiled preview in tileedit and PIL support
* Dr. L. Humbert -- gui.Password widget
* illume -- added auto-load features to tile & leveledit
* python -- suggestions, bug finding, bug fixing (unicode)
* Addison Hardy -- added ScrollArea to html5.py
* dang`r`us -- testing, suggestions
* piman -- testing, suggestions
* coca-cola -- testing
* tenoften -- testing
* Joao S. O. Bueno - evolving the code base to Python3 (pygame 1.9.5)
