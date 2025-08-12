# PROYECTO-SI-2025 
# Asistente de Voz ESP32 con Reconocimiento de Voz y Base de Conocimiento

Este proyecto implementa un asistente de voz interactivo utilizando un ESP32 para la captura y reproducción de audio, y Python en el lado del PC para el procesamiento de voz (ASR), la gestión de una base de conocimiento y la síntesis de voz (TTS).

## 🚀 Características Principales

*   **Captura de Audio por Botón:** El ESP32 detecta la pulsación de un botón para iniciar la grabación de audio.
*   **Comunicación Serial:** Transmisión eficiente de audio en tiempo real entre el ESP32 y el PC a través de UART.
*   **Reconocimiento de Voz (ASR):** Utiliza el modelo Whisper de OpenAI para transcribir el audio capturado a texto.
*   **Base de Conocimiento:** Almacena preguntas y respuestas en una base de datos SQLite, permitiendo búsquedas difusas (fuzzy search) para encontrar la respuesta más relevante.
*   **Síntesis de Voz (TTS):** Convierte la respuesta de texto en audio utilizando Google Text-to-Speech (gTTS).
*   **Reproducción de Audio:** El ESP32 reproduce la respuesta de audio sintetizada a través de I2S.
*   **Preprocesamiento de Audio:** Incluye filtros para mejorar la calidad del audio antes de la síntesis y reproducción.
*   **Comando de Parada:** El asistente puede ser detenido por el usuario mediante comandos de voz específicos.

## 🛠️ Componentes y Tecnologías

### Hardware
*   **ESP32:** Microcontrolador principal.
*   **MAX9814 (o similar):** Módulo de micrófono con amplificador para la captura de audio.
*   **Módulo I2S (DAC):** Para la reproducción de audio de alta calidad.
*   **Botón:** Para activar la grabación de audio.

### Software
*   **Arduino IDE / ESP-IDF:** Para programar el ESP32.
*   **Python 3.x:** Lenguaje de programación principal para el lado del PC.
*   **Librerías Python:**
    *   `pyserial`: Comunicación serial con el ESP32.
    *   `numpy`: Manipulación de datos de audio.
    *   `wave`: Manejo de archivos WAV.
    *   `openai-whisper`: Reconocimiento automático de voz (ASR).
    *   `sqlite3`: Gestión de la base de datos de conocimiento.
    *   `unicodedata`, `re`: Limpieza y normalización de texto.
    *   `rapidfuzz`: Búsqueda difusa (fuzzy search) en la base de conocimiento.
    *   `soundfile`: Lectura/escritura de archivos de audio.
    *   `gTTS`: Google Text-to-Speech para síntesis de voz.
    *   `pydub`: Manipulación de audio (requiere FFmpeg).
*   **FFmpeg:** Necesario para `pydub` para la conversión de formatos de audio.

## 📂 Estructura del Proyecto
Proyecto_V3/
├─ hardware/
│  ├─ audio_boton.ino
│  └─ reproductor_uart_i2s.ino.ino
├─ test/
│  ├─ audio_boton.py
│  ├─ captura_y_wav_16bit.py
│  ├─ captura_y_wav.py
│  ├─ enviar_audio.py
│  ├─ prueba_altavoz.py
│  ├─ prueba_enviar.py
│  ├─ pruebas.py
│  ├─ recolectar_audio.py
│  ├─ reconocer_voz_whisper.py
│  ├─ reconocer_voz.py
│  ├─ reproducir_respuesta.py
│  ├─ test_MAX9814.py
│  └─ test_serial.py
├─ base_Conocimiento.db
├─ base_conocimiento.py
├─ grabacion_16bit.wav
├─ main.py
├─ respuesta.wav
├─ temp_resp.mp3
├─ temp_tts.mp3
└─ temp.mp3



## ⚙️ Configuración y Uso

### 1. Configuración del ESP32

1.  **Instala el entorno de desarrollo de ESP32:** Sigue las instrucciones para instalar el soporte de ESP32 en Arduino IDE o ESP-IDF.
2.  **Carga `audio_boton.ino`:** Este sketch se encarga de la captura de audio desde el micrófono (MAX9814) y envía los datos al PC cuando se presiona el botón. Asegúrate de configurar `pinMicrofono` y `pinBoton` correctamente.
3.  **Carga `reproductor_uart_i2s.ino.ino`:** Este sketch recibe datos de audio desde el PC a través de UART y los reproduce usando I2S. Configura los pines I2S (`I2S_BCLK`, `I2S_LRC`, `I2S_DOUT`) según tu hardware.
    *   **Nota:** Necesitarás cargar ambos sketches en el ESP32, o combinarlos si tu aplicación lo requiere. El `main.py` asume que el ESP32 está configurado para enviar audio al presionar el botón y recibir audio para reproducir.

