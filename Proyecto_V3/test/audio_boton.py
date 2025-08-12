import serial
import numpy as np
import wave
import whisper
import sqlite3
import unicodedata
import re
import rapidfuzz
from rapidfuzz import fuzz,process
import time

PUERTO = 'COM8'  # Puerto para grabar audio
BAUDRATE = 115200
FS = 7500  # Frecuencia de muestreo del ESP32
N_MUESTRAS = int(FS*3)  # 3 segundos a 8000 Hz
ARCHIVO_WAV = "grabacion_16bit.wav"
DB_PATH = "base_Conocimiento.db"

def limpiar_texto(texto):
    texto = texto.lower().strip()
    texto = unicodedata.normalize('NFKD', texto).encode('ASCII', 'ignore').decode('utf-8')
    texto = re.sub(r'[^\w\s]', '', texto)
    return texto

def normalizar_audio(datos):
    datos = datos - np.mean(datos)  # Quitar DC
    max_valor = np.max(np.abs(datos))
    if max_valor > 0:
        datos = datos * (32767 / max_valor)
    return datos.astype(np.int16)

def leer_exactamente(ser, n):
    buf = bytearray()
    while len(buf) < n:
        chunk = ser.read(n - len(buf))
        if not chunk: break
        buf.extend(chunk)
    return bytes(buf)

def grabar_audio():
    exp = N_MUESTRAS*2
    tmo = max(2.0, (exp*10)/BAUDRATE * 1.5)  # 10 bits/byte en UART

    with serial.Serial(PUERTO, BAUDRATE, timeout=0.1) as s:
        # Limpieza inicial
        try: s.dtr=False; s.rts=False
        except: pass
        s.reset_input_buffer(); s.reset_output_buffer()
        time.sleep(0.5)

        # === NUEVO: esperar a que el ESP32 avise botón ('G') ===
        print("⌛ Esperando botón del ESP32... (enviará 'G')")
        while True:
            if s.in_waiting:
                ch = s.read(1)
                if ch == b'G':
                    break
            # si llega basura (texto de arranque), se ignora

        # Ahora sí, conservamos tu protocolo: respondemos con 'G' para iniciar
        s.timeout = tmo
        s.write(b'G')
        print("🎙 Grabando audio...")

        bruto = leer_exactamente(s, exp)

    print(f"Recibidos {len(bruto)}/{exp} bytes")
    if len(bruto) < 2:
        return np.array([], dtype=np.int16)

    u16 = np.frombuffer(bruto, dtype='<u2')      # uint16 LE
    x = u16.astype(np.int32) - 2048             # centrar (ADC ~12 bits en 0..4095)
    x = np.clip(x*16, -32768, 32767).astype(np.int16)  # ganancia segura
    return x

def guardar_wav(datos):
    with wave.open(ARCHIVO_WAV, 'wb') as archivo:
        archivo.setnchannels(1)
        archivo.setsampwidth(2)
        archivo.setframerate(FS)
        archivo.writeframes(datos.tobytes())
    print(f"🎧 Audio guardado como: {ARCHIVO_WAV}")

def transcribir_audio():
    model = whisper.load_model("small")
    resultado = model.transcribe(ARCHIVO_WAV, language="es")
    texto = resultado["text"].strip().lower()
    print("🗣 Texto reconocido:", texto)
    return texto

def buscar_respuesta_fuzzy(texto_usuario):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("SELECT pregunta, respuesta FROM conocimiento")
    pares = c.fetchall()
    conn.close()

    texto_usuario = limpiar_texto(texto_usuario)
    preguntas = [limpiar_texto(p[0]) for p in pares]

    mejor_match, score, idx = process.extractOne(texto_usuario, preguntas, scorer=fuzz.ratio)

    if score > 65:
        print(f"✅ Pregunta más cercana: {pares[idx][0]} ({score}%)")
        print(f"💬 Respuesta: {pares[idx][1]}")
        return pares[idx][1]
    else:
        print("❌ No se encontró una respuesta cercana.")
        return "No encontré una respuesta para eso."

# Flujo completo (arranca cuando presiones el botón en el ESP32)
audio = grabar_audio()
audio = normalizar_audio(audio)
guardar_wav(audio)
texto_raw = transcribir_audio()
texto = limpiar_texto(texto_raw)
respuesta = buscar_respuesta_fuzzy(texto)
