#Import socket module
from socket import *
import sys 
import os
import time, datetime
import threading
import csv


LABEL_X = 'Time'
LABEL_Y = '[Mb/s]'

is_server_running = True
number_of_connections = 0

PAYLOAD_SIZE = 4096 #bytes
DELAY = 1 #seconds
MEGA = 10**6

class PayloadSize:
    def __init__(self, size):
        self.size = size

class Timer (threading.Thread):
    def __init__(self, delay, payload):
        threading.Thread.__init__(self)
        self.delay = delay
        self.payload = payload
      
    def run(self):
        global is_server_running
        global number_of_connections
        
        while os.path.exists("results%s.csv" % number_of_connections):
            number_of_connections += 1

        with open('results%s.csv' % number_of_connections, 'w') as file:
            writer = csv.writer(file, delimiter=',', quotechar='"')
            writer.writerow([LABEL_X, LABEL_Y])
            while is_server_running:
                initial_size = self.payload.size
                time.sleep(self.delay)
                actual_size = self.payload.size

                amount_of_data = actual_size - initial_size
                mega_bits_amount_of_data = (amount_of_data*8)/(10**6)
                transfer_rate = mega_bits_amount_of_data/self.delay
                
                writer.writerow([datetime.datetime.now().isoformat(), transfer_rate])
                print('Numero de clientes conectados %s\nTaxa de transferência: ' % str(number_of_connections +1) , transfer_rate, 'Mbits/s')
                file.flush()

            file.close()
class ConnectionHandler(threading.Thread):
    def __init__(self, newConnectionSocket):
        threading.Thread.__init__(self)
        self.socket = newConnectionSocket

    def run(self):
        global is_server_running
        payload = PayloadSize(0)
        timer = Timer(DELAY, payload)
        timer.start()
        while is_server_running:
            payload_recv = self.socket.recv(PAYLOAD_SIZE)
            payload.size = payload.size + sys.getsizeof(payload_recv)

        self.socket.close()
        print("connection aborted!")

try:
    if len(sys.argv) is not 2:
        print("python Server.py <port>")
        exit()

    server_socket = socket(AF_INET, SOCK_STREAM) # IPv4 ; TCP
    server_socket.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1) #reuso
    server_port = int(sys.argv[1])

    server_socket.bind(('', server_port))

    server_socket.listen(5) #permite até 5 conexões
    print('Servidor pronto para receber clientes')

    while True:
        # Accepts new connections creating connection sockets 
        connectionSocket, addr = server_socket.accept()
        
        # create new thread to handler different connections
        connectionHandler = ConnectionHandler(connectionSocket)
        connectionHandler.start()

except KeyboardInterrupt:
    is_server_running = False
    server_socket.close()
    print("Server finalizado")


