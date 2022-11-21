from socket import *

DEBUG = True
TAS_PORT = 3333
def send_to_TAS_(cntName, data):
    client = socket(AF_INET, SOCK_STREAM)
    client.connect(('127.0.0.1', TAS_PORT))
    if DEBUG:
        print("[*] {}".format((cntName + '/' + data).encode('utf-8')))
    client.send((cntName + '/' + data).encode('utf-8'))

def send_to_TAS(cntName, data):
    send_to_TAS_(cntName, data)
    send_to_TAS_(cntName, data)

send_to_TAS('seat1', '1')
