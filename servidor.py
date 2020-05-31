import time
import sys

from threading import Thread
from sense_emu import SenseHat

from coapthon.server.coap import CoAP
from coapthon.resources.resource import Resource
from coapthon.client.helperclient import HelperClient

# class responsible for creating resources with default payload = "null"
class BasicResource(Resource):
    def __init__(self, name="BasicResource", coap_server=None):
        super(BasicResource, self).__init__(name, coap_server, visible=True,
                                            observable=True, allow_children=True)
        self.payload = "null"

    def render_GET(self, request):
        return self

    def render_PUT(self, request):
        self.payload = request.payload
        return self

    def render_POST(self, request):
        res = BasicResource()
        res.location_query = request.uri_query
        res.payload = request.payload
        return res

    def render_DELETE(self, request):
        return True
    

# Server class as a specialization of CoAP superclass
class CoAPServer(CoAP):
    def __init__(self, host, port):
        CoAP.__init__(self, (host, port))
        
        # create a resource named "limiares" to receive thresholds from clients
        self.add_resource("limiares", BasicResource("limiares"))


# method for observing the "limiares" resource for new POST/PUT values from clients
def observer(response):
    global pixels
    global sense
    global client
    global limiares_temperature
    global limiares_pressure
    global atualizar
    
    try:
        resp = response.payload
        
        if (resp != "null"):
            # sort out which LED the client wishes to control
            (LED, limiares) = resp.split("=")
            LED = int(LED)
            
            # split the thresholds for temperature and pressure
            limiares = limiares.split(";") 
            lim_temperature = float(limiares[0])
            lim_pressure = float(limiares[1])
            
            # store the received thresholds on server-side variables  
            limiares_temperature[LED] = lim_temperature            
            limiares_pressure[LED] = lim_pressure
            
            # update the board if necessary
            atualizar()
            
    except:
        print("problema no payload do observer.\n\n")
    
# method for updating the LEDs when actuation is required
def atualizar():
    global last_temperature
    global last_pressure
    global sense
    global pixels
    global limiares_temperature
    global limiares_pressure
    
    vermelho = (255,0,0)
    apagado = (0,0,0)
    
    try:
        # for each LED, 
        for i in range(64):
                
            # confront the corresponding client thresholds with current temperature and pressure     
            if (last_temperature > limiares_temperature[i] and last_pressure > limiares_pressure[i]):
                pixels[i] = vermelho
            else:
                pixels[i] = apagado
        
        # change the state of the sensehat board
        sense.set_pixels(pixels)
    except:
        print('Erro ao atualizar a sensehat.')
            
# function to be executed by a thread that controls the sensehat board
def gerencia_a_sensehat():
    global last_temperature
    global last_pressure
    
    # infinite loop
    while True:
        try:
            # sense the new data for temperature and pressure
            temperature = sense.temperature
            pressure = sense.pressure
            
            # update the board ONLY if the new values differ from the previous readings
            if (temperature != last_temperature or pressure != last_pressure):

                last_temperature = temperature
                last_pressure = pressure
                atualizar()
        except:
            print('Erro ao ler a sensehat.')
            
        time.sleep(1)
        

# thread responsible for observing CoAP for new thresholds from clients
def clients_thread_function():
    global pixels
    global sense
    global client
        
    client = HelperClient(server=(host, port))       
    try:
        client.observe("limiares", observer) # observe the "limiares" resource
    except:
        print('Erro ao chamar o observe.')
        
# main function
def main():
    global sense
    global pixels
    global host
    global port
    global limiares_temperature
    global limiares_pressure
    global last_temperature
    global last_pressure
    
    # initialize the sensehat and set outliers as pre-sensored data for temperature and pressure
    sense = SenseHat()
    last_temperature=999999
    last_pressure=999999
    
    # initialize arrays for the LEDs and thresholds
    pixels = [None]*64
    limiares_temperature = [None]*64
    limiares_pressure = [None]*64
    for i in range(64):
        pixels[i] = (0,0,0)
        limiares_temperature[i] = 105 # highest temperature possible from the sensor, so the LEDs initiate turned OFF
        limiares_pressure[i] = 1260 # highest pressure possible from the sensor, so the LEDs initiate turned OFF
 
    # convert arguments into variables: host and port of the server
    host = sys.argv[1]
    port = int (sys.argv[2])
    
    # create the server
    server = CoAPServer(host, port)
    
    # this thread will be responsible for observing CoAP for changes in clients' thresholds
    clients_thread = Thread(target = clients_thread_function)
    clients_thread.setDaemon(True)
    clients_thread.start()
    
    # this thread will control the sensehat board
    sensehat_thread = Thread(target = gerencia_a_sensehat)
    sensehat_thread.setDaemon(True)
    sensehat_thread.start()
    
    # server starts listening for communication
    try:
        server.listen(10)
    except KeyboardInterrupt:
        server.close()
        sys.exit()
        
    

if __name__ == '__main__':
    main()