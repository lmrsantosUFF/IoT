# Exercicio3IoT
 <br> <br>

This small project simulates an IoT application that deals with sensors (temperature and pressure) and actuators (LEDs, on a SenseHat board embedded on Raspbian OS of Raspberry Pi). The sensors are distributed through different clients, which communicate with the server via CoAP , a protocol that suits well IoT and edge computing devices. <br> <br>
Part of the documentation is written in Portuguese.


Communication 

<br> <br>

<h3>Comando para iniciar o servidor </h3><br>
Sendo:<br>
argv[1] o endereço do host,  <br>
argv[2] o número da porta. <br>
 <br>
<b>python servidor.py   192.168.56.101   5683</b> <br>
 <br> <br> <br>


<h3>Comando para iniciar um cliente </h3><br>
Sendo:<br>
argv[1] o endereço do host,  <br>
argv[2] o número da porta, <br>
argv[3] o número do LED pretendido, <br>
argv[4] o novo limiar de temperatura, <br>
argv[5] o novo limiar de pressão. <br> <br>

<b>python clientes.py   192.168.56.101   5683   1   50   700</b>
