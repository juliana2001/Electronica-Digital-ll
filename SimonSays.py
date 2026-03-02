from machine import Pin #se importa la clase PIN para controlar los pines
import time, random #modulos time y random para tiempos y generar numeros aleatorios
import micropython #para optimizar codigo

#Configuración de pines, se definen los pines de los LEDs y buzzer
LED_PINS = (2, 4, 5)
BUZZER_PIN = 18

#Configuración de botones jugador 1 y 2
J1_BTN_PINS = (12, 13, 14, 27)
J2_BTN_PINS = (32, 33, 25, 26)

#Configuración de boton inicio, final e interrupcion
BTN_INICIO_PIN = 19
BTN_FIN_PIN = 21
IRQ_MODO3_PIN = 23   

#Registros GPIO
GPIO_OUT_REG      = 0x3FF44004 #registro de salida
GPIO_OUT_W1TS_REG = 0x3FF44008 #registro para encender los LEDs
GPIO_OUT_W1TC_REG = 0x3FF4400C #registro para apagar los leds

LED_MASK = 0 #inicializacion de la mascara para LEDs
for p in LED_PINS:
    LED_MASK |= (1 << p) #crea mascara para los pines de los LEDs

#inicializa LEDs, Botones y buzzer.
leds = [Pin(p, Pin.OUT) for p in LED_PINS] #se define los LEDs como salida
buzzer = Pin(BUZZER_PIN, Pin.OUT) #buzzer como salida

botones_j1 = [Pin(p, Pin.IN, Pin.PULL_DOWN) for p in J1_BTN_PINS] #se definen los botones del jugador 1 como entradas con resistencia pull-down.
botones_j2 = [Pin(p, Pin.IN, Pin.PULL_DOWN) for p in J2_BTN_PINS] #se definen los botones del jugador 2 como entradas con resistencia pull-down.
btn_inicio = Pin(BTN_INICIO_PIN, Pin.IN, Pin.PULL_DOWN) #define boton de inicio
btn_fin = Pin(BTN_FIN_PIN, Pin.IN, Pin.PULL_DOWN) #define boton de fin
irq_pin = Pin(IRQ_MODO3_PIN, Pin.IN, Pin.PULL_UP) #define el pin de interrupcion  

#variables globales de puntaje
puntaje_j1 = 0 #puntaje inicial jugador 1
puntaje_j2 = 0 #puntaje inicial jugador 2
modo3_disparado = False #control de interrupcion para el modo 3
modo_actual = None #variable define el modo actual del juego

#Funciones para controlar los LEDs
def leds_off_mask(mask=LED_MASK):
    import machine
    machine.mem32[GPIO_OUT_W1TC_REG] = mask #apaga LEDs segun la masrcara

def leds_on_mask(mask):
    import machine
    machine.mem32[GPIO_OUT_W1TS_REG] = mask #enciende LEDs segun la mascara

def led_index_mask(i):
    pin = LED_PINS[i]
    return (1 << pin) #crea mascara para un solo pin

def leds_all_off():
    leds_off_mask(LED_MASK) #apaga todos los leds

def leds_show_index(i):
    import machine
    mask = led_index_mask(i) #crea mascara del led que se va a mostrar
    val = machine.mem32[GPIO_OUT_REG] #lee el valor actual de los registros GPIO
    machine.mem32[GPIO_OUT_REG] = (val & ~LED_MASK) | mask #modifica los registro GPIO para mostrar el led deseado

def apagar_salidas():
    leds_all_off() #apaga todos los leds
    buzzer.off() #apaga el buzzer

#Antirrebote e interrupciones
def antirrebote(btn, hold_ms=20):
    if btn.value() == 1: #si el boton está presionado
        time.sleep_ms(hold_ms) #espera un momentito para evitar rebotes
        return btn.value() == 1 #verifica si el boton sigue presionado
    return False

