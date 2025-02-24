#!/usr/bin/python
"""<title>a tga creator</title>
<pre>usage: tganew fname.tga w h

options:
  -h, --help  show this help message and exit

example:
tganew tiles.tga 256 256
</pre>
"""

from optparse import OptionParser

usage = "usage: %prog fname.tga w h"
parser = OptionParser(usage)
(opts,args) = parser.parse_args()
if len(args) != 3:
	parser.error("incorrect number of arguments")

try: 
    fname,w,h = args[0],int(args[1]),int(args[2])
except ValueError: 
    parser.error("width and height must be integers")

if w < 1 or h < 1: 
    parser.error("width and height must be greater than 0")

import pygame
from pygame.locals import *

s = pygame.Surface((w,h),SWSURFACE|SRCALPHA,32)
s.fill((0,0,0,0))

pygame.image.save(s,fname)
# vim: set filetype=python sts=4 sw=4 noet si :
