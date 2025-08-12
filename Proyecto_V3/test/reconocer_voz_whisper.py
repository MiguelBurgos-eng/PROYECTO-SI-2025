import whisper

def transcribir_whisper(nombre_archivo="grabacion_16bit.wav"):
    model = whisper.load_model("base")  # También puedes probar "tiny"
    resultado = model.transcribe(nombre_archivo, language="es")
    print("🗣 Texto reconocido (whisper):", resultado["text"])
    return resultado["text"]

transcribir_whisper()
