# -*- coding: utf-8 -*-
import os
import time
import wave
import serial
import sqlite3
import numpy as np
import unicodedata
import re

import whisper
from rapidfuzz import fuzz, process
import soundfile as sf
from gtts import gTTS
from pydub import AudioSegment

# ----------------- Configuración -----------------
# Serial IN (ESP32 -> PC, micrófono)
PORT_IN   = 'COM8'
BAUD_IN   = 115200
FS_IN     = 7500            # fs del ADC en el ESP32 (tu valor actual)
DUR_SEC   = 5.0
N_SAMPLES = int(FS_IN * DUR_SEC)
RAW_BYTES = N_SAMPLES * 2   # 16 bits (2 bytes por muestra)

# Serial OUT (PC -> ESP32, altavoz)
PORT_OUT  = 'COM6'
BAUD_OUT  = 921600
CHUNK_TX  = 512        # tamaño de bloque por envío

# Archivos
WAV_IN    = "grabacion_16bit.wav"
WAV_OUT   = "respuesta.wav"
DB_PATH   = "base_Conocimiento.db"

# ----------------- Utilidades -----------------
def limpiar_texto(texto: str) -> str:
    texto = texto.lower().strip()
    texto = unicodedata.normalize('NFKD', texto).encode('ASCII', 'ignore').decode('utf-8')
    texto = re.sub(r'[^\w\s]', '', texto)
    return texto

def normalizar_audio(datos: np.ndarray) -> np.ndarray:
    # quitar DC y escalar a int16 full scale
    datos = datos.astype(np.float32)
    datos = datos - np.mean(datos)
    max_val = np.max(np.abs(datos)) if datos.size else 0
    if max_val > 0:
        datos = datos * (32767.0 / max_val)
    return datos.astype(np.int16)

def leer_exactamente(ser: serial.Serial, n: int) -> bytes:
    buf = bytearray()
    while len(buf) < n:
        chunk = ser.read(n - len(buf))
        if not chunk:
            break
        buf.extend(chunk)
    return bytes(buf)

# ----------------- Grabación desde ESP32 -----------------
def grabar_audio_desde_esp32() -> np.ndarray:
    exp = RAW_BYTES
    # timeout aproximado: 10 bits/byte en UART + margen
    tmo = max(2.0, (exp * 10) / BAUD_IN * 1.5)

    with serial.Serial(PORT_IN, BAUD_IN, timeout=1) as s:
        try:
            s.dtr = False
            s.rts = False
        except:
            pass

        s.reset_input_buffer()
        s.reset_output_buffer()
        time.sleep(1.0)                    # estabiliza el puerto
        _ = s.read(s.in_waiting or 1)      # limpia basura inicial
        s.timeout = tmo

        # Orden para capturar 3 s en el ESP32
        s.write(b'G')
        print("🎙 Grabando audio...")
        bruto = leer_exactamente(s, exp)

    print(f"Recibidos {len(bruto)}/{exp} bytes")
    if len(bruto) < 2:
        return np.array([], dtype=np.int16)

    # El ESP32 suele mandar ADC en 12 bits dentro de 16 LE (0..4095).
    # Centramos y escalamos a int16 de forma segura.
    u16 = np.frombuffer(bruto, dtype='<u2')
    x = u16.astype(np.int32) - 2048          # centra (suponiendo 0..4095)
    x = np.clip(x * 16, -32768, 32767)       # expande a rango 16-bit
    return x.astype(np.int16)

def guardar_wav_int16(datos: np.ndarray, fs: int, path: str):
    with wave.open(path, 'wb') as f:
        f.setnchannels(1)
        f.setsampwidth(2)
        f.setframerate(fs)
        f.writeframes(datos.tobytes())
    print(f"🎧 Audio guardado: {path} @ {fs} Hz")

# ----------------- ASR (Whisper) -----------------
_whisper_model = None
def transcribir_wav(path: str, lang="es") -> str:
    global _whisper_model
    if _whisper_model is None:
        print("⬇️ Cargando modelo Whisper 'small' (una sola vez)...")
        _whisper_model = whisper.load_model("small")
    res = _whisper_model.transcribe(path, language=lang)
    texto = res.get("text", "").strip()
    print("🗣 Texto reconocido:", texto)
    return texto

