import numpy as np
from matplotlib import pyplot as plt
import time

x = 0

def funcion(x):
    y = np.sin(np.sqrt(x))
    return y

r = np.linspace(0,10,100)
plt.ion()
plt.plot(r,funcion(r))


b = float(input('Ingrese el limite superior: '))
a = float(input('Ingrese el limite inferior: '))
n_trapecios = int(input('Ingrese el numero de trapecios: '))

x = np.zeros([n_trapecios + 1])

h = (b - a) / n_trapecios
x[0] = a
x[n_trapecios] = b
suma = 0


t0 = time.time()

for i in np.arange(1, n_trapecios):
    x[i] = x[i-1] + h
    suma = suma + funcion(x[i])
    print('sumatoria ', i, ': ', suma)


integral = (h / 2) * (funcion(x[0]) + 2 * suma + funcion(x[n_trapecios]))
tf = time.time() - t0

print("Resultado: ", round(integral, 10))
print("Tiempo total: {}".format(tf))