def sleep_con_interrupcion(segundos):
    global modo3_disparado
    fin_ms = time.ticks_add(time.ticks_ms(), int(segundos * 1000)) #calcula el tiempo de fin
    while time.ticks_diff(fin_ms, time.ticks_ms()) > 0: #mientras no haya pasado el tiempo
        if modo3_disparado:
            return 'irq' #si se detectó la interrupcion, regresa irq
        if antirrebote(btn_fin):
            return 'fin' #si el boton de fin se presiona, regres "fin"
        time.sleep_ms(10) #espera 10ms antes de verificar de nuevo
    return 'ok' #entonces, si no ocurrio ninguna interrupcion o fin, regresa "ok"

#Espera de las respuestas
def esperar_respuesta_1jugador(correcto):
    inicio = time.ticks_ms() #obtiene tiempo actual.
    while True:
        if antirrebote(btn_fin): #si el boton de fin se presiona
            return None, None #termina el juego
        if modo3_disparado: #si se dectetó interrupción
            return 'irq', None #regrea irq
        for i, btn in enumerate(botones_j1): #revisa botones del jugador 1
            if antirrebote(btn):
                fin = time.ticks_ms() #obtine el tiempo final de la pulsacion
                tiempo = time.ticks_diff(fin, inicio) #calcula el tiempo de la respuesta
                return (tiempo, 0) if i == correcto else (tiempo, -1) #regrea el tiempo y si fue correcto o no

def esperar_respuesta_2jugadores(correcto, ventana_ms=1500, limite_total_ms=10000):
    inicio = time.ticks_ms() #inicia el conteo del tiempo
    tiempos = {'JugadorUno': None, 'JugadorDos': None} #inicializa los tiempos de respuesta
    penal = {'JugadorUno': None, 'JugadorUno': None} #inicializa penalizaciones
    t_primera = None #variable para la primera pulsacion

    while True:
        if antirrebote(btn_fin): #si el boton fin se presiona
            return None, None #termina el juego
        if modo3_disparado: #si se dectecta la interrupcion
            return None, 'irq' #regresa irq
        
        #revisar las respuesta de los jugadores
        for i, btn in enumerate(botones_j1):
            if tiempos['JugadorUno'] is None and antirrebote(btn):
                fin = time.ticks_ms()
                tiempos['JugadorUno'] = time.ticks_diff(fin, inicio)
                penal['JugadorUno'] = 0 if i == correcto else -1
                if t_primera is None:
                    t_primera = fin #registra el primer tiempo de la primera respuesta

        for i, btn in enumerate(botones_j2):
            if tiempos['JugadorDos'] is None and antirrebote(btn):
                fin = time.ticks_ms()
                tiempos['JugadorDos'] = time.ticks_diff(fin, inicio)
                penal['JugadorDos'] = 0 if i == correcto else -1
                if t_primera is None:
                    t_primera = fin #registra el primer tiempo de la primera respuesta

        if tiempos['JugadorUno'] is not None and tiempos['JugadorDos'] is not None: #si ambos jugadores respondieron
            break

        if t_primera is not None:
            if time.ticks_diff(time.ticks_ms(), t_primera) >= ventana_ms: #si la ventana de repsuesta ha pasado
                break

        if time.ticks_diff(time.ticks_ms(), inicio) >= limite_total_ms: #si el tiempo total ha pasado
            break

        time.sleep_ms(5) #espera  un tiempito antes de continuar verificando

    return tiempos, penal #regresa los tiempos y las penalizaciones de los jugadores

#Rondas logica 
def ronda_generar_estimulo():
    estimulo = random.randint(0, 3) #genera un estimulo aleatorio (led o el buzzer)
    if estimulo == 3:
        buzzer.on() #si el estimulo es 3, enciende el buzzer
    else:
        leds_show_index(estimulo) #sino, entoncrs enciende un led
    return estimulo #devuelve el estimulo generado

#funcion para reproducir los estimulos y las secuencias
def reproducir_estimulo(estimulo, on_ms=350, off_ms=150):
    apagar_salidas()
    if estimulo == 3:
        buzzer.on()
    else:
        leds_show_index(estimulo)
    time.sleep_ms(on_ms)
    apagar_salidas()
    time.sleep_ms(off_ms)

def reproducir_secuencia(secuencia, on_ms=350, off_ms=150):
    for e in secuencia:
        reproducir_estimulo(e, on_ms=on_ms, off_ms=off_ms)