# ----------------- Búsqueda en SQLite -----------------
def buscar_respuesta_fuzzy(texto_usuario: str, umbral: int = 65) -> str:
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("SELECT pregunta, respuesta FROM conocimiento")
    pares = c.fetchall()
    conn.close()

    if not pares:
        print("⚠️ La tabla 'conocimiento' está vacía.")
        return "No encontré una respuesta para eso."

    texto_usuario_limpio = limpiar_texto(texto_usuario)
    preguntas_limpias = [limpiar_texto(p) for p, _ in pares]

    match, score, idx = process.extractOne(texto_usuario_limpio, preguntas_limpias, scorer=fuzz.ratio)
    if idx is None:
        print("❌ No se encontró coincidencia.")
        return "No encontré una respuesta para eso."

    if score >= umbral:
        print(f"✅ Pregunta más cercana: {pares[idx][0]} ({score}%)")
        print(f"💬 Respuesta: {pares[idx][1]}")
        return pares[idx][1]
    else:
        print(f"❌ Coincidencia insuficiente ({score}%).")
        return "No encontré una respuesta para eso."

# ----------------- TTS → WAV -----------------
def texto_a_wav(texto: str, out_path: str = WAV_OUT):
    tts = gTTS(texto if texto else "No encontré una respuesta para eso.", lang='es')
    tts.save("temp_tts.mp3")
    # Normalizamos a mono, 44.1 kHz, 16-bit PCM
    audio = AudioSegment.from_mp3("temp_tts.mp3")
    audio = audio.set_frame_rate(44100).set_channels(1).set_sample_width(2)
    audio = audio + 10  # leve boost
    audio.export(out_path, format="wav")
    print(f"✅ WAV de respuesta generado: {out_path}")

# ----------------- Envío WAV al ESP32 -----------------
def enviar_wav_a_esp32(path: str):
    data, samplerate = sf.read(path, dtype='int16')
    if data.ndim > 1:
        data = data[:, 0]  # mono

    print(f"📦 Enviando audio ({len(data)} muestras @ {samplerate} Hz) a {PORT_OUT}...")
    with serial.Serial(PORT_OUT, BAUD_OUT, timeout=1) as ser:
        time.sleep(2.0)  # margen para establecer puerto
        ser.reset_input_buffer()
        ser.reset_output_buffer()

        # Marcadores de inicio/fin que tu firmware debe reconocer
        ser.write(b'__START__\n')
        time.sleep(0.05)

        # Enviar en bloques
        total = len(data)
        sent = 0
        view = memoryview(data)
        for i in range(0, total, CHUNK_TX):
            bloque = view[i:i+CHUNK_TX].tobytes()
            ser.write(bloque)
            sent += len(bloque) // 2  # muestras
            # Descomenta si tu receptor se atraganta:
            # time.sleep(0.0001)

        ser.write(b'__END__\n')
        print(f"✅ Envío completado ({sent} muestras).")

# ----------------- Pipeline completo -----------------
def main():
    # 1) Grabar desde ESP32
    audio = grabar_audio_desde_esp32()
    if audio.size == 0:
        print("❌ No se recibió audio. Revisa el puerto/baudios o el comando 'G' en el ESP32.")
        return

    # 2) Normalizar + guardar
    audio = normalizar_audio(audio)
    guardar_wav_int16(audio, FS_IN, WAV_IN)

    # 3) Transcribir
    texto_raw = transcribir_wav(WAV_IN, lang="es")
    texto = limpiar_texto(texto_raw)

    # 4) Buscar respuesta en la base
    respuesta = buscar_respuesta_fuzzy(texto)

    # 5) TTS → WAV
    texto_a_wav(respuesta, WAV_OUT)

    # 6) Enviar WAV al ESP32 (altavoz)
    enviar_wav_a_esp32(WAV_OUT)

if __name__ == "__main__":
    # Dependencias: pip install openai-whisper rapidfuzz soundfile gTTS pydub
    # y tener ffmpeg instalado para pydub.
    main()


