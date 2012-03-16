#!/usr/bin/env python

import collections
import sys

try:
    path = sys.argv[1]
except:
    print "usage: convertconfig.py config.txt"
    print ""
    print "Converts the old PGU theme config.txt format into the style.ini format"
    print ""
    sys.exit(1)

styleByClass = collections.defaultdict(dict)

fd = file(path, "r")
for line in fd.readlines():
    line = line.strip()
    if (not line): continue

    args = line.split()
    try:
        name = args[0]
        attr = args[1]
        values = " ".join(args[2:])
    except:
        print "Invalid line: %s" % line
        sys.exit()
    styleByClass[name][attr] = values
fd.close()

for klass in sorted(styleByClass.keys()):
    print "[%s]" % klass
    for attr in sorted(styleByClass[klass].keys()):
        print "%s = %s" % (attr, styleByClass[klass][attr])
    print ""

