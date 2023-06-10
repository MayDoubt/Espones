import keyboard
import sounddevice as sd
from scipy.io.wavfile import write
import requests
import json
import numpy

import whisper

##### Constantes usadas a lo largo del programa #####

    # Configuración del servicio de reconocimiento de voz de OpenAI
#openai.api_key = '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'
OPENAI_API_URL = 'https://api.openai.com/v1/engines/davinci/v1/assistant/completions'

    # Configuración de la captura de audio
SAMPLE_RATE = 16000
DURATION = 5

    # Speakers a usar 
    # 13 para hombre voz profunda
    # 14 para la mujer
    # 2 mujer por defecto
    # 22 susurro
SPEAKER = 13

##### Inicio del programa #####

def inicio_proceso():

    print("Se ha iniciado el programa de traducción.\n")

    audio = capturar_audio()
    texto = transcribir_audio(audio)


def capturar_audio():
    print("Capturando audio...\n")

    # Capturar el audio desde el micrófono
    audio = sd.rec(int(DURATION * SAMPLE_RATE), samplerate=SAMPLE_RATE, channels=1)
    sd.wait()

    print("Audio capturado.\n")
    write('output.wav', SAMPLE_RATE, audio)
    return audio.flatten()

def transcribir_audio(audio):
    print("Enviando audio para transcripción...\n")

    # Convertir el audio a texto usando le librería whisper
    model = whisper.load_model('base')
    transcripcion = model.transcribe(audio, fp16 = False)

    print("""{:^15}Audio recibido y transcrito
    {}
    """.format('', transcripcion['text']))

    return transcripcion['text']

def main():
    # Método que marca el inicio para que se ejecute la traducción
    keyboard.add_hotkey('º', inicio_proceso)

    # Mantiene el programa en ejecución hasta que se pulse la combinación de teclas
    keyboard.wait('ctrl+º')

    print("Cierre del programa al pulsar control + º, gracias por usar Espones.")

if __name__ == '__main__':
    main()