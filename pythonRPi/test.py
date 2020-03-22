#IoT services
'''
IoT Services
https://adafruit.io/
https://pushdata.io/
https://corlysis.com/


DigitalOcean Example Droplets:
Grafana
ThingsBoard Community Edition
'''


import random
import time
import Adafruit_IO as adaIO
import serial
import serial.tools.list_ports
import binascii
import credentials

#Data format: **(W:n,B:m)

START_TOKEN = '**'
WIFI_TOKEN = 'W'
BLE_TOKEN  = 'B'
LIST_OF_COUNTERS = [WIFI_TOKEN, BLE_TOKEN]
TYPE_SEPARATOR_TOKEN = ','
COUNT_SEPARATOR_TOKEN = ':'

AVG_VALUES = 5 #Values to be averaged (mean) 
SECONDS_PER_MINUTE = 60
SAMPLING_MINUTES = 5 #Peroid to wait until next data sent is performed 

def parseCounters(serialText):
    #Expected format '**m,n', being 'm' and 'n' integers for (WiFi,BLE)
    #Returns a list of integer in the same order it was received, ie. [WiFi,BLE]
    text = str(serialText)
    if text[0:len(START_TOKEN)] != START_TOKEN:
        #print('No usable string: ' + text)
        return None
    t = text.split(START_TOKEN)[-1].split(TYPE_SEPARATOR_TOKEN)
    #print('x: ' + str(t) )
    
    counters = []
    for i in t:
        counters.append(int(i))

    print('Counters: ' + str(counters))
    
    return counters

def findUsbPort():
    USB_TOKEN = 'USB'
    portList = serial.tools.list_ports.comports()
    ports = []
    for i in portList:
        ports.append(i.device)

    x = 0 #index of available USB port
    for i in ports:
        if USB_TOKEN in i:
            return i
    return None

def readFromUart():
    a = str(uart.readline().decode("utf-8"))
    #print('Read from uart: ' + a)
    if len(a):
        return a
    else:
        return ''


usbport = findUsbPort()
try:
    uart = serial.Serial(usbport, 115200, timeout = 30)
except IOError as serialE:
    print('No se pudo abrir puerto serial: ' + str(serialE))
finally:
    print('Inicialización UART completada en ' + usbport)
    

aio = adaIO.Client(credentials.USER_NAME, credentials.PRIVATE_KEY)

values = []
avg = 0
lastTime = time.time()

while(1):
    x = readFromUart()
    if(len(x)):
        counters = parseCounters(x)
        if counters:
            wifiCounters = int(counters[0])
            bleCounters  = int(counters[1])
            print('Parsed data: ' + str(counters))
            
            currentTime = time.time()
            if (currentTime - lastTime) > SAMPLING_MINUTES*SECONDS_PER_MINUTE:
                
                avg = sum(values)/len(values)
                values = []
                
                aio.send('node-1', avg)
                print('WiFi counters sent: ' + str(avg))

                lastTime = time.time()
                
            else:
                values.append(wifiCounters)

'''
n = 10
while(n):
    x = readFromUart()
    if(len(x)):
        print('Parsed data: ' + str(parseCounters(x)))
        n -= 1
        print('Counters left: ' + str(n))
    else:
        print('Nothing to show')
uart.close()
'''

'''
for i in range(10):
    data = int(random.random()*4)
    aio.send("node-1", data)
    print("Data has been sent", str(data))
    time.sleep(30)
'''