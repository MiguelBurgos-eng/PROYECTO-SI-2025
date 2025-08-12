import serial
import numpy as np
import wave

PUERTO = 'COM6'
BAUDRATE = 115200
N_MUESTRAS = 8000
FS = 4000

def grabar_audio():
    with serial.Serial(PUERTO, BAUDRATE, timeout=1) as puerto:
        puerto.write(b'G')
        datos = []
        print("🎙 Grabando...")

        while len(datos) < N_MUESTRAS:
            # Leer 2 bytes (LSB y MSB)
            lsb = puerto.read(1)
            msb = puerto.read(1)
            if lsb and msb:
                muestra = int.from_bytes(lsb + msb, byteorder='little')
                muestra_16bit = np.int16((muestra - 2048) << 4)  # Centrado
                datos.append(muestra_16bit)

        print("✅ Audio recibido.")
        return np.array(datos, dtype=np.int16)

def guardar_wav(datos, nombre="grabacion_16bit.wav"):
    with wave.open(nombre, 'wb') as archivo:
        archivo.setnchannels(1)
        archivo.setsampwidth(2)  # 16 bits = 2 bytes
        archivo.setframerate(FS)
        archivo.writeframes(datos.tobytes())
    print(f"🎧 Archivo guardado como: {nombre}")

audio = grabar_audio()
guardar_wav(audio)