def leer_pulsacion(botones, timeout_ms=5000):
    inicio = time.ticks_ms()
    while time.ticks_diff(time.ticks_ms(), inicio) < timeout_ms:
        if antirrebote(btn_fin):
            return None
        for i, btn in enumerate(botones):
            if antirrebote(btn):
                reproducir_estimulo(i, on_ms=120, off_ms=40)
                return i
        time.sleep_ms(5)
    return 'timeout'

def verificar_secuencia(botones, secuencia, timeout_ms_por_tecla=5000):
    for esperado in secuencia:
        r = leer_pulsacion(botones, timeout_ms=timeout_ms_por_tecla)
        if r is None:
            return None
        if r == 'timeout' or r != esperado:
            return False
    return True

def juego_1jugador():
    #aquí se maneja el como funciona el juego cuando solo hay un jugador
    #y se gestionan todas las rondas, las puntuaciones y los estimulos
    global puntaje_j1, modo3_disparado, modo_actual
    modo_actual = "1jugador"
    modo3_disparado = False
    puntaje_j1 = 0
    ronda = 0
    print("Modo: 1 Jugador")
    print("Presiona botón INICIO para comenzar")
    while not antirrebote(btn_inicio):
        if modo3_disparado:
            juego_modo3()
            return
        time.sleep_ms(10)
    print("Juego iniciado!")

    while True:
        ronda += 1
        apagar_salidas()
        espera = random.randint(1, 10)
        s = sleep_con_interrupcion(espera)
        if s == 'fin':
            print("Juego finalizado")
            break
        if s == 'irq':
            juego_modo3()
            continue

        estimulo = ronda_generar_estimulo()
        print("Ronda {ronda}")
        print("Reacciona al estímulo {estimulo+1}")

        tiempo, penalizacion = esperar_respuesta_1jugador(estimulo)
        apagar_salidas()

        if tiempo is None and penalizacion is None:
            print("Juego finalizado")
            break
        if tiempo == 'irq':
            juego_modo3()
            continue

        if penalizacion == 0:
            puntaje_j1 += 1
            print("Correcto! Tiempo: {tiempo} ms | Puntaje jugador uno: {puntaje_j1}")
        else:
            puntaje_j1 -= 1
            print(f"Incorrecto! Tiempo: {tiempo} ms | Puntaje jugador uno: {puntaje_j1}")

        time.sleep(1)

    print("Puntaje final jugador uno: {puntaje_j1}")

