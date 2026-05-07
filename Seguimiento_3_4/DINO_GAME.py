from machine import Pin, I2C, ADC, PWM #I2C comunicacion con la pantalla OLED,
import ssd1306 #libreria de la pantalla
import utime #manejo del tiempo
import urandom #numeros aleatorios

#random se usa para la altura, ancho, tiempo de aparición
def rand_range(a, b):
    return a + (urandom.getrandbits(16) % (b - a + 1))

#definicion de los pines 
I2C_SCL = 22
I2C_SDA = 21
OLED_W = 128
OLED_H = 64

JOY_Y_PIN = 34
JOY_SW_PIN = 27
BUZZER_PIN = 26

PLOT_ENABLED = True
PLOT_INTERVAL_MS = 40

GROUND_LINE_Y = 54

DINO_X = 18
DINO_W = 10
DINO_H = 12

#Fisica del dino
GRAVITY = 0.7 #gravedad
JUMP_VELOCITY = -8.1 #velocidad negativa al subir (o sea, gravedad positiva lo sube y velocidad negativa, lo baja)

JUMP_THRESHOLD = 3000 #umbral del joystick para dectetar salto
JUMP_WHEN_HIGH = True

MENU_UP_THRESHOLD = 3000
MENU_DOWN_THRESHOLD = 1200

i2c = I2C(0, scl=Pin(I2C_SCL), sda=Pin(I2C_SDA), freq=400000) #crea el canal de comunicación con la OLED
oled = ssd1306.SSD1306_I2C(OLED_W, OLED_H, i2c) #inicializa la pantalla

joy_y = ADC(Pin(JOY_Y_PIN)) #lee el eje vertical del joystick
joy_y.atten(ADC.ATTN_11DB) #ATTN_11DB permite leer hasta 3.3v

joy_sw = Pin(JOY_SW_PIN, Pin.IN, Pin.PULL_UP)

buzzer = PWM(Pin(BUZZER_PIN))
buzzer.duty(0)

#funciones que son mas que todo para retroalimentacion sensorial
def beep(freq=1200, duration=80, duty=300):
    buzzer.freq(freq)
    buzzer.duty(duty)
    utime.sleep_ms(duration)
    buzzer.duty(0)

def menu_beep():
    beep(1400, 60, 250)

def jump_beep():
    beep(1800, 40, 220)

def score_beep():
    beep(2200, 25, 180)

def game_over_beep():
    tones = [700, 600, 500, 350]
    for t in tones:
        buzzer.freq(t)
        buzzer.duty(350)
        utime.sleep_ms(120)
        buzzer.duty(0)
        utime.sleep_ms(30)

#filtro exponencial: suaviza la señal del joystick porque ADC tiene mucho ruido
        #entonces, se supone que sin filtro, va a tener saltos falsos en cambio con filtro, la señal es estable
        #se eligió exponencial porque es rapido, poco retardo y bajo costo
class ExponentialFilter:
    def __init__(self, alpha=0.25):
        self.alpha = alpha
        self.y = None

    def update(self, value):
        if self.y is None:
            self.y = value
        else:
            self.y = self.alpha * value + (1 - self.alpha) * self.y
        return self.y

def safe_hline(x, y, length, color):
    for i in range(length):
        px = x + i
        if 0 <= px < OLED_W and 0 <= y < OLED_H:
            oled.pixel(px, y, color)

def safe_fill_rect(x, y, w, h, color): #dibuja pixeles sin salirse de pantalla
    for i in range(w):
        for j in range(h):
            px = x + i
            py = y + j
            if 0 <= px < OLED_W and 0 <= py < OLED_H:
                oled.pixel(px, py, color)

#dinujito dino, se construye el peronaje con rectagunlos 
def draw_dino(x, y):
    safe_fill_rect(x, y, 8, 10, 1)
    safe_fill_rect(x + 6, y - 4, 6, 6, 1)
    safe_fill_rect(x + 1, y + 10, 2, 3, 1)
    safe_fill_rect(x + 5, y + 10, 2, 3, 1)

