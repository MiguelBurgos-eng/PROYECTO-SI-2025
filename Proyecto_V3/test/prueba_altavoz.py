import serial
import numpy as np
import time

PUERTO = 'COM6'
BAUDRATE = 115200
DURACION = 2  # segundos
FS = 24000  # Frecuencia de muestreo
FREQ = 440  # Frecuencia del tono (La)

# Generar tono seno 16 bits
t = np.linspace(0, DURACION, int(FS * DURACION), endpoint=False)
audio = 0.5 * np.sin(2 * np.pi * FREQ * t)
samples = (audio * 32767).astype(np.int16)

with serial.Serial(PUERTO, BAUDRATE, timeout=1) as ser:
    time.sleep(2)
    ser.write(b'START\n')
    time.sleep(0.1)
    
    print(f"🎵 Enviando tono de {FREQ}Hz...")
    for i in range(0, len(samples), 512):
        bloque = samples[i:i+512].tobytes()
        ser.write(bloque)
        time.sleep(0.01)

    time.sleep(0.1)
    ser.write(b'END\n')
    print("✅ Listo.")