### 2. Configuración del PC (Python)

1.  **Clona el repositorio:**
    ```bash
    git clone https://github.com/MiguelBurgos-eng/PROYECTO-SI-2025.git
    cd PROYECTO-SI-2025
    ```
2.  **Crea un entorno virtual (recomendado):**
    ```bash
    python -m venv venv
    source venv/bin/activate  # En Linux/macOS
    venv\Scripts\activate     # En Windows
    ```
3.  **Instala las dependencias de Python:**
    ```bash
    pip install pyserial numpy soundfile gTTS pydub rapidfuzz openai-whisper
    ```
4.  **Instala FFmpeg:** `pydub` requiere FFmpeg para procesar archivos de audio. Descárgalo e instálalo, y asegúrate de que esté en tu PATH. Puedes encontrar instrucciones detalladas en la documentación de `pydub` o buscando "install ffmpeg [your_os]".
5.  **Configura los puertos seriales:**
    *   Abre `main.py` y ajusta `PORT_IN` y `PORT_OUT` a los puertos COM correctos de tu ESP32.
    *   `PORT_IN`: Puerto usado para la comunicación del ESP32 al PC (micrófono).
    *   `PORT_OUT`: Puerto usado para la comunicación del PC al ESP32 (altavoz).
    *   Asegúrate de que los `BAUDRATE` en los scripts Python (`BAUD_IN`, `BAUD_OUT`) coincidan con los configurados en los sketches de Arduino.

### 3. Base de Conocimiento

*   El archivo `base_Conocimiento.db` es la base de datos SQLite.
*   El script `base_conocimiento.py` se utiliza para crear la tabla `conocimiento` e insertar datos. Puedes modificarlo para añadir más preguntas y respuestas.
    *   **Para inicializar o modificar la base de datos:** Ejecuta `python MultipleFiles/base_conocimiento.py`. Descomenta las líneas relevantes para crear la tabla o insertar nuevos datos.

### 4. Ejecución del Asistente

1.  Asegúrate de que tu ESP32 esté conectado y los sketches cargados.
2.  Ejecuta el script principal de Python:
    ```bash
    python MultipleFiles/main.py
    ```
3.  El programa te indicará que presiones el botón en el ESP32. Una vez presionado, el ESP32 grabará tu voz, el PC la procesará, buscará una respuesta y la enviará de vuelta al ESP32 para su reproducción.
4.  Para detener el asistente, di una de las palabras de parada configuradas (ej. "detente", "basta", "terminar") cuando el asistente esté escuchando.

## 💡 Notas y Consideraciones

*   **Frecuencia de Muestreo (FS):** Asegúrate de que `FS_IN` en `main.py` coincida con la frecuencia de muestreo configurada en tu sketch de ESP32 para la captura de audio.
*   **Calibración del ADC:** El código Python incluye un centrado (`- 2048`) y escalado (`* 16`) para los datos del ADC del ESP32. Es posible que necesites ajustar estos valores para optimizar la calidad de audio según tu configuración específica del MAX9814 y el ADC del ESP32.
*   **Latencia:** La comunicación serial y el procesamiento pueden introducir cierta latencia. Para aplicaciones en tiempo real, se podrían explorar optimizaciones adicionales (ej. reducir el tamaño de los buffers, usar protocolos más rápidos).
*   **Modelos Whisper:** El script usa el modelo "small" de Whisper. Puedes probar con "tiny" para menor consumo de recursos o "base" para mayor precisión, aunque esto aumentará el tiempo de procesamiento y el tamaño del modelo.
*   **Preprocesamiento de Audio:** Los filtros de paso alto y notch en `enviar_audio.py` (y replicados en `main.py`) están diseñados para reducir ruido y zumbidos. Ajusta las frecuencias de corte (`FC_HZ`, `F_NOTCH`) si es necesario para tu entorno.

## 🤝 Contribuciones

Las contribuciones son bienvenidas. Si encuentras un error o tienes una mejora, no dudes en abrir un *issue* o enviar un *pull request*.

---
**Proyecto de Sistemas Inteligentes 2025**
*   **Miguel Burgos**
*   **Diego Castillo**
*   **Alan Fernandez**
*   **Universidad Tecnológica de México (UNITEC)**

