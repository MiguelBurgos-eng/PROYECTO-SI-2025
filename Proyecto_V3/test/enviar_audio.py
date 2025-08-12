import serial
import soundfile as sf
import time
from gtts import gTTS
from pydub import AudioSegment

# NUEVO
import numpy as np  # para filtros/arrays

PUERTO = 'COM6'
BAUDRATE = 921600
ARCHIVO_WAV = "respuesta.wav"

def texto_a_wav(texto):
    tts = gTTS(texto, lang='es')
    tts.save("temp.mp3")

    audio = AudioSegment.from_mp3("temp.mp3")
    audio = audio.set_frame_rate(44100).set_channels(1).set_sample_width(2)
    audio = audio + 5  # Ajuste de volumen

    audio.export(ARCHIVO_WAV, format="wav")
    print("✅ WAV generado correctamente")

def enviar_audio_a_esp32():
    data, samplerate = sf.read(ARCHIVO_WAV, dtype='int16')
    if data.ndim > 1:
        data = data[:, 0]

    # ================== NUEVO: preprocesado anti-ruido ==================
    x = data.astype(np.float64, copy=False)

    # (A) Elimina DC (offset), ayuda a quitar "pops"/rumble residual
    x -= np.mean(x)

    # (B) (Opcional) Re-muestrear si tu ESP32 NO está a 44100 Hz
    TARGET_FS = 44100  # <-- si tu I2S está a 24000 p.ej., cámbialo aquí
    if samplerate != TARGET_FS:
        t_old = np.arange(x.shape[0]) / float(samplerate)
        n_new = int(round(x.shape[0] * TARGET_FS / float(samplerate)))
        t_new = np.arange(n_new) / float(TARGET_FS)
        x = np.interp(t_new, t_old, x)
        samplerate = TARGET_FS

    # (C) High-pass 2º orden (Butterworth aprox) ~150 Hz (ajusta FC_HZ)
    FC_HZ = 150.0
    Q_HP = 0.707  # ≈ Butterworth
    w0 = 2.0 * np.pi * FC_HZ / float(samplerate)
    cosw0, sinw0 = np.cos(w0), np.sin(w0)
    alpha = sinw0 / (2.0 * Q_HP)
    b0 =  (1.0 + cosw0) / 2.0
    b1 = -(1.0 + cosw0)
    b2 =  (1.0 + cosw0) / 2.0
    a0 =  1.0 + alpha
    a1 = -2.0 * cosw0
    a2 =  1.0 - alpha
    # normaliza
    b0, b1, b2, a1, a2 = b0/a0, b1/a0, b2/a0, a1/a0, a2/a0

    # biquad (implementado localmente para no añadir librerías)
    y = np.empty_like(x, dtype=np.float64)
    x1 = x2 = y1 = y2 = 0.0
    for n in range(x.shape[0]):
        y0 = b0*x[n] + b1*x1 + b2*x2 - a1*y1 - a2*y2
        y[n] = y0
        x2, x1 = x1, x[n]
        y2, y1 = y1, y0

    x = y

    # (D) Notch a 60 Hz (Q alto) por si cuela zumbido de red
    F_NOTCH = 60.0     # cambia a 50.0 si estás en 50 Hz
    Q_NOTCH = 25.0
    w0 = 2.0 * np.pi * F_NOTCH / float(samplerate)
    cosw0, sinw0 = np.cos(w0), np.sin(w0)
    alpha = sinw0 / (2.0 * Q_NOTCH)
    b0 = 1.0
    b1 = -2.0 * cosw0
    b2 = 1.0
    a0 = 1.0 + alpha
    a1 = -2.0 * cosw0
    a2 = 1.0 - alpha
    b0, b1, b2, a1, a2 = b0/a0, b1/a0, b2/a0, a1/a0, a2/a0

    y = np.empty_like(x, dtype=np.float64)
    x1 = x2 = y1 = y2 = 0.0
    for n in range(x.shape[0]):
        y0 = b0*x[n] + b1*x1 + b2*x2 - a1*y1 - a2*y2
        y[n] = y0
        x2, x1 = x1, x[n]
        y2, y1 = y1, y0

    x = y

    # (E) Fade-in/out corto para eliminar clicks de inicio/fin
    FADE = min(256, x.shape[0]//20)  # ~6 ms a 44.1 kHz
    if FADE > 4:
        x[:FADE] *= np.linspace(0.0, 1.0, FADE, endpoint=True)
        x[-FADE:] *= np.linspace(1.0, 0.0, FADE, endpoint=True)

    # (F) Limitar y convertir a int16 (little-endian forzado)
    x = np.clip(x, -32768.0, 32767.0)
    data = x.astype('<i2')  # '<i2' = int16 little-endian
    # ================== /NUEVO ==========================================

    with serial.Serial(PUERTO, BAUDRATE, timeout=1) as ser:
        print("📦 Enviando audio...")
        time.sleep(2)

        ser.write(b'__START__\n')
        time.sleep(0.1)

        for i in range(0, len(data), 256):
            bloque = data[i:i+256].tobytes()
            ser.write(bloque)
            # time.sleep(0.0001)

        ser.write(b'__END__\n')
        print("✅ Envío completado")

# Ejecuta prueba
texto = "Hola Miguel, esta es una prueba con el ESP32 lalalalallalalalalalallaallalalalalalalalalalalalñalalalalalalalalalalala 12345678910 112 12323131223 que rico papi."
texto_a_wav(texto)
enviar_audio_a_esp32()
