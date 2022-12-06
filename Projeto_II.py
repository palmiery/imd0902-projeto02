import time, random
from Adafruit_IO import Client, Feed
from gpiozero import Button
import Adafruit_DHT

sensor = Adafruit_DHT.DHT11
pin = 22

ruido = Button(5)

ADAFRUIT_IO_KEY = 'aio_ZoTs57hulgxO3xIoKPeSqg2Nz0WN'

ADAFRUIT_IO_USERNAME = 'palmiery'

aio = Client(ADAFRUIT_IO_USERNAME, ADAFRUIT_IO_KEY)

import sys

if sys.platform.startswith('linux'):
    print('Linux!')
elif sys.platform.startswith('win'):
    print('Windows!')
elif sys.platform.startswith('darwin'):
    print('Mac OS')
else:
    print('Sistema Desconhecido!')

from ipaddress import IPv4Address
from ping3 import ping

inicial = IPv4Address("192.168.1.253")
final = IPv4Address("192.168.1.255")

#ips = [str(IPv4Address(ip)) for ip in range(int(inicial), int(final))]
ips = ("192.168.1.50", "192.168.1.69","192.168.1.71","192.168.1.73","192.168.1.69", "192.168.1.254")


while True:
    for ip in ips:
        t = ping(ip, timeout=1)
        time.sleep(0.6)
        status = 'OFFLINE' if t is None else 'ONLINE'
        aio.send_data('status', str(status))
        time.sleep(3)
        print(f'IP: {ip} [{status}]')
        aio.send_data('ip', str(ip))
				
	
        time.sleep(0.5)

    umidade, temperatura = Adafruit_DHT.read_retry(sensor, pin)
    print("{} {} {}".format(temperatura,umidade,str(ruido.is_pressed)))
    aio.send_data('temperatura', str(temperatura))
    aio.send_data('umidade', str(umidade))
    aio.send_data('ruido', str(ruido.value))
    
    time.sleep(10)
