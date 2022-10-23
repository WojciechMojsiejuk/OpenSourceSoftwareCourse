from sympy import *
from IPython.display import display
import numpy as np
from scipy.optimize import minimize
import matplotlib
import matplotlib.pyplot as plt
matplotlib.use('TKAgg')

str_fun = "(1 - x_0)**2 + 100*(x_1 - x_0**2)**2"
sym_fun = sympify(str_fun)
display(sym_fun)
x_0, x_1 = symbols('x_0 x_1')
x = Matrix([[x_0, x_1]])


# First derivatives

fdx_0 = diff(sym_fun, x[0])
fdx_1 = diff(sym_fun, x[1])
fd = Matrix([fdx_0, fdx_1])
display(fd)

# Hessian (Second derivatives)

fdd = Matrix(
    [
        [diff(fdx_0, x_0), diff(fdx_0, x_1)],
        [diff(fdx_1, x_0), diff(fdx_1, x_1)]
    ]
)

display(fdd)