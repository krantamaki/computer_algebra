## @package Tools
# Useful helper functions and decorators to be used by the other classes

from collections.abc import Callable
from typing import Any
import numpy as np


## Decorator that checks that the two objects are valid for computations
#  Assumes that self is the first positional argument and the other
#  object is the second positional argument
def check_objects(func: Callable[[Any], Any]) -> Callable[[Any], Any]:
    def check_objects_wrapper(*args, **kwargs):
        this = args[0]
        that = args[1]

        assert isinstance(that, type(this)), f"The types of the objects must match! ({type(this)} != {type(that)})"
        assert that.base() == this.base(), f"The bases must match! ({this.base()} != {that.base()})"

        return func(*args, *kwargs)

    return check_objects_wrapper


## Decorator that checks the correctness of a polynomial array
#  Assumes that the array is the second positional argument
#  (first is generally self). The base should either be a keyword
#  argument or it is retrieved from the self argument
def check_array(func: Callable[[Any], Any]) -> Callable[[Any], Any]:
    def check_array_wrapper(*args, **kwargs):
        array = np.array(args[1])
        
        if "base" not in kwargs:
            base = args[0].base()
        else:
            base = kwargs["base"]

        assert array.dtype == np.int32 or array.dtype == np.int64, f"Coefficients must be integers! (type: {array.dtype})"
        assert (np.abs(array) < base).all(), "Coefficients must be modulo base!"

        return func(*args, **kwargs)

    return check_array_wrapper




