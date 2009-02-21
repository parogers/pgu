#! /usr/bin/env python

from distutils.core import setup
print 'When you get python 2.5, enable the next line...'
#from setuptools import setup

import sys, os
from glob import glob

#############################################################################
### Main setup stuff
#############################################################################

def main():
    # add data files
    installdatafiles = []
    def visit(l, dirname, names):
        r = []
        new_names = []
        for name in names[:]:
            path = os.path.join(dirname, name)
            if "CVS" in path:
                continue
            if name == 'CVS': 
                continue
            elif not os.path.isfile(path): 
                continue
            r.append(path)
        if r:
            l.append((os.path.join('share', 'pgu', dirname[5:]), r))

    os.path.walk('data', visit, installdatafiles)

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
