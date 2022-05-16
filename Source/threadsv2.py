from concurrent.futures import Executor, ThreadPoolExecutor
import math
import numpy as np
from matplotlib import pyplot as plt
import threading
import time

x = 0

def funcion(x):
    y = np.sin(np.sqrt(x))
    return y

r = np.linspace(0,10,100)
#plt.ion()
plt.plot(r,funcion(r))


b = float(input('Ingrese el limite superior: '))
a = float(input('Ingrese el limite inferior: '))
n_trapecios = int(input('Ingrese el numero de trapecios: '))
#n_threads = int(input('Ingrese el numero de hilos: '))

x = np.zeros([n_trapecios + 1])

h = (b - a) / n_trapecios
x[0] = a
x[n_trapecios] = b
suma = 0

def calcTrapecio(i):
    #print('FOR TRAPECIO: ', i)
    global suma
    x[i] = x[i-1] + h
    suma = suma + funcion(x[i])
    #print('sumatoria ',i, ': ', suma)

executor = ThreadPoolExecutor(max_workers=int(n_trapecios/2))
t0 = time.time()
for i in np.arange(1, n_trapecios):
    #print('FOR: ', i)
    executor.submit(calcTrapecio, i)

integral = (h / 2) * (funcion(x[0]) + 2 * suma + funcion(x[n_trapecios]))
tf = time.time() - t0
print("Resultado: ", round(integral, 10))
print('Tiempo total en {} segundos\n'.format(tf))


