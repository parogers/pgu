#! /usr/bin/env python

try:
    from distutils.core import setup
except:
    from setuptools import setup

import sys, os
from glob import glob

#############################################################################
### Main setup stuff
#############################################################################

def main():
    # Add themes from the data folder
    installdatafiles = []
    for name in ("default", "gray", "tools"):
        installdatafiles.append(
            (os.path.join("share", "pgu", "themes", name), glob(os.path.join("data", "themes", name, "*")))
        )

    #import pprint
    #pprint.pprint(installdatafiles)
    
    # perform the setup action
    from pgu import __version__
    setup_args = {
        'name': "pgu",
        'version': __version__,
        'description': "Phil's pyGame Utilities - a collection of handy "
            "modules and scripts for PyGame.",
        'long_description':
'''Phil's pyGame Utilities - a collection of handy modules and scripts for PyGame.

tileedit  -- edit tga based images
leveledit -- edit tga based levels in tile, isometric, and hexagonal formats

gui     -- gui with standard widget, dialog, connections, and themes
html    -- html rendering utilities
layout  -- layout utilities
text    -- text rendering utilities

tilevid -- sprite and tile engine
isovid  -- isometric sprite and tile engine
hexvid  -- hexagonal sprite and tile engine
engine  -- state engine
timer   -- a timer for games with set-rate FPS
high    -- high score tracking
ani     -- animation helpers
algo    -- helpful pathfinding algoritms
fonts   -- font wrappers, bitmapped fonts
''',
        'author': "Phil Hassey",
        'author_email': "philhassey@yahoo.com",
        'url': 'http://www.imitationpickles.org/pgu/',
        'packages': ['pgu','pgu.gui'],
        'classifiers': [
            'Development Status :: 4 - Beta',
            'Intended Audience :: Developers',
            'Operating System :: MacOS :: MacOS X',
            'Operating System :: Microsoft :: Windows',
            'Operating System :: POSIX',
            'Programming Language :: Python',
        ],
        'data_files': installdatafiles,
    'scripts': ['scripts/tileedit','scripts/leveledit','scripts/tganew','scripts/levelfancy'],
    }
    setup(**setup_args)

if __name__ == '__main__':
    main()

# vim: set filetype=python sts=4 sw=4 et si :
