<h1 align="center">Juego de Reflejos y Simón Dice con ESP32</h1>

<p align="center">
Proyecto desarrollado en <b>MicroPython</b> sobre <b>ESP32</b> que implementa un sistema interactivo de reflejos
para 1 y 2 jugadores, incluyendo un modo especial tipo <b>Simón Dice</b> activado mediante interrupción externa.
</p>

<hr>

<h2>Descripción General</h2>

<p>
Este proyecto implementa un sistema embebido interactivo basado en ESP32 donde los jugadores deben reaccionar
a estímulos luminosos o sonoros en el menor tiempo posible.
</p>

<p>
El sistema incluye:
</p>

<ul>
<li>Juego de reflejos para 1 jugador</li>
<li>Juego competitivo para 2 jugadores</li>
<li>Modo especial “Simón Dice” con dificultad progresiva</li>
<li>Activación mediante interrupción por hardware</li>
<li>Control directo de registros GPIO para mayor eficiencia</li>
<li>Medición precisa de tiempos de reacción</li>
<li>Antirrebote por software</li>
</ul>

<hr>

<h2>Hardware Utilizado</h2>

<ul>
<li>ESP32</li>
<li>3 LEDs</li>
<li>1 Buzzer</li>
<li>8 Pulsadores (4 por jugador)</li>
<li>1 Botón INICIO</li>
<li>1 Botón FIN</li>
<li>1 Botón de Interrupción (Modo 3)</li>
<li>Protoboard y resistencias</li>
</ul>

<hr>

<h2>Configuración de Pines</h2>

<h3>LEDs</h3>
<table border="1">
<tr><th>Dispositivo</th><th>GPIO</th></tr>
<tr><td>LED 1</td><td>2</td></tr>
<tr><td>LED 2</td><td>4</td></tr>
<tr><td>LED 3</td><td>5</td></tr>
</table>

<h3>Buzzer</h3>
<table border="1">
<tr><th>Dispositivo</th><th>GPIO</th></tr>
<tr><td>Buzzer</td><td>18</td></tr>
</table>

<h3>Jugador 1</h3>
<table border="1">
<tr><th>Botón</th><th>GPIO</th></tr>
<tr><td>BTN1</td><td>12</td></tr>
<tr><td>BTN2</td><td>13</td></tr>
<tr><td>BTN3</td><td>14</td></tr>
<tr><td>BTN4</td><td>27</td></tr>
</table>

<h3>Jugador 2</h3>
<table border="1">
<tr><th>Botón</th><th>GPIO</th></tr>
<tr><td>BTN1</td><td>32</td></tr>
<tr><td>BTN2</td><td>33</td></tr>
<tr><td>BTN3</td><td>25</td></tr>
<tr><td>BTN4</td><td>26</td></tr>
</table>

<h3>Control</h3>
<table border="1">
<tr><th>Función</th><th>GPIO</th></tr>
<tr><td>INICIO</td><td>19</td></tr>
<tr><td>FIN</td><td>21</td></tr>
<tr><td>Modo 3 (IRQ)</td><td>23</td></tr>
</table>

<hr>

<h2>Arquitectura del Software</h2>

<p>El sistema está estructurado en módulos funcionales:</p>

<ul>
<li>Inicialización y configuración de pines</li>
<li>Control de LEDs mediante acceso directo a registros</li>
<li>Gestión de antirrebote</li>
<li>Gestión de interrupciones externas</li>
<li>Lógica de juegos</li>
<li>Menú interactivo principal</li>
</ul>

<hr>

<h2> Control Directo por Registros</h2>

<p>
El sistema manipula directamente los registros GPIO del ESP32:
</p>

<pre>
GPIO_OUT_REG      = 0x3FF44004
GPIO_OUT_W1TS_REG = 0x3FF44008
GPIO_OUT_W1TC_REG = 0x3FF4400C
</pre>

<p><b>Ventajas técnicas:</b></p>

<ul>
<li>Mayor velocidad de ejecución</li>
<li>Operaciones atómicas</li>
<li>Mejor rendimiento en juegos de reacción</li>
<li>Acceso a bajo nivel (programación embebida avanzada)</li>
</ul>

<hr>

<h2>Modos de Juego</h2>

<h3> Juego 1 Jugador</h3>
<ul>
<li>Generación de estímulo aleatorio (LED o buzzer)</li>
<li>Medición de tiempo de reacción</li>
<li>+1 punto por acierto</li>
<li>-1 punto por error</li>
</ul>

<h3> Juego 2 Jugadores</h3>
<ul>
<li>Competencia simultánea</li>
<li>Evaluación de tiempo y precisión</li>
<li>Punto para el más rápido si ambos aciertan</li>
<li>Penalización por error</li>
</ul>

<h3>Modo Simón Dice (Activado por Interrupción)</h3>
<ul>
<li>Secuencia acumulativa</li>
<li>Dificultad progresiva</li>
<li>Soporte para 1 o 2 jugadores</li>
<li>Cancelable con botón FIN</li>
</ul>

<hr>

<h2>Interrupciones</h2>

<p>
El modo 3 se activa mediante interrupción por flanco descendente en GPIO 23.
Incluye sistema de protección contra rebote temporal (150 ms).
</p>

<hr>

<h2>Medición de Tiempo</h2>

<p>
Se emplean funciones de alta precisión:
</p>

<pre>
time.ticks_ms()
time.ticks_diff()
</pre>

<p>
Permiten medir latencias en milisegundos para evaluar reflejos con precisión.
</p>

<hr>

<h2>Estructura del Proyecto</h2>

<pre>
Proyecto-ESP32-JuegoReflejos/
│
├── main.py
├── README.html
└── esquema_conexion.png
</pre>

<hr>

<h2>Instrucciones de Uso</h2>

<ol>
<li>Instalar firmware MicroPython en el ESP32</li>
<li>Subir el archivo <b>main.py</b></li>
<li>Reiniciar la placa</li>
<li>Abrir consola serial</li>
<li>Seleccionar modo desde el menú</li>
</ol>

<hr>

<h2>Conceptos Aplicados</h2>

<ul>
<li>Programación de sistemas embebidos</li>
<li>Manipulación de registros hardware</li>
<li>Manejo de interrupciones</li>
<li>Antirrebote por software</li>
<li>Programación modular</li>
<li>Medición de latencia en tiempo real</li>
<li>Diseño de lógica competitiva</li>
</ul>

<hr>

<h2>Mejoras Futuras</h2>

<ul>
<li>Integración con pantalla OLED</li>
<li>Almacenamiento de récord en memoria flash</li>
<li>Interfaz gráfica</li>
<li>Control por FreeRTOS</li>
<li>Efectos PWM avanzados para buzzer</li>
</ul>
