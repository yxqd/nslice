# -*- Python -*-
# Jiao Lin <linjiao@caltech.edu>


import numpy as np, os

def mparr2nparr(a):
    return np.frombuffer(a.get_obj())

def load_mod(f):
    if not os.path.exists(f):
        raise IOError("%s does not exist" % f)
    code = open(f).read()
    context = dict()
    exec code in context
    return context

import copy
import optparse
def check_tuple(option, opt, value):
    if not value:
        return
    try:
        v = eval(value)
        return tuple(v)
    except ValueError:
        raise optparse.OptionValueError(
            "option %s: invalid value: %r" % (opt, value))

def check_axis(option, opt, value):
    if not value:
        return
    try:
        tokens = value.split(':')
        if len(tokens) not in [2, 3]:
            raise optparse.OptionValueError(
                "option %s: invalid value: %r. Format: min:max:step or min:max" % (opt, value))
        tokens = [eval(t)  if t else None for t in tokens]
        return tokens
    except ValueError:
        raise optparse.OptionValueError(
            "option %s: invalid value: %r" % (opt, value))

class MyOption(optparse.Option):
    TYPES = optparse.Option.TYPES + ('tuple', 'axis')
    TYPE_CHECKER = copy.copy(optparse.Option.TYPE_CHECKER)
    TYPE_CHECKER['tuple'] = check_tuple
    TYPE_CHECKER['axis'] = check_axis
