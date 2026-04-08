<h1>Sistema de Grúa Robótica con ESP32</h1>

  <div class="section box">
      <p>
            Proyecto desarrollado en <strong>Electrónica Digital II</strong>, que implementa una grúa robótica con 
            <strong>3 grados </strong>, controlada mediante potenciómetros y gestionada por un ESP32.
      </p>
  </div>

  <div class="section">
      <h2>Descripción General</h2>
      <p>
          Este sistema embebido permite controlar una grúa robótica de forma intuitiva mediante entradas analógicas.
          El usuario manipula la posición de los brazos usando potenciómetros, mientras que el sistema procesa las señales
          y controla servomotores en tiempo real.
      </p>
      <ul>
          <li>Control manual en tiempo real</li>
          <li>Modo automático de retorno</li>
          <li>Secuencia automática predefinida</li>
          <li>Interrupciones con antirrebote</li>
      </ul>
  </div>

  <div class="section">
      <h2>Arquitectura del Sistema</h2>
      <h3>Entradas</h3>
      <ul>
          <li>3 Potenciómetros (base, brazo, gancho)</li>
          <li>2 Pulsadores (reset y modo automático)</li>
      </ul>

  <h3>Procesamiento</h3>
      <ul>
          <li>ESP32</li>
          <li>ADC:
              <ul>
                  <li>Pot1 → 12 bits</li>
                  <li>Pot2 → 10 bits</li>
                  <li>Pot3 → 12 bits</li>
              </ul>
          </li>
          <li>Conversión ADC → PWM</li>
          <li>Interrupciones externas</li>
          <li>Máquina de estados</li>
      </ul>

  <h3>Salidas</h3>
      <ul>
          <li>3 Servomotores</li>
          <li>LED verde (modo manual)</li>
          <li>LED rojo (modo automático)</li>
          <li>Buzzer</li>
      </ul>
  </div>

  <div class="section">
      <h2>Funcionamiento</h2>
      <h3>Modo Manual</h3>
      <ul>
           <li>Lectura de potenciómetros</li>
           <li>Conversión a ángulos (0°–180°)</li>
           <li>Control en tiempo real</li>
           <li>LED verde activo</li>
      </ul>

  <h3>Modo Automático: Retorno</h3>
      <ul>
          <li>Desactiva control manual</li>
          <li>Retorno suave a 0°</li>
          <li>LED rojo + buzzer</li>
          <li>Regresa a modo manual</li>
      </ul>

  <h3>Modo Automático: Secuencia</h3>
      <ul>
          <li>Movimiento tipo “ola”</li>
          <li>Señalización con LED y buzzer</li>
          <li>Retorno automático al finalizar</li>
      </ul>
  </div>

  <div class="section">
      <h2>Características Técnicas</h2>
      <ul>
          <li>ADC para lectura analógica</li>
          <li>PWM a 50 Hz para servos</li>
          <li>Interrupciones con antirrebote</li>
          <li>Promediado de señales</li>
          <li>Control por máquina de estados</li>
      </ul>
  </div>

<div class="section">
    <h2>Tecnologías</h2>
    <ul>
        <li>MicroPython</li>
        <li>ESP32</li>
        <li>PWM</li>
        <li>ADC</li>
    </ul>
</div>

<div class="section">
      <h2>Posibles Mejoras</h2>
        <ul>
          <li>Pantalla LCD/OLED</li>
          <li>Bluetooth o WiFi</li>
          <li>Integración IoT</li>
          <li>Automatización inteligente</li>
      </ul>
  </div>

  <div class="section">
        <h2>Notas importantes:</h2>
        <ul>
            <li>Se promedian lecturas ADC para mayor estabilidad</li>
            <li>Un servo está invertido por montaje mecánico</li>
            <li>Uso de interrupciones con control de rebote</li>
            <li>Estados: manual, reset, auto</li>
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
</body>
</html>
