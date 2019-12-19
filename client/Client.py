#!/usr/bin/env python
# -*- coding: utf-8 -*- 

from socket import *
import time
import sys

PAYLOAD_SIZE = 4096
MEGA = 10**6

if len(sys.argv) is not 3:
    print("python Client.py <ip> <port>")
    exit()

server_ip = sys.argv[1]
server_port = int(sys.argv[2])

client_socket = socket(AF_INET, SOCK_STREAM)

client_socket.connect((server_ip, server_port))


while True:
    # send data
    client_socket.send(bytearray(PAYLOAD_SIZE))

client_socket.close()
