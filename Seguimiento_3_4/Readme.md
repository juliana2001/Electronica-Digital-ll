<body>  <div class="container"><h1>Dino Game</h1>
<p class="subtitle">
  Proyecto de procesamiento de señales y videojuego interactivo con ESP32
</p>

<div class="card">
  <h2>Descripción del Proyecto</h2>
  <p>
    Este proyecto consiste en el desarrollo de un videojuego tipo <b>Dino Runner</b>
    implementado en una ESP32 utilizando un joystick analógico, una pantalla OLED SSD1306
    y un buzzer.
  </p>

  <p>
    El sistema permite comparar el comportamiento de una señal analógica utilizando:
  </p>

  <ul>
    <li>Señal sin filtrar</li>
    <li>Señal filtrada mediante filtro exponencial</li>
  </ul>
</div>

<div class="card">
  <h2>Objetivos</h2>

  <h3>Objetivo General</h3>
  <p>
    Desarrollar un sistema interactivo basado en ESP32 que permita analizar el efecto
    del filtrado digital sobre señales analógicas provenientes de un joystick.
  </p>

  <h3>Objetivos Específicos</h3>
  <ul>
    <li>Adquirir señales analógicas mediante un joystick.</li>
    <li>Implementar un filtro exponencial.</li>
    <li>Comparar señales filtradas y sin filtrar.</li>
    <li>Diseñar una interfaz OLED interactiva.</li>
    <li>Desarrollar un videojuego en tiempo real.</li>
  </ul>
</div>

<div class="card">
  <h2>Componentes Utilizados</h2>

  <table>
    <tr>
      <th>Componente</th>
      <th>Descripción</th>
    </tr>
    <tr>
      <td>ESP32</td>
      <td>Microcontrolador principal</td>
    </tr>
    <tr>
      <td>OLED SSD1306</td>
      <td>Pantalla gráfica</td>
    </tr>
    <tr>
      <td>Joystick</td>
      <td>Entrada analógica</td>
    </tr>
    <tr>
      <td>Buzzer</td>
      <td>Retroalimentación sonora</td>
    </tr>
  </table>
</div>

<div class="card">
  <h2>Conexiones</h2>

  <table>
    <tr>
      <th>Dispositivo</th>
      <th>Pin ESP32</th>
    </tr>
    <tr>
      <td>OLED SDA</td>
      <td>GPIO 21</td>
    </tr>
    <tr>
      <td>OLED SCL</td>
      <td>GPIO 22</td>
    </tr>
    <tr>
      <td>Joystick Y</td>
      <td>GPIO 34</td>
    </tr>
    <tr>
      <td>Botón Joystick</td>
      <td>GPIO 27</td>
    </tr>
    <tr>
      <td>Buzzer</td>
      <td>GPIO 26</td>
    </tr>
  </table>
</div>

<div class="card">
  <h2>Funcionamiento del Sistema</h2>

  <p>El usuario puede:</p>

  <ul>
    <li>Seleccionar juego con o sin filtro.</li>
    <li>Escoger nivel de dificultad.</li>
    <li>Controlar el dinosaurio con el joystick.</li>
    <li>Visualizar señales en Serial Plotter.</li>
  </ul>
</div>

<div class="card">
  <h2>Procesamiento de Señales</h2>

  <h3>Señal Sin Filtrar</h3>
  <p>
    La lectura del joystick se utiliza directamente:
  </p>

  <code>raw = read_joystick()</code>

  <h3>Señal Filtrada</h3>
  <p>
    Se implementó un filtro exponencial:
  </p>

  <code>y = alpha * value + (1 - alpha) * y_prev</code>

  <p>
    Este filtro suaviza la señal y reduce el ruido.
  </p>
</div>

<div class="card">
  <h2>Mecánicas del Juego</h2>

  <ul>
    <li>El dinosaurio puede saltar obstáculos.</li>
    <li>Los cactus aparecen aleatoriamente.</li>
    <li>La dificultad modifica velocidad y frecuencia.</li>
    <li>El buzzer genera sonidos de interacción.</li>
  </ul>
</div>

<div class="card">
  <h2>Niveles de Dificultad</h2>

  <table>
    <tr>
      <th>Nivel</th>
      <th>Velocidad</th>
      <th>Frecuencia Obstáculos</th>
    </tr>
    <tr>
      <td>Fácil</td>
      <td>Baja</td>
      <td>Baja</td>
    </tr>
    <tr>
      <td>Intermedio</td>
      <td>Media</td>
      <td>Media</td>
    </tr>
    <tr>
      <td>Difícil</td>
      <td>Alta</td>
      <td>Alta</td>
    </tr>
  </table>
</div>

<div class="card">
  <h2>Resultados</h2>

  <ul>
    <li>La señal filtrada genera un movimiento más estable.</li>
    <li>El filtro exponencial reduce ruido y variaciones bruscas.</li>
    <li>La experiencia de juego mejora utilizando filtrado.</li>
  </ul>
</div>
<div class="section box">
        <h2>Autores</h2>
        <ul>
            <li>Juliana Areiza Cano</li>
            <li>Hanny Melissa Calle Sepúlveda</li>
            <li>Alex Salinas Vega</li>
            <li>Isabella Suaza Gomez</li>
        </ul>
    </div>

  </div>  <footer>
    Dino Game ESP32 | Procesamiento de Señales y Sistemas Embebidos
  </footer></body>
</html>