def juego_2jugadores():
    #aquí se maneja el como funciona el juego cuando solo hay un jugador
    #y se gestionan todas las rondas, las puntuaciones y los estimulos

    global puntaje_j1, puntaje_j2, modo_actual, modo3_disparado
    modo_actual = "2jugadores"
    modo3_disparado = False
    puntaje_j1 = 0
    puntaje_j2 = 0
    ronda = 0
    print("Modo: 2 Jugadores")
    print("Presiona botón INICIO para comenzar...")
    while not antirrebote(btn_inicio):
        if modo3_disparado:
            juego_modo3()
            return
        time.sleep_ms(10)
    print("Juego iniciado!")

    while True:
        ronda += 1
        apagar_salidas()
        espera = random.randint(1, 10)
        s = sleep_con_interrupcion(espera)
        if s == 'fin':
            print("Juego finalizado")
            break
        if s == 'irq':
            juego_modo3()
            continue

        estimulo = ronda_generar_estimulo()
        print("Ronda {ronda}")
        print("Reacciona al estímulo {estimulo+1}")

        tiempos, penal = esperar_respuesta_2jugadores(estimulo)
        apagar_salidas()

        if tiempos is None and penal is None:
            print("Juego finalizado")
            break
        if penal == 'irq':
            juego_modo3()
            continue

        t1 = f"{tiempos['J1']} ms" if tiempos['J1'] is not None else "—"
        t2 = f"{tiempos['J2']} ms" if tiempos['J2'] is not None else "—"
        e1 = "Correcto" if penal['J1'] == 0 else ("Incorrecto" if penal['J1'] == -1 else "Sin respuesta")
        e2 = "Correcto" if penal['J2'] == 0 else ("Incorrecto" if penal['J2'] == -1 else "Sin respuesta")

        print(f"J1: {t1} ({e1})")
        print(f"J2: {t2} ({e2})")

        if penal['J1'] == -1:
            puntaje_j1 -= 1
            print("J1 se equivoca: -1 punto.")
        if penal['J2'] == -1:
            puntaje_j2 -= 1
            print("J2 se equivoca: -1 punto.")

        candidatos = []
        if penal['J1'] == 0 and tiempos['J1'] is not None:
            candidatos.append(('J1', tiempos['J1']))
        if penal['J2'] == 0 and tiempos['J2'] is not None:
            candidatos.append(('J2', tiempos['J2']))

        if len(candidatos) == 2:
            if candidatos[0][1] < candidatos[1][1]:
                puntaje_j1 += 1
                print("Punto por mejor tiempo: Jugador 1.")
            elif candidatos[1][1] < candidatos[0][1]:
                puntaje_j2 += 1
                print("Punto por mejor tiempo: Jugador 2.")
            else:
                puntaje_j1 += 1
                puntaje_j2 += 1
                print("Empate perfecto: ambos +1.")
        elif len(candidatos) == 1:
            if candidatos[0][0] == 'J1':
                puntaje_j1 += 1
                print("Punto para Jugador 1 (único correcto).")
            else:
                puntaje_j2 += 1
                print("Punto para Jugador 2 (único correcto).")
        else:
            print("Nadie acierta.")

        print("Marcador — Jugador 1: {puntaje_j1} | Jugador 2: {puntaje_j2}")
        time.sleep(1)

    print("Puntaje final — J1: {puntaje_j1} | J2: {puntaje_j2}")
    if puntaje_j1 > puntaje_j2:
        print("Ganador: Jugador 1")
    elif puntaje_j2 > puntaje_j1:
        print("Ganador: Jugador 2")
    else:
        print("Empate!")

#Interrupción
#Aqui se configura la interrupcion para Simon dice o el modo 3. Se utilizan
#el pin IRQ_MODO3_PIN para activar el modo 3 cuando el pin detecta un cambio de nivel
#(o sea de alto a bajo).

#La variable last_irq_ms se utiliza para evitar que simon dice repetidamente
#si no ha pasado suficiente tiempo desde la ultima interrupcion.
last_irq_ms = 0 #Varaible para controlar el tiempo entre las interrupciones
def _irq_handler(pin):
    global modo3_disparado, last_irq_ms
    now = time.ticks_ms() #obtiene el tiempo actual
    if time.ticks_diff(now, last_irq_ms) > 150: #si ha pasado mucho tiempo
        modo3_disparado = True #activa el modo de simon dice
        last_irq_ms = now #Actualiza el tiempo de la ultima interrupcion

irq_pin.irq(trigger=Pin.IRQ_FALLING, handler=_irq_handler)

#simon dice
#Esta es la logica para el jeugo simon dice. LOs jugadores deben memorizar
#repetir una secuencia de estimulos. Entonces a medida que avanzan en
#los niveles, la velocidad de los estimulos aumenta.

#Entonceees, si el jugador presiona boton fin, juego se cancela
#si jugador acierta, avanza nivel siguiente
#si falla, termina juego y muestra nivel alcanzado.
#en modo de dos jugadores, ambos jugadores deben repetir la secuencia en cada turno
#y el jugador mas rapido, en acertar tiene el punto"""