#dibujo cactus
def draw_cactus(x, y, w, h):
    safe_fill_rect(x, y, w, h, 1)
    if h >= 10:
        safe_fill_rect(x - 2, y + 4, 2, 4, 1)
    if h >= 12:
        safe_fill_rect(x + w, y + 6, 2, 4, 1)

#dibujo suelo
def draw_ground():
    safe_hline(0, GROUND_LINE_Y + 12, OLED_W, 1)

#dibujo puntaje
def draw_score(score, difficulty):
    oled.text("P:%d" % score, 0, 0)

    if difficulty == "facil":
        txt = "FAC"
    elif difficulty == "intermedio":
        txt = "INT"
    else:
        txt = "DIF"

    oled.text(txt, 92, 0)

def show_start_message():
    oled.fill(0)
    oled.text("DINO READY", 20, 20)
    oled.text("Iniciando...", 18, 34)
    oled.show()
    menu_beep()
    utime.sleep_ms(700)

def show_game_over(score):
    oled.fill(0)
    oled.text("GAME OVER", 22, 18)
    oled.text("Puntaje:%d" % score, 16, 34)
    oled.text("Pulsa boton", 14, 48)
    oled.show()

def show_end_message():
    oled.fill(0)
    oled.text("Fin del juego", 14, 28)
    oled.show()

def pause_game():
    oled.fill(0)
    oled.text("PAUSA", 40, 20)
    oled.text("Pulsa boton", 10, 40)
    oled.show()

    wait_button_release()
    wait_for_button_press()

#detecta si dino y cactus se tocan
def rect_collision(ax, ay, aw, ah, bx, by, bw, bh):
    return (
        ax < bx + bw and
        ax + aw > bx and
        ay < by + bh and
        ay + ah > by
    )

def read_joystick():
    return joy_y.read()

def button_pressed():
    return joy_sw.value() == 0

def wait_button_release(): #detecta boton, 0 si esta espichado, 1 si esta suelto
    while button_pressed():
        utime.sleep_ms(20)

def wait_for_button_press(): #evita lecturas falsas
    while True:
        if button_pressed():
            utime.sleep_ms(30)
            if button_pressed():
                menu_beep()
                wait_button_release()
                return
        utime.sleep_ms(20)

#envia los datos al pc
def send_plot_data(raw, signal_value):
    if PLOT_ENABLED:
        print("raw:{},signal:{},threshold:{}".format(
            int(raw), int(signal_value), int(JUMP_THRESHOLD)
        ))

#sistema de navegacion, aqui se convierte el joystick en lo arriba/abajo y el boton en seleccion
def draw_menu(title, options, selected):
    oled.fill(0)
    oled.text(title, 0, 0)

    y = 16
    for i in range(len(options)):
        prefix = ">" if i == selected else " "
        oled.text(prefix + options[i], 0, y)
        y += 14

    oled.show()

def menu_oled(title, options):
    selected = 0
    last_move_time = utime.ticks_ms()

    while True:
        draw_menu(title, options, selected)
        value = read_joystick()
        now = utime.ticks_ms()

        if utime.ticks_diff(now, last_move_time) > 220:
            moved = False

            if value > MENU_UP_THRESHOLD:
                selected -= 1
                if selected < 0:
                    selected = len(options) - 1
                moved = True

            elif value < MENU_DOWN_THRESHOLD:
                selected += 1
                if selected >= len(options):
                    selected = 0
                moved = True

            if moved:
                last_move_time = now

        if button_pressed():
            utime.sleep_ms(30)
            if button_pressed():
                menu_beep()
                wait_button_release()
                return selected

        utime.sleep_ms(30)

def choose_filter_mode():
    idx = menu_oled("MENU", ["Filtrado", "Sin filtrar"])
    return "filtrado" if idx == 0 else "sin_filtrar"

def choose_difficulty():
    idx = menu_oled("Dificultad", ["Facil", "Intermedio", "Dificil"])
    return ["facil", "intermedio", "dificil"][idx]

