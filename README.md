# Library for algebraic computations on polynomials

This library is meant to be an easy to use tool for basic computations on arbitrarily large univariate polynomials. The algorithms should run in near linear time. However, the implementation is not meant to be highly optimized and is more just for demonstration and testing purposes.

The algorithms roughly follow the textbook _Modern Computer Algebra_ by Joachim Von Zur Gathen and Jurgen Gerhard and lecture material for the graduate level course _Advanced Course in Algorithms_ in Aalto University lectured by Prof. Petteri Kaski.

## Structure

The main components of the library are the classes _Polynomial_, _Integer_ and _Radix_. The _Polynomial_ class contains most of the logic and algorithms used. The _Integer_ class in turn is a wrapper around the _Polynomial_ class that allows for computations on arbitrary large integers in a wanted base. The _Radix_ class is also wrapper around the _Polynomial_ class, but is used to denote arbitrary rational numbers (read floating point) in the scientific notation. 