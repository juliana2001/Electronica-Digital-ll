<h1 align="center">Monitor IoT Biomédico con ESP32</h1>

<p align="center">
Sistema IoT biomédico desarrollado con ESP32 para monitoreo de temperatura,
humedad y movimiento en tiempo real, incluyendo alertas sonoras,
servidor web local y notificaciones mediante Telegram.
</p>

<h2>Objetivo</h2>

<p>
Desarrollar un sistema de monitoreo biomédico basado en IoT capaz de detectar condiciones críticas relacionadas con variables ambientales y movimiento, permitiendo supervisión local y remota.
</p>
<hr>
<h2>Funcionalidades</h2>

<ul>
    <li>✅ Monitoreo de temperatura</li>
    <li>✅ Monitoreo de humedad</li>
    <li>✅ Detección de movimiento</li>
    <li>✅ Detección de movimiento brusco</li>
    <li>✅ Buzzer de alerta</li>
    <li>✅ Botón de pánico</li>
    <li>✅ Página web local en tiempo real</li>
    <li>✅ Notificaciones mediante Telegram</li>
    <li>✅ Comunicación WiFi con ESP32</li>
</ul>
<hr>
<h2>Componentes Utilizados</h2>

<table>

<tr>
<th>Componente</th>
<th>Función</th>
</tr>

<tr>
<td>ESP32</td>
<td>Microcontrolador principal</td>
</tr>

<tr>
<td>DHT11</td>
<td>Sensor de temperatura y humedad</td>
</tr>

<tr>
<td>MPU6500</td>
<td>Sensor acelerómetro y giroscopio</td>
</tr>

<tr>
<td>Buzzer pasivo</td>
<td>Alarmas sonoras</td>
</tr>

<tr>
<td>Botón pulsador</td>
<td>Botón de pánico</td>
</tr>

<tr>
<td>Protoboard</td>
<td>Montaje del circuito</td>
</tr>

<tr>
<td>Cables Dupont</td>
<td>Conexiones</td>
</tr>

</table>

<hr>

<h2>Conexiones</h2>

<h3>DHT11</h3>

<table>

<tr>
<th>DHT11</th>
<th>ESP32</th>
</tr>

<tr>
<td>VCC</td>
<td>3.3V</td>
</tr>

<tr>
<td>GND</td>
<td>GND</td>
</tr>

<tr>
<td>DATA</td>
<td>GPIO15</td>
</tr>

</table>

<br>

<h3>MPU6500</h3>

<table>

<tr>
<th>MPU6500</th>
<th>ESP32</th>
</tr>

<tr>
<td>VCC</td>
<td>3.3V</td>
</tr>

<tr>
<td>GND</td>
<td>GND</td>
</tr>

<tr>
<td>SDA</td>
<td>GPIO21</td>
</tr>

<tr>
<td>SCL</td>
<td>GPIO22</td>
</tr>

</table>

<br>

<h3>Buzzer</h3>

<table>

<tr>
<th>Buzzer</th>
<th>ESP32</th>
</tr>

<tr>
<td>+</td>
<td>GPIO18</td>
</tr>

<tr>
<td>-</td>
<td>GND</td>
</tr>

</table>

<br>

<h3>Botón</h3>

<table>

<tr>
<th>Botón</th>
<th>ESP32</th>
</tr>

<tr>
<td>Pin 1</td>
<td>GPIO4</td>
</tr>

<tr>
<td>Pin 2</td>
<td>GND</td>
</tr>

</table>

<hr>

<h2>Estructura del Proyecto</h2>

<pre>
 proyecto-iot-biomedico
│
├── main.py
├── mpu6500.py
├── utelegram.py
└── README.md
</pre>

<hr>

<h2>Descripción de Archivos</h2>

<h3>main.py</h3>

<p>
Archivo principal del sistema.
</p>

<p>
Contiene:
</p>

