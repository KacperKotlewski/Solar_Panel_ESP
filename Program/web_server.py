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

async def start_server():
    wlan = connect()
    await app.start_server(debug=True, port=80)
    
@app.route('/')
async def index(request):
    return "Hello World"


#@app.route('/shutdown')
#async def shutdown(request):
    #request.app.shutdown()
    #from . import finish_flag
    #finish_flag = True
    #return 'The server is shutting down...'

