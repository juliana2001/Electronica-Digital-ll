from machine import Pin, ADC, PWM #importa clases para manera los pines, entradas analog y PMW
import time #Importa tiempo
 
#Potenciometros
pot1 = ADC(Pin(34)) #crea ADC en pin 34
pot1.width(ADC.WIDTH_12BIT) #configura resolucion 12bits (0 a 4095) (entre mas bits, mas preciso-mas suaves)

pot2 = ADC(Pin(35))
pot2.width(ADC.WIDTH_10BIT) #resolución de 10 bits (0 a 1023)

pot3 = ADC(Pin(32))
pot3.width(ADC.WIDTH_12BIT) #resolucion 12bits (0 a 4095)
 
#Servos
servo1 = PWM(Pin(25), freq=50) #50 ciclos por segundo-1 ciclo cada 20ms
servo2 = PWM(Pin(19), freq=50)
servo3 = PWM(Pin(23), freq=50)
 
#LEDs y buzzer
led_verde = Pin(2, Pin.OUT) #led verde como salida
led_rojo  = Pin(4, Pin.OUT) #ñled rojo como salida
buzzer    = Pin(5, Pin.OUT) #buzzer como salida
 
#Botones
btn_reset = Pin(12, Pin.IN, Pin.PULL_UP) #boton con resistencia pull-up
btn_auto  = Pin(14, Pin.IN, Pin.PULL_UP)
 
modo = "manual" #variable que guarda el modo actual

last_interrupt_time = 0 #ultimo tiempo de interrupcion
debounce_ms = 200 #tiempo minimo entre las pulsaciones 200ms
 
#Ángulos actuales
ang_actual = [0, 0, 0]
 
def map_value(x, in_min, in_max, out_min, out_max):
    #convierte un valor de un rango a otro
    return int((x - in_min) * (out_max - out_min) / (in_max - in_min) + out_min)
 
def mover_servo(servo, angulo, idx):
    #Mueve el servo y guarda el ángulo actual
    if idx == 0:
        angulo = 180 - angulo #Invertir servo 1 porque se montó al reves
    duty = map_value(angulo, 0, 180, 26, 128) #convierte el angulo a ciclo de trabajo PWM
    servo.duty(duty) #aplica el ciclo al servo
    ang_actual[idx] = angulo  #Guarda ángulo actual en la lista
 
def mostrar_angulos():
    #Imprime los ángulos actuales de los 3 servos.
    print("Servo1: {}° | Servo2: {}° | Servo3: {}°".format(
        ang_actual[0], ang_actual[1], ang_actual[2]))
 
def posicion_inicial(): ##Mueve los 3 servos juntos desde 90 hasta 0 grados de "forma suave"
    print(">> RESET: volviendo a 0°")
    for i in range(90, -1, -2): ##Baja de 90 a 0 en pasos de 2
        mover_servo(servo1, i, 0)
        mover_servo(servo2, i, 1)
        mover_servo(servo3, i, 2)
        time.sleep(0.02) #Pausa para suavizar movimiento
    mostrar_angulos() #Muestra posicion final
 
def secuencia():
    #Ejecuta movimiento tipo ola, osea, cada servo se mueve uno despues del otro
    print(">> AUTO: iniciando secuencia ola")
    
    #Servo1 sube de 0 a 90
    for i in range(0, 91, 2):
        mover_servo(servo1, i, 0)
        time.sleep(0.02)
    mostrar_angulos()
    
    #Servo2 baja de 90 a 0
    for i in range(90, -1, -2):
        mover_servo(servo2, i, 1)
        time.sleep(0.02)
    mostrar_angulos()
    
    #Servo3 sube de 0 a 90
    for i in range(0, 91, 2):
        mover_servo(servo3, i, 2)
        time.sleep(0.02)
    mostrar_angulos()
 
def manejar_interrupcion(tipo):
     #Cambia el modo del sistema con anti-rebote para evitar pulsaciones falsas
    global modo, last_interrupt_time
    now = time.ticks_ms() #Tiempo actual en milisegundos
    if time.ticks_diff(now, last_interrupt_time) > debounce_ms: #Verifica que paso suficiente tiempo
        last_interrupt_time = now #Actualiza el tiempo de la ultima interrupcion
        modo = tipo #Cambia al nuevo modo
 
def ir_a_inicio(pin):
    manejar_interrupcion("reset") #cambia modo a reset
 
def rutina_auto(pin):
    manejar_interrupcion("auto") #cambia modo a auto

#Configura las interrupciones: se activan al presionar
btn_reset.irq(trigger=Pin.IRQ_FALLING, handler=ir_a_inicio)
btn_auto.irq(trigger=Pin.IRQ_FALLING, handler=rutina_auto)
 
# Contador para imprimir ángulos cada ~1 segundo en modo manual
last_print = 0
 
while True: #Bucle principal
 
    if modo == "manual": #modo manuel: pot se controlan
        led_verde.value(1) #led verde enciende
        led_rojo.value(0) #led rojo apagado
        buzzer.value(0) #buzzer apagado

        #Lee cada potenciometro 3 veces y promedia para estabilizar la lectura
        val1 = (pot1.read() + pot1.read() + pot1.read()) // 3
        val2 = (pot2.read() + pot2.read() + pot2.read()) // 3
        val3 = (pot3.read() + pot3.read() + pot3.read()) // 3
 
        #Convierte cada lectura del potenciometro a un angulo entre 0 y 180
        ang1 = map_value(val1, 0, 4095, 0, 180)
        ang2 = map_value(val2, 0, 1023, 0, 180)
        ang3 = map_value(val3, 0, 4095, 0, 180)
 
        #Mueve cada servo al angulo calculado
        mover_servo(servo1, ang1, 0)
        mover_servo(servo2, ang2, 1)
        mover_servo(servo3, ang3, 2)
 
        #Imprime ángulos cada 1 segundo sin bloquear el loop
        now = time.ticks_ms()
        if time.ticks_diff(now, last_print) >= 1000:
            mostrar_angulos()
            last_print = now #Actualiza el tiempo de la ultima impresion
 
        time.sleep(0.05) #Pequeñita pausa para no saturar el procesador
 
    elif modo == "reset": 
        led_verde.value(0)
        led_rojo.value(1)
        buzzer.value(1)
        posicion_inicial()
        buzzer.value(0)
        modo = "manual"
 
    elif modo == "auto":
        led_verde.value(0)
        led_rojo.value(1)
        buzzer.value(1)
        secuencia()
        buzzer.value(0)
        modo = "manual"