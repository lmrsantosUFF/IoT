from coapthon.client.helperclient import HelperClient
import sys
import time

# convert arguments into the following variables:
# host and port to connect to the CoAP server
# number of the LED which the client wishes to control
# temperature and pressure thresholds for the client
host = sys.argv[1]
port = int (sys.argv[2])
meu_LED = sys.argv[3]
lim_temperature = sys.argv[4]
lim_pressure = sys.argv[5]

# create a CoAP client
client = HelperClient(server=(host, port))
print ("Meu LED =", meu_LED, ", meus limiares = ", lim_temperature, lim_pressure)

# PUT the desired LED and both thresholds via CoAP
try:
    client.put("limiares", meu_LED + "=" + lim_temperature + ";" + lim_pressure)
    client.stop()
except:
    print ("problema na comunicacao do cliente")
    sys.exit()
