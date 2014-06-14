# -*- Python -*-
# Jiao Lin <linjiao@caltech.edu>

import os

from . import name

def run(*args, **kwds):
    from . import public_commands
    print()
    print('Basic commands:')
    for cmd in public_commands:
        print('  %s %s' % (name, cmd))
        continue
    return
    

def parse_cmdline():
    return [], {}

