import numpy as np
from matplotlib import pyplot as plt
import time
import asyncio
import concurrent.futures
import logging
import sys
import re
import socket
import sys

funcionPrincipal = ''
x = 0
suma = 0
n_trapecios = 0
h = 0

def funcion(x):
    return eval(funcionPrincipal)

def mensajeRecivido(data):
    cadena = str(data, 'UTF-8')
    expresion = re.split(r'\s+', cadena)
    global funcionPrincipal
    global l_superior
    global l_inferior
    global n_trapecios
    global h
    global x
    funcionPrincipal = expresion[0]
    l_superior = int(expresion[1])
    l_inferior = int(expresion[2])
    n_trapecios = int(expresion[3])

    x = np.zeros([n_trapecios + 1])

    h = (l_superior - l_inferior) / n_trapecios
    x[0] = l_inferior
    x[n_trapecios] = l_superior
    funcMain()
    

def funcMain():
    logging.basicConfig(
        level=logging.INFO,
        format='%(threadName)10s %(message)s',
        stream=sys.stderr,
    )

    # creando un limite de hilos.
    executor = concurrent.futures.ThreadPoolExecutor(
        max_workers = int(n_trapecios/2),
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

def showFunction():
    r = np.linspace(0,10,100)
    plt.ion()
    plt.plot(r,funcion(r))

#l_superior = float(input('Ingrese el limite superior: '))
#l_inferior = float(input('Ingrese el limite inferior: '))
#n_trapecios = int(input('Ingrese el numero de trapecios: '))





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




# Create a UDP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
# Bind the socket to the port
server_address = ('0.0.0.0', 10000)
print('starting up on {} port {}'.format(*server_address))
sock.bind(server_address)


while True:
    print('\nwaiting to receive message')
    data, address = sock.recvfrom(4096)

    print('received {} bytes from {}'.format(
        len(data), address))
    mensajeRecivido(data)
    print(data)

    if data:
        sent = sock.sendto(data, address)
        print('sent {} bytes back to {}'.format(
            sent, address))


