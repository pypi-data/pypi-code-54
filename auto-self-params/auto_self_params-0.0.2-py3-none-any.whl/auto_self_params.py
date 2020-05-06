#!/usr/bin/env python3
# coding:utf-8
"""
  Author: Steve Barnes  --<gadgetsteve.hotmail.com>
  Purpose: Enable the automatic creation of self properties from parameters.
  Created: 05/05/20
"""


def auto_self_params(args: dict):
    """
    Typically call as the first line of __init__ with a parameter of locals().

    This will add all of the parameters of __init__ as attributes of self.
    The args parameter must be a dictionary which must include `self` which
    must be a  class object.  The built in locals gives this with all of the
    local names, including parameters, defined.
    """
    assert isinstance(args, dict), "Must be called with dict as a parameter"
    theobj = args.pop("self", None)
    assert theobj is not None, "Class must specify 'self'"
    assert hasattr(theobj, "__class__") and hasattr(
        theobj, "__init__"
    ), "Must be called in a class __init__ method"
    for key, val in args.items():
        setattr(theobj, key, val)


if __name__ == '__main__':
    print(__file__, "is not directly executale.")
