import numpy as np
from matplotlib import pyplot as plt
import time
import asyncio
import concurrent.futures
import logging
import sys

x = 0

def funcion(x):
    y = np.sin(np.sqrt(x))
    return y

def show():
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

def calcTrapecio(i):
    global suma
    x[i] = x[i-1] + h
    suma = suma + funcion(x[i])
    print('sumatoria ', i, ': ', suma)


def blocks(n):
    log = logging.getLogger('blocks({})'.format(n))
    log.info('running')
    calcTrapecio(n)
    log.info('done')
    return n ** 2


async def run_blocking_tasks(executor):
    log = logging.getLogger('run_blocking_tasks')
    log.info('starting')

    log.info('creating executor tasks')
    loop = asyncio.get_event_loop()
    blocking_tasks = [
        loop.run_in_executor(executor, blocks, i)
        for i in np.arange(1, n_trapecios)
    ]
    log.info('waiting for executor tasks')
    completed, pending = await asyncio.wait(blocking_tasks)
    log.info('exiting')


if __name__ == '__main__':
    logging.basicConfig(
        level=logging.INFO,
        format='%(threadName)10s %(message)s',
        stream=sys.stderr,
    )

    # creando un limite de hilos.
    executor = concurrent.futures.ThreadPoolExecutor(
        max_workers=int(n_trapecios/2),
    )

    event_loop = asyncio.get_event_loop()
    try:
        t0 = time.time()
        event_loop.run_until_complete(
            run_blocking_tasks(executor)
        )
        tf = time.time() - t0
    finally:
        event_loop.close()
    
    integral = (h / 2) * (funcion(x[0]) + 2 * suma + funcion(x[n_trapecios]))

    print("Resultado: ", round(integral, 10))
    print("Tiempo total: {}".format(tf))