def ask_play_again():
    idx = menu_oled("Otra vez?", ["Si", "No"])
    return idx == 0

def run_game(filter_mode, difficulty):
    if difficulty == "facil":
        obstacle_speed = 2
        spawn_min = 1600
        spawn_max = 2400
    elif difficulty == "intermedio":
        obstacle_speed = 3
        spawn_min = 1300
        spawn_max = 2000
    else:
        obstacle_speed = 4
        spawn_min = 1000
        spawn_max = 1600

    filt = ExponentialFilter(alpha=0.25)

    dino_y = GROUND_LINE_Y
    dino_vy = 0
    jumping = False

    obstacles = []
    last_spawn = utime.ticks_ms()
    next_spawn_delay = rand_range(spawn_min, spawn_max)

    score = 0
    last_score_time = utime.ticks_ms()
    last_plot_time = utime.ticks_ms()

    show_start_message()

#loop principaaaaal
    while True:
        now = utime.ticks_ms()

        if button_pressed():
            utime.sleep_ms(30)
            if button_pressed(): #permite interrumpir el flujo en tiempo real
                menu_beep()
                pause_game()

                now = utime.ticks_ms()
                last_spawn = now
                last_score_time = now
                last_plot_time = now

        raw = read_joystick() #lectura
        signal_value = filt.update(raw) if filter_mode == "filtrado" else raw #filtrado

        if utime.ticks_diff(now, last_plot_time) >= PLOT_INTERVAL_MS:
            send_plot_data(raw, signal_value)
            last_plot_time = now

        jump_detected = signal_value > JUMP_THRESHOLD if JUMP_WHEN_HIGH else signal_value < JUMP_THRESHOLD #salto

        if jump_detected and (not jumping) and (dino_y >= GROUND_LINE_Y):
            dino_vy = JUMP_VELOCITY
            jumping = True
            jump_beep()

        dino_y += dino_vy
        dino_vy += GRAVITY

        if dino_y >= GROUND_LINE_Y:
            dino_y = GROUND_LINE_Y
            dino_vy = 0
            jumping = False

        can_spawn = True
        if len(obstacles) > 0 and obstacles[-1]["x"] > 95:
            can_spawn = False

        if utime.ticks_diff(now, last_spawn) >= next_spawn_delay and can_spawn:
            h = rand_range(8, 16)
            w = rand_range(4, 8)
            y = GROUND_LINE_Y + 12 - h

            obstacles.append({"x": OLED_W, "y": y, "w": w, "h": h, "passed": False})
            last_spawn = now
            next_spawn_delay = rand_range(spawn_min, spawn_max)

        for obs in obstacles:
            obs["x"] -= obstacle_speed

        obstacles = [obs for obs in obstacles if obs["x"] + obs["w"] > 0]

        if utime.ticks_diff(now, last_score_time) >= 250:
            score += 1
            last_score_time = now

        for obs in obstacles:
            if (not obs["passed"]) and (obs["x"] + obs["w"] < DINO_X):
                score += 5
                obs["passed"] = True
                score_beep()

        for obs in obstacles:
            if rect_collision(DINO_X, int(dino_y), DINO_W, DINO_H,
                              obs["x"], obs["y"], obs["w"], obs["h"]): #colision
                show_game_over(score)
                game_over_beep()
                wait_for_button_press()
                return score

        oled.fill(0) #se borra porque la oled no tiene Frames, es masnual
        draw_score(score, difficulty)
        draw_ground()
        draw_dino(DINO_X, int(dino_y))

        for obs in obstacles:
            draw_cactus(obs["x"], obs["y"], obs["w"], obs["h"])

        oled.show()
        utime.sleep_ms(35)

def main():
    while True: #reinicia el juego 
        filter_mode = choose_filter_mode()
        difficulty = choose_difficulty()
        run_game(filter_mode, difficulty)

        if not ask_play_again():
            show_end_message()
            return

main()