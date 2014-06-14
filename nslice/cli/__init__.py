# -*- Python -*-
# Jiao Lin <linjiao@caltech.edu>


name = 'nslice'


def run(action, *args, **opts):
    mod = importActionHandler(action)
    return mod.run(*args, **opts)


def importActionHandler(action):
    code = 'from . import %s' % action
    exec(code)
    mod = locals()[action]
    return mod


def main():
    import sys
    if len(sys.argv) <= 1:
        action = 'help'
    else:
        action = sys.argv[1]

    if action in ['-h', '--help']:
        action = 'help'

    if action not in commands:
        print ()
        print ("Invalid command: %s" % action)
        action = 'help'
    
    mod = importActionHandler(action)
    args, kwds = mod.parse_cmdline()
    
    mod.run(*args, **kwds)
    return


public_commands = [
    'project',
    'help',
    ]

hidden_commands = [
    ]


commands = public_commands + hidden_commands


