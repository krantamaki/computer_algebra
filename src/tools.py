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
        assert (np.abs(array) < base).all(), "Coefficients must less than the base!"

        return func(*args, **kwargs)

    return check_array_wrapper


## Function for computing the inverse of a unit in some ring Z_b using 
#  the adapted Euclidean algorithm
#  @exception ValueError Raises ValueError if unit is not invertible (is not a unit)
#  @param unit The unit of which inverse is computed
#  @param b The modulo respect to which the ring is defined
def unit_inv(unit: int, b: int) -> int:
    t, t_upd = 0, 1
    r, r_upd = b, unit

    while r_upd != 0:
        quo = r // r_upd

        t, t_upd = t_upd, t - quo * t_upd
        r, r_upd = r_upd, r - quo * r_upd

    if r > 1:
        raise ValueError("Passed unit is not invertible!")
    if t < 0:
        t += b

    return t
