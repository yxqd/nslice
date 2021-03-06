# -*- Python -*-
# Jiao Lin <linjiao@caltech.edu>


name = 'volume'


def run(mod, *args, **opts):
    return mod.run(*args, **opts)


def importActionHandler(action):
    code = 'from . import %s' % action
    exec(code)
    mod = locals()[action]
    if mod is None:
        raise ImportError(action)
    return mod


def parse_cmdline():
    import sys
    if len(sys.argv) <= 2:
        action = 'default'
    else:
        action = sys.argv[2]
    
    if action in ['-h', '--help']:
        action = 'help'
    elif action.startswith('-'): # default action can be escaped
        action = 'default'

    if action not in actions:
        print ()
        print ("Invalid action: %s" % action)
        action = 'help'
    
    mod = importActionHandler(action)
    args, kwds = mod.parse_cmdline()
    
    return [mod] + args, kwds


actions = [
    'default',
    'help',
    ]


