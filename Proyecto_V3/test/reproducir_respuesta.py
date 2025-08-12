import serial
import soundfile as sf
import time
from gtts import gTTS
from pydub import AudioSegment

PUERTO = 'COM6'
BAUDRATE = 921600
ARCHIVO_WAV = "respuesta.wav"
TAMANIO_BLOQUE = 256  # 256 muestras ≈ 512 bytes

def texto_a_wav(texto):
    tts = gTTS(texto, lang='es')
    tts.save("temp.mp3")
    audio = AudioSegment.from_mp3("temp.mp3")
    audio = audio.set_frame_rate(24000).set_channels(1).set_sample_width(2)
    audio.export(ARCHIVO_WAV, format="wav")
    print("✅ WAV generado correctamente")

def enviar_audio_a_esp32():
    data, samplerate = sf.read(ARCHIVO_WAV, dtype='int16')
    if data.ndim > 1:
        data = data[:, 0]  # Convertir a mono si es estéreo

    print(f"📦 Enviando {len(data)} muestras...")
    with serial.Serial(PUERTO, BAUDRATE, timeout=1) as ser:
        time.sleep(2)
        ser.write(b'START\n')
        time.sleep(0.1)

        for i in range(0, len(data), TAMANIO_BLOQUE):
            bloque = data[i:i+TAMANIO_BLOQUE].tobytes()
            ser.write(bloque)
            time.sleep(0.03)  # Ajusta si aún se traba. Ideal: 0.01 – 0.03

        time.sleep(0.1)
        ser.write(b'END\n')
        print("✅ Envío finalizado")

# Prueba
texto_a_wav("Esta es una prueba de voz enviada al ESP32 para su reproducción.")
enviar_audio_a_esp32()
