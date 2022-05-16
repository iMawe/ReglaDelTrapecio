import math
import numpy as np
from matplotlib import pyplot as plt
import threading
import time
from concurrent.futures import ThreadPoolExecutor

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
n_threads = int(input('Ingrese numero de hilos: '))

x = np.zeros([n_trapecios + 1])

h = (b - a) / n_trapecios
x[0] = a
x[n_trapecios] = b
suma = 0
lista = list()


def calcTrapecio(inicio, fin):
    global suma
    if (n_trapecios % n_threads == 0):
        for i in np.arange(inicio, fin):
            x[i] = x[i-1] + h
            suma = suma + funcion(x[i])
    else:
        for i in np.arange(inicio, fin+1):
            x[i] = x[i-1] + h
            suma = suma + funcion(x[i])
    
p = n_trapecios//n_threads #5

inicios = list()
fines = list()
inicio = 1
fin = p

for i in range(n_threads): #2
    inicios.append(inicio)
    fines.append(fin)
    inicio += p
    fin += p

t0 = time.time()
threads = list()
for i in range(len(inicios)):
    t = threading.Thread(target = calcTrapecio, args=(inicios[i], fines[i],))
    threads.append(t)
    t.start()

for t in threads:
    t.join()

print(inicios)
print(fines)



integral = (h / 2) * (funcion(x[0]) + 2 * suma + funcion(x[n_trapecios]))

print("Resultado: ", round(integral, 10))

tf = time.time() - t0
print('Tiempo total en {} threads: {} segundos\n'.format(n_threads, tf))