<ul>
    <li>Conexión WiFi</li>
    <li>Lectura de sensores</li>
    <li>Servidor web</li>
    <li>Alertas</li>
    <li>Telegram</li>
    <li>Lógica principal del proyecto</li>
</ul>

<br>

<h3>mpu6500.py</h3>

<p>
Librería utilizada para controlar el sensor MPU6500 mediante comunicación I2C.
</p>

<p>
Permite:
</p>

<ul>
    <li>Leer aceleración</li>
    <li>Leer giroscopio</li>
    <li>Calcular movimiento</li>
</ul>

<br>

<h3>utelegram.py</h3>

<p>
Librería utilizada para la conexión entre el ESP32 y Telegram Bot API.
</p>

<p>
Permite:
</p>

<ul>
    <li>Enviar mensajes</li>
    <li>Crear bots</li>
    <li>Gestionar notificaciones</li>
</ul>

<hr>

<h2>Servidor Web</h2>

<p>
El ESP32 crea una página web local donde se visualizan:
</p>

<ul>
    <li>Temperatura</li>
    <li>Humedad</li>
    <li>Movimiento</li>
    <li>Estado de alarma</li>
</ul>

<p>
Acceso desde navegador:
</p>

<pre>
http://IP_DEL_ESP32
</pre>

<p>
Ejemplo:
</p>

<pre>
http://172.16.226.58
</pre>

<hr>

<h2>Configuración Telegram</h2>

<h3>1️1. Crear Bot</h3>

<p>
Buscar en Telegram:
</p>

<pre>
@BotFather
</pre>

<p>
Crear bot:
</p>

<pre>
/newbot
</pre>

<br>

<h3>2️. Obtener TOKEN</h3>

<p>
BotFather entregará:
</p>

<pre>
123456789:AAxxxxxxxxxxxxxxxx
</pre>

<br>

<h3>3️. Obtener Chat ID</h3>

<p>
Abrir:
</p>

<pre>
https://api.telegram.org/botTU_TOKEN/getUpdates
</pre>

<hr>

<h2>Alertas Implementadas</h2>

<table>

<tr>
<th>Evento</th>
<th>Acción</th>
</tr>

<tr>
<td>Temperatura alta</td>
<td>Buzzer + Telegram</td>
</tr>

<tr>
<td>Temperatura baja</td>
<td>Buzzer + Telegram</td>
</tr>

<tr>
<td>Humedad alta</td>
<td>Buzzer + Telegram</td>
</tr>

<tr>
<td>Humedad baja</td>
<td>Buzzer + Telegram</td>
</tr>

<tr>
<td>Movimiento brusco</td>
<td>Buzzer + Telegram</td>
</tr>

<tr>
<td>Botón de pánico</td>
<td>Buzzer + Telegram</td>
</tr>

</table>

<hr>

<h2>Tecnologías Utilizadas</h2>

<ul>
    <li>MicroPython</li>
    <li>ESP32</li>
    <li>HTML</li>
    <li>CSS</li>
    <li>IoT</li>
    <li>Telegram Bot API</li>
    <li>Comunicación I2C</li>
</ul>

<hr>

<h2>Futuras Mejoras</h2>

<ul>
    <li>Integración con Firebase</li>
    <li>Base de datos histórica</li>
    <li>Gráficas en tiempo real</li>
    <li>Aplicación móvil</li>
    <li>Integración con sensores biomédicos reales</li>
    <li>Optimización energética</li>
    <li>Inteligencia artificial</li>
</ul>

<hr>

<h2>Vista General del Sistema</h2>

<pre>
Sensores → ESP32 → Página Web
                 → Telegram
                 → Buzzer
</pre>

<hr>

<h2>Autores</h2>
<ul>
            <li>Juliana Areiza Cano</li>
            <li>Hanny Melissa Calle Sepúlveda</li>
            <li>Alex Salinas Vega</li>
            <li>Isabella Suaza Gomez</li>
  </ul>
<p>
Proyecto desarrollado para aplicaciones de monitoreo IoT biomédico en Ingeniería Biomédica. ITM.
</p>
