from .settings import ssid, passwd
import network
import uasyncio
from microdot_asyncio import Microdot


def scan():
    wlan = network.WLAN(network.STA_IF) # create station interface
    wlan.active(True)                   # activate the interface
    return wlan.scan()                  # scan for access points

def connect():
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    if not wlan.isconnected():
        print('connecting to network...')
        wlan.connect(ssid, passwd)
        while not wlan.isconnected():
            pass
    print('network config:', wlan.ifconfig())
    return wlan

app = Microdot()

def start_server():
    print("start server")
    connect()
    try:
        app.run(port=80)
    except Exception as e:
        app.shutdown()
        raise Exception(e)
    
@app.route('/')
def index(request):
    return "Hello World"