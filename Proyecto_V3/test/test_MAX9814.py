import serial
import numpy as np
import matplotlib.pyplot as plt

PUERTO = 'COM6'       # Cambia si no es COM6
BAUDRATE = 115200
N_MUESTRAS = 8000     # Igual al sketch

def grabar_audio():
    puerto = serial.Serial(PUERTO, BAUDRATE, timeout=1)
    puerto.write(b'G')  # Iniciar grabación
    datos = []

    print("🎙 Escuchando...")

    while len(datos) < N_MUESTRAS:
        byte = puerto.read(1)
        if byte:
            datos.append(ord(byte))

    puerto.close()
    return np.array(datos)

# Prueba de visualización
audio = grabar_audio()
plt.plot(audio)
plt.title("Audio capturado del MAX9814")
plt.xlabel("Muestra")
plt.ylabel("Nivel")
plt.show()
