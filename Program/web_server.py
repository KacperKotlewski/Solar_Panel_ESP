from .settings import ssid, passwd
import network
import uasyncio
from microdot_asyncio import Microdot, Response
from .settings import DEBUG


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
    await app.start_server(debug=DEBUG, port=80)
    
@app.after_request
def func(request, response):
    response.headers["Access-Control-Allow-Origin"] = "*"
    
@app.route('/')
async def index(request):
    return Response.send_file('index.html')

@app.route("/get_debug", methods=["GET"])
async def get(request):
    print("headers",request.headers)
    print("args",request.args)
    print("body",request.body)
    print("json",request.json)
    return Response(["test"])