from machine import Pin, PWM, I2C
import time
import math
import network
import socket
import ujson
import dht
import utelegram
from mpu6500 import MPU6500

#conectar wifi
WLAN = network.WLAN(network.STA_IF)
WLAN.active(True)
WLAN.connect('Xiaomi 14', 'holamundo')

while not WLAN.isconnected():
    print("Conexión en proceso...")
    time.sleep(1)

estado = WLAN.ifconfig()

print(estado)
print("Conectado")

#telegram
token = '8980293239:AAFVHgQKHNaRVbL01zxwT-0sJpKwQovY94g'
miID = '8795987850'

MiBot = utelegram.ubot(token)

print("Telegram conectado")

MiBot.send(miID, "Monitor IoT Biomédico conectado")

def enviar_telegram(mensaje):

    try:
        MiBot.send(miID, mensaje)
        print("Mensaje enviado")

    except Exception as e:
        print("Error enviando Telegram")
        print(e)

#sensor dth11
sensor_dht = dht.DHT11(Pin(15))

#mpu6500
i2c = I2C(0, scl=Pin(22), sda=Pin(21))
print("Dispositivos I2C encontrados:", i2c.scan())
mpu = MPU6500(i2c)

#buzzer
buzzer = PWM(Pin(18))
buzzer.duty_u16(0)

def sonar(freq, tiempo):
    buzzer.freq(freq)
    buzzer.duty_u16(30000)
    time.sleep(tiempo)
    buzzer.duty_u16(0)

#boton
boton = Pin(4, Pin.IN, Pin.PULL_UP)

#variables
temperatura = 0
humedad = 0
estado_movimiento = "Reposo"
alarma = "NORMAL"
TEMP_MAX = 30
TEMP_MIN = 18
HUM_MAX = 80
HUM_MIN = 30

#control alertas telegram
alerta_temp_alta = False
alerta_temp_baja = False
alerta_hum_alta = False
alerta_hum_baja = False
alerta_movimiento = False
alerta_panico = False

#pagina web
def pagina_web():

    html = f"""
    <!DOCTYPE html>

    <html>

    <head>

        <meta http-equiv="refresh" content="2">

        <title>Monitor IoT Biomedico</title>

        <style>

            body {{
                font-family: Arial;
                background-color: #0f172a;
                color: white;
                text-align: center;
                padding-top: 40px;
            }}

            .card {{
                background-color: #1e293b;
                margin: auto;
                width: 300px;
                padding: 20px;
                border-radius: 15px;
                box-shadow: 0px 0px 10px black;
            }}

            h1 {{
                color: cyan;
            }}

            p {{
                font-size: 20px;
            }}

            .alerta {{
                color: yellow;
                font-weight: bold;
            }}

        </style>

    </head>

    <body>

        <div class="card">

            <h1>Monitor IoT Biomedico</h1>

            <p>Temperatura: {temperatura:.2f} °C</p>

            <p>Humedad: {humedad:.2f} %</p>

            <p>Movimiento: {estado_movimiento}</p>

            <p class="alerta">Alarma: {alarma}</p>

        </div>

    </body>

    </html>
    """
    return html

#web
addr = socket.getaddrinfo('0.0.0.0', 80)[0][-1]
server = socket.socket()
server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server.bind(addr)
server.listen(1)
server.settimeout(0.1)
print("Servidor web activo")

#loop principal
while True:
    #lectura dh11
    try:
        sensor_dht.measure()
        temperatura = sensor_dht.temperature()
        humedad = sensor_dht.humidity()

    except:
        print("Error leyendo DHT11")
    
    #lectura MPU6500
    try:
        ax, ay, az = mpu.read_accel_data()
        magnitud = math.sqrt(ax**2 + ay**2 + az**2)
        print("Magnitud:", magnitud)

        if magnitud < 1.2:
            estado_movimiento = "Reposo"

        elif magnitud < 2:
            estado_movimiento = "Movimiento"

        else:
            estado_movimiento = "Movimiento Brusco"

    except:
        print("Error leyendo MPU6500")

    #alertas
    alarma = "NORMAL"

    #temperatura alta
    if temperatura > TEMP_MAX:
        alarma = "TEMPERATURA ALTA"
        sonar(1000, 0.2)

        if not alerta_temp_alta:
            enviar_telegram("ALERTA: TEMPERATURA ALTA")
            alerta_temp_alta = True

    else:
        alerta_temp_alta = False

    #temperatura baja
    if temperatura < TEMP_MIN:
        alarma = "TEMPERATURA BAJA"
        sonar(500, 0.2)

        if not alerta_temp_baja:
            enviar_telegram("ALERTA: TEMPERATURA BAJA")
            alerta_temp_baja = True

    else:
        alerta_temp_baja = False

    #humedad alta
    if humedad > HUM_MAX:
        alarma = "HUMEDAD ALTA"
        sonar(1500, 0.2)

        if not alerta_hum_alta:
            enviar_telegram("ALERTA: HUMEDAD ALTA")
            alerta_hum_alta = True

    else:
        alerta_hum_alta = False

    #humedad baja
    if humedad < HUM_MIN:
        alarma = "HUMEDAD BAJA"
        sonar(700, 0.2)

        if not alerta_hum_baja:
            enviar_telegram("ALERTA: HUMEDAD BAJA")
            alerta_hum_baja = True

    else:
        alerta_hum_baja = False
    
    #movimiento feo
    if estado_movimiento == "Movimiento Brusco":
        alarma = "MOVIMIENTO BRUSCO"
        sonar(2500, 0.3)

        if not alerta_movimiento:
            enviar_telegram("ALERTA: MOVIMIENTO BRUSCO DETECTADO")
            alerta_movimiento = True

    else:
        alerta_movimiento = False

    #panicooo
    if boton.value() == 0:
        alarma = "BOTON DE PANICO"
        sonar(3000, 0.5)

        if not alerta_panico:
            enviar_telegram("ALERTA: BOTON DE PANICO ACTIVADO")
            alerta_panico = True

    else:
        alerta_panico = False
        
    #servidor web
    try:

        client, addr = server.accept()

        print("Cliente conectado")

        request = client.recv(1024)

        response = pagina_web()

        client.send('HTTP/1.1 200 OK\r\n')
        client.send('Content-Type: text/html\r\n')
        client.send('Connection: close\r\n\r\n')

        client.sendall(response)

        client.close()

    except:

        pass
    
    #serial monitor
    print("----------------------------")
    print("Temperatura:", temperatura)
    print("Humedad:", humedad)
    print("Movimiento:", estado_movimiento)
    print("Alarma:", alarma)

    time.sleep(1)