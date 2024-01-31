## @package Polynomial
#  Module containing the class Polynomial and associated methods. The Polynomial class
#  is the workhorse in this library and the standard way of storing the information of
#  the integers or the radix-point numbers.

from __future__ import annotations
import numpy as np


## The Polynomial class is used to represent univariate polynomials. These can be considered
#  to be on a ring \$\mathbb{Z}_p\$ (that is integers modulo \$p\$). 
#
#  The Polynomial class is very convenient as e.g. by setting \$p\$ to be 2 we can use the 
#  polynomial to represent binary numbers. Note that this is by no means an optimized implementation.
#  While the algorithms themselves should run in near linear time, Python (even with help from Numpy)
#  is not all that fast and doesn't allow low level optimizations. Additionally, the implementation
#  is not the most memory efficient as the coefficients of the polynomial will be stored as 64-bit
#  integers in a Numpy array.
class Polynomial:

    ## The standard constructor
    #  @param coefs The coefficient array. Should consist of integers modulo base
    #  @param base The base used in computations. 
    def __init__(self, coefs: np.ndarray, base: int) -> None:
        self.__coefs = coefs
        self.__base = base

    def __repr__(self) -> str:
        pass

    def __hash__(self) -> int:
        pass
        
    def __call__(self, x: int = None) -> str:
        pass

    def __eq__(self, other: Polynomial) -> bool:
        pass

    def __mul__(self, other: Polynomial) -> Polynomial:
        pass

    def __add__(self, other: Polynomial) -> Polynomial:
        pass

    def __sub__(self, other: Polynomial) -> Polynomial:
        pass

    def __truediv__(self, other: Polynomial) -> tuple[Polynomial, Polynomial]:
        pass