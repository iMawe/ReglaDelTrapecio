import math
import numpy as np
from matplotlib import pyplot as plt

x = 0

def funcion(x):
    y = np.sin(np.sqrt(x))
    return y

r = np.linspace(0,10,100)
plt.ion()
plt.plot(r,funcion(r))

