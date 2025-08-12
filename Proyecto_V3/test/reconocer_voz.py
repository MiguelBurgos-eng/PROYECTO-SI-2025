import speech_recognition as sr

def reconocer_audio(nombre_archivo="grabacion.wav"):
    recognizer = sr.Recognizer()
    with sr.AudioFile(nombre_archivo) as fuente:
        audio = recognizer.record(fuente)  # Lee todo el archivo
    try:
        texto = recognizer.recognize_google(audio, language="es-MX")
        print(f"🗣 Texto reconocido: {texto}")
        return texto
    except sr.UnknownValueError:
        print("❌ No se entendió el audio.")
    except sr.RequestError as e:
        print(f"❌ Error de conexión con el servicio: {e}")

# Ejecutar
reconocer_audio("grabacion_16bit.wav")  # Cambia el nombre si es necesario