def juego_modo3():
    global modo3_disparado, modo_actual
    print("MODO 3 (SIMÓN DICE) ACTIVADO")
    print("Memoriza la secuencia y repítela.")
    print("FIN: salir/cancelar")
    print("INICIO: comenzar")
    modo3_disparado = False #desactiva el modo 3 al inicio

    if modo_actual not in ("1jugador", "2jugadores"):
        modo_actual = "1jugador" #si no hay modo actual, se establece como 1 jugador

    while not antirrebote(btn_inicio): #espera hasta que se presione el boton de inicio
        if antirrebote(btn_fin): #si se presioba el boton de fin, termina el juego
            print("Cancelado por usuario.")
            modo3_disparado = False
            apagar_salidas()
            return
        time.sleep_ms(10)

    nivel = 0 #nivel inicia el juego
    secuencia = [] #almacena la secuencia de los estimulos

    # Ajuste leve de velocidad: a mayor nivel, más rápido.
    while True:
        if antirrebote(btn_fin): #si se preciona el boton fin, termina el juego
            print("Cancelado por usuario.")
            modo3_disparado = False
            apagar_salidas()
            return

        nivel += 1 #aumenta el nivel en cada ronda
        secuencia.append(random.randint(0, 3)) #genera un estimulo aleatorio para la secuencia

        on_ms = max(140, 380 - (nivel * 15))
        off_ms = max(60, 180 - (nivel * 5))

        print("Nivel {nivel}")
        print("Mira...")
        time.sleep_ms(300)
        reproducir_secuencia(secuencia, on_ms=on_ms, off_ms=off_ms) #reproduce la secuencia generada
        apagar_salidas()

        if modo_actual == "1jugador":
            print("Tu turno: repite la secuencia")
            ok = verificar_secuencia(botones_j1, secuencia, timeout_ms_por_tecla=5000) #verifica si el jugador 1 repitio correctamente la secuencia
            if ok is None:
                print("Cancelado por usuario.")
                modo3_disparado = False
                apagar_salidas()
                return
            if ok: #si el jugador respondio correctamente
                print("¡Bien! Pasas al siguiente nivel.")
                time.sleep_ms(400)
                continue

            # si el jugador falla, termina el juego y muestra el nivel que se alcanzó
            alcanzado = max(0, nivel - 1)
            print(f"Fallaste. Nivel alcanzado: {alcanzado}")
            modo3_disparado = False
            apagar_salidas()
            return

        else:
            print("Turno Jugador 1: repite la secuencia")
            ok1 = verificar_secuencia(botones_j1, secuencia, timeout_ms_por_tecla=5000) #verifica respuesta del jugador 1
            if ok1 is None:
                print("Cancelado por usuario.")
                modo3_disparado = False
                apagar_salidas()
                return

            print("Turno Jugador 2: repite la secuencia")
            ok2 = verificar_secuencia(botones_j2, secuencia, timeout_ms_por_tecla=5000) #verifica respuesta del jugador 2
            if ok2 is None:
                print("Cancelado por usuario.")
                modo3_disparado = False
                apagar_salidas()
                return
            
        #verifica quien respondió correctamente más rapido y asigna el punto
            if ok1 and ok2:
                print("¡Los dos acertaron! Siguiente nivel...")
                time.sleep_ms(500)
                continue

            alcanzado = max(0, nivel - 1)
            if ok1 and not ok2:
                print(f"Jugador 2 falló. Gana Jugador 1. Nivel alcanzado: {alcanzado}")
            elif ok2 and not ok1:
                print(f"Jugador 1 falló. Gana Jugador 2. Nivel alcanzado: {alcanzado}")
            else:
                print(f"Los dos fallaron. Empate. Nivel alcanzado: {alcanzado}")

            modo3_disparado = False
            apagar_salidas()
            return

def main():

    global modo_actual
    print("Juego de Reflejos (ESP32)")
    print("LEDs por REGISTROS")
    print("Modo 3 por interrupción en GPIO", IRQ_MODO3_PIN)
    while True:
        print("Menú:")
        print("1. Juego de 1 jugador")
        print("2. Juego de 2 jugadores")
        opcion = input("Selecciona una opcion: ")

        if opcion == "1":
            juego_1jugador() #llama a la funcion para el jeugo de una sola persona
        elif opcion == "2":
            juego_2jugadores() #llama a la funcion para el juego de dos jugadores
        else:
            print("Opción invalida") #si se selcciona otra cosa, pues opcion no valida

#Aqui se apagan los LEDs y el buzzer antes de finalizar el juego
#y luego vuelve a llamar main para reiniciar el ciclo

apagar_salidas() #apaga todos los leds y el buzzer al final del programa
leds_all_off() #asegura que todos los leds esten apagados
main() #llama a la funcion principal para iniciar el juego