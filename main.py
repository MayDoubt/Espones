import keyboard
import sounddevice as sd
from scipy.io.wavfile import write
import requests
import json
import numpy

# Estas son las constantes que vamos a usar a lo largo del programa #

    # Configuración del servicio de reconocimiento de voz de OpenAI
OPENAI_API_KEY = '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'
OPENAI_API_URL = 'https://api.openai.com/v1/engines/davinci/v1/assistant/completions'

    # Configuración de la captura de audio
SAMPLE_RATE = 16000
DURATION = 5

# Inicio del programa #

def inicio_proceso():

    print("Se ha iniciado el programa de traducción.")

    audio = capturar_audio()
    transcriptions = transcribe_audio(audio)

    if transcriptions:
        print("Transcripciones:")
        for transcription in transcriptions:
            print(transcription)

def capturar_audio():
    print("Capturando audio...")

    # Capturar el audio desde el micrófono
    audio = sd.rec(int(DURATION * SAMPLE_RATE), samplerate=SAMPLE_RATE, channels=1)
    sd.wait()

    print("Audio capturado.")
    write('/grabacion/output.wav', SAMPLE_RATE, audio)
    return audio.flatten()

def transcribe_audio(audio):
    print("Enviando audio para transcripción...")

    # Convertir el audio a formato de 16 bits y little-endian
    audio_bytes = audio.astype('int16').tobytes()

    # Realizar la solicitud al servicio de reconocimiento de voz de OpenAI
    headers = {
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {OPENAI_API_KEY}'
    }
    data = {
        'prompt': '',
        'max_tokens': 100,
        'temperature': 0.6,
        'n': 1,
        'stop': None,
        'logprobs': None,
        'echo': False,
        'stream': None,
        'mode': 'message',
        'messages': [
            {'role': 'system', 'content': 'You are a helpful assistant.'},
            {'role': 'user', 'content': 'Transcribe the following audio:'}
        ],
        'model': 'davinci',
        'assistantId': None
    }
    response = requests.post(OPENAI_API_URL, headers=headers, data=json.dumps(data))
    response_data = response.json()

    if 'choices' in response_data:
        transcriptions = [choice['message']['content'] for choice in response_data['choices']]
        return transcriptions
    else:
        print("No se pudo transcribir el audio.")
        return None

def main():
    # Método que marca el inicio para que se ejecute la traducción
    keyboard.add_hotkey('º', inicio_proceso)

    # Mantener el programa en ejecución
    keyboard.wait('ctrl+esc')

    print("Cierre del programa al pulsar control + º, gracias por usar Espones.")

if __name__ == '__main__':
    main()