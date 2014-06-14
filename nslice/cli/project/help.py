# -*- Python -*-
# Jiao Lin <linjiao@caltech.edu>


from .. import name as cliname
from . import name as cmdname


import os

def run(*args, **kwds):
    from . import actions
    print()
    print('actions:')
    for action in actions:
        print('  %s %s %s' % (cliname, cmdname, action))
        continue
    return
    

def parse_cmdline():
    return [], {}


