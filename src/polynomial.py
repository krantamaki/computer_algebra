## @package Polynomial
#  Module containing the class Polynomial and associated methods. The Polynomial class
#  is the workhorse in this library and the standard way of storing the information of
#  the integers or the radix-point numbers.

from __future__ import annotations
import numpy as np
from tools import check_objects, check_array, unit_inv


## The Polynomial class is used to represent univariate polynomials. These can be considered
#  to be on a ring \$\mathbb{Z}_p\$ (that is integers modulo \$p\$). 
#
#  The Polynomial class is very convenient as e.g. by setting \$p\$ to be 2 we can use the 
#  polynomial to represent binary numbers. Note that this is by no means an optimized implementation.
#  While the algorithms themselves should run in near linear time, Python (even with help from Numpy)
#  is not all that fast and doesn't allow low level optimizations. Additionally, the implementation
#  is not the most memory efficient as the coefficients of the polynomial will be stored as 64-bit
#  (or 32-bit if ran on 32-bit architecture) integers in a Numpy array.
class Polynomial:

    ## The standard constructor
    #  @param coefs The coefficient array. Should consist of integers modulo base. Note that the array
    #   should include zero coefficients as well. The indexes of the coefficients in the array should
    #   coincide with the powers of the polynomial variable.
    #  @param base The base used in computations. Optional and defaults to 10.
    #  @param reverse Boolean flag for reversing the array. Optional and defaults to False. If the array 
    #   contains the coefficients in decreasing order of power the array can be reversed with this flag.
    @check_array
    def __init__(self, coefs: np.ndarray[np.int64], base: int = 10, 
                                                    reverse: bool = False, 
                                                    carries: np.ndarray[np.int64] = None) -> None:
        self.__coefs = np.array(coefs)
        self.__base = base

        if reverse:
            self.__coefs = np.flip(self.__coefs)

        # Remove trailing zeros to find valid degree and leading coefficient
        self.__coefs = np.trim_zeros(self.__coefs, 'b')

        self.__deg = len(self.__coefs) - 1
        self.__lc = self.__coefs[-1] if self.__deg > 0 else 0

        # Additionally, we will store the carries in a separate array that is not yet defined
        self.__carries = carries


    ## The object representation for debugging purposes. Call with repr() built-in function
    def __repr__(self) -> str:
        return f"coefs: {self.__coefs}\ncarries: {self.__carries}\nbase: {self.__base}"
    


    ## The object representation in a more readable form. Call with str() built-in function
    def __str__(self) -> str:
        return repr(self)
    

    def __hash__(self) -> int:
        return hash(repr(self))
    

    def __copy__(self) -> Polynomial:
        if self.__carries is not None:
            return Polynomial(self.__coefs.copy(), base=self.__base, carries=self.__carries.copy())
        else:
            return Polynomial(self.__coefs.copy(), base=self.__base)
    

    def copy(self) -> Polynomial:
        return self.__copy__()

    ## Evaluate the polynomial at some given point 
    #  @param x The point of evaluation. Optional and if not passed the polynomial
    #  will be evaluated at the base
    def __call__(self, x: int = None) -> str:
        pass

    ## Get an individual coefficient from the coefficient array
    #  @param key The key by which coefficient is accessed. Should be the index of
    #   the coefficient
    def __getitem__(self, key: int) -> int:
        if key <= self.__deg:
            return self.__coefs[key]
        else:
            return 0
    

    ## Set a coefficient at specified index
    #  @exception ValueError Raises a ValueError if the value set is not modulo base
    #  @param key The key by which coefficient is accessed. Should be the index of
    #   the coefficient
    #  @param value The value set at given index
    def __setitem__(self, key: int, value: int) -> None:
        if np.abs(value) >= self.__base:
            raise ValueError("The set value must be modulo base!")
        
        if key <= self.__deg:
            self.__coefs[key] = value
        else:
            self.__coefs += [0] * (key - self.__deg)
            self.__coefs[key] = value 
            self.__deg = key - 1
            self.__lc = value


    @check_objects
    def __eq__(self, other: Polynomial) -> bool:
        return self.__coefs == other.coefs() and self.__base == other.base()


    @check_objects
    def __add__(self, other: Polynomial) -> Polynomial:
        new_len = max(self.__deg, other.deg()) + 1
        new_coefs = [0] * new_len
        carries = [0] * (new_len + 1)

        for i in range(new_len):
            new_coefs[i] = (self[i] + other[i]) % self.__base
            carries[i + 1] = (self[i] + other[i]) // self.__base

        return Polynomial(new_coefs, base=self.__base, carries=carries)
    

    @check_objects
    def __sub__(self, other: Polynomial) -> Polynomial:
        new_len = max(self.__deg, other.deg()) + 1
        new_coefs = [0] * new_len
        carries = [0] * (new_len + 2)

        for i in range(new_len):
            new_coefs[i] = (self[i] - other[i]) % self.__base
            carries[i + 1] = (self[i] - other[i]) // self.__base

        return Polynomial(new_coefs, base=self.__base, carries=carries)


    @check_objects
    def __mul__(self, other: Polynomial) -> Polynomial:
        # While the near linear time algorithm for multiplication is not implemented
        # use the quadratic time one
        return self._slow_mul(other)


    ## Slow O((n + m)^2) implementation of polynomial multiplication. Used for debugging
    @check_objects
    def _slow_mul(self, other: Polynomial) -> Polynomial:
        new_len = self.__deg + other.deg() + 1
        new_coefs = [0] * new_len
        carries = [0] * (new_len + 1)

        for i in range(new_len):
            coef = 0

            for j in range(i):
                coef += self[j] * other[i - j]

            new_coefs[i] = coef % self.__base
            carries[i + 1] = coef // self.__base

        return Polynomial(new_coefs, base=self.__base, carries=carries)


    @check_objects
    def __truediv__(self, other: Polynomial) -> tuple[Polynomial, Polynomial]:
        # While the near linear time algorithm for division is not implemented
        # use the quadratic time one
        return self._slow_div(other)


    ## Slow O((n + m)^2) implementation of polynomial division. Used for debugging
    @check_objects
    def _slow_div(self, other: Polynomial) -> tuple[Polynomial, Polynomial]:
        import time 
        q, q_upd = Polynomial([0], base=self.__base), None
        r, r_upd = self.copy(), None

        inv_lc_b = unit_inv(other.lc(), self.__base)

        deg_r, deg_b = r.deg(), other.deg()

        i = 0
        while deg_r >= deg_b:

            if i != 0:
                q, r = q_upd, r_upd

            tmp = Polynomial([0] * (deg_r - deg_b) + [r.lc() * inv_lc_b], base=self.__base)

            q_upd = q + tmp
            r_upd = r - tmp * other

            deg_r = r_upd.deg()
            i += 1

        return q, r


    ## Returns a copy of the coefficient array
    def coefs(self) -> np.ndarray[np.int64]:
        return self.__coefs.copy()
    

    ## Returns the base
    def base(self) -> int:
        return self.__base
    

    ## Set the carries that resulted from e.g. addition an are required by the Integer and Radix classes
    #  @param carries The array of carries. Should consist of integers modulo base. Note that the array
    #   should include zero carries as well. The indexes of the carries in the array should
    #   coincide with the powers of the polynomial variable
    @check_array
    def set_carries(self, carries: np.ndarray[np.int64]) -> None:
        self.__carries = carries


    ## Access the carries if set
    #  @exception RuntimeError Raises a RuntimeError if carries have not been set
    def get_carries(self) -> np.ndarray[np.int64]:
        if self.__carries is not None:
            return self.__carries.copy()
        else:
            raise RuntimeError("The carries have not been set yet!")


    ## Computes the discrete Fourier transform
    def dft(self) -> Polynomial:
        pass


    ## Returns the leading coefficient
    def lc(self) -> int:
        return self.__lc


    ## Returns the degree of the polynomial
    def deg(self) -> int:
        return self.__deg
    