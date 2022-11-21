import serial
import pynmea2
from socket import *

DEBUG = True
TAS_PORT = 3333
def send_to_TAS_(cntName, data):
    client = socket(AF_INET, SOCK_STREAM)
    client.connect(('127.0.0.1', TAS_PORT))
    if DEBUG:
        print("[*] {}".format((cntName + '/' + data).encode('utf-8')))
    client.send((cntName + '/' + data).encode('utf-8'))
    client.close()

def send_to_TAS(cntName, data):
    send_to_TAS_(cntName, data)
    send_to_TAS_(cntName, data)

def parseGPS(s):
    if s.find('GGA') > 0:
        msg = pynmea2.parse(s)
        lat = float(msg.lat)/100+0.2206
        lon = float(msg.lon)/100+0.0293
        print(msg.lat, msg.lon)
        send_to_TAS('gps_lat', str(lat))
        send_to_TAS('gps_lon', str(lon))

serialPort = serial.Serial("/dev/serial0", 9600, timeout=0.5)
while True:
    s = serialPort.readline()
    parseGPS(s.decode())


