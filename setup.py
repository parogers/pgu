#! /usr/bin/env python

from setuptools import setup
from textwrap import dedent

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
        'name': "pygame-pgu",
        'version': __version__,
        'install_requires' : ['pygame > 1.9.0'],
        'description': "Phil's pyGame Utilities - a collection of handy "
            "modules and scripts for PyGame.",
        'long_description': dedent('''\
            Phil's pyGame Utilities - a collection of handy modules and scripts for PyGame.

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
        '''),
        'author': "Phil Hassey",
        'author_email': "philhassey@yahoo.com",
        'url': 'https://github.com/parogers/pgu',
            'project_urls': {
            # "Documentation": "https://pygame-pgu.readthedocs.io/en/stable/",
            "Source Code":'https://github.com/parogers/pgu',
            },
        'packages': ['pgu','pgu.gui'],
        'classifiers': [
            'Development Status :: 5 - Production/Stable',
            'Intended Audience :: Developers',
            'Operating System :: MacOS :: MacOS X',
            'Operating System :: Microsoft :: Windows',
            'Operating System :: POSIX',
            'Programming Language :: Python',
            'Programming Language :: Python :: 3 :: Only',
        ],
        'data_files': installdatafiles,
        'scripts': ['scripts/tileedit','scripts/leveledit','scripts/tganew','scripts/levelfancy'],
    }
    setup(**setup_args)

if __name__ == '__main__':
    main()

# vim: set filetype=python sts=4 sw=4 et si :
