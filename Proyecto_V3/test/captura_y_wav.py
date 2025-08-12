import serial
import numpy as np
import wave
import time

PUERTO = 'COM6'          # Asegúrate de que es el correcto
BAUDRATE = 115200
N_MUESTRAS = 8000        # 1 segundo a 8kHz
FS = 5200    # Frecuencia de muestreo

def grabar_audio():
    with serial.Serial(PUERTO, BAUDRATE, timeout=1) as puerto:
        puerto.write(b'G')  # Iniciar captura en el ESP32
        datos = []
        print("🎙 Grabando...")

        while len(datos) < N_MUESTRAS:
            byte = puerto.read(1)
            if byte:
                datos.append(ord(byte))

        print("✅ Audio recibido.")
        return np.array(datos, dtype=np.uint8)

def guardar_wav(datos, nombre_archivo="grabacion.wav"):
    with wave.open(nombre_archivo, 'wb') as archivo:
        archivo.setnchannels(1)            # Mono
        archivo.setsampwidth(1)            # 8 bits (1 byte)
        archivo.setframerate(FS)           # 8000 Hz
        archivo.writeframes(datos.tobytes())
    print(f"🎧 Archivo guardado como: {nombre_archivo}")

# Proceso completo
audio = grabar_audio()
guardar_wav(audio)
