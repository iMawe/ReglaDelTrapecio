import socket
import sys

# Create a UDP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
server_address = ('172.18.0.2', 10000)
print("funcion limiteSuperior limiteInferior numeroTrapecios")
message = input()#b'' 90

try:
    # Send data
    #casteo
    message=bytes(message,'utf-8')
    print('sending {!r}'.format(message))
    sent = sock.sendto(message, server_address)

    # Receive response
    print('waiting to receive')
    data, server = sock.recvfrom(4096)
    print('received {!r}'.format(data))

finally:
    print('closing socket')
    sock.close()