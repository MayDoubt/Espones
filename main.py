import keyboard
import sounddevice as sd
from scipy.io.wavfile import write
#import json
#import numpy

import openai
import whisper
import requests

##### Constantes usadas a lo largo del programa #####

    # Configuración del servicio de reconocimiento de voz de OpenAI
OPENAI_API_KEY = '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'
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
    texto_ingles = transcribir_audio_y_traducir_ingles(audio)
    texto_japones = traduccion_japones(texto_ingles)
    sintetizado_texto_japones(texto_japones)


def capturar_audio():
    print("Capturando audio...\n")

    # Capturar el audio desde el micrófono
    audio = sd.rec(int(DURATION * SAMPLE_RATE), samplerate=SAMPLE_RATE, channels=1)
    sd.wait()

    print("Audio capturado.\n")
    write('output.wav', SAMPLE_RATE, audio)
    return audio.flatten()

def transcribir_audio_y_traducir_ingles(audio):
    print("Enviando audio para transcripción y traducción a inglés...\n")

    # Convertir el audio a texto usando le librería whisper
    model = whisper.load_model('base')
    transcripcion = model.transcribe(audio, fp16 = False)

    # Traducción asíncrona a inglés usando el archivo generado de audio
    media_file_path = 'output.wav'
    media_file = open(media_file_path, 'rb')

    # Al apartado prompt se le pone una descripción para hacer una traducción más acotada
    # Puede ser usado para darle más contexto y sentido a la traducción
    ingles = openai.Audio.translate(
        api_key=OPENAI_API_KEY,
        model='whisper-1',
        file=media_file,
        prompt='Some phrases in spanish'
    )

    # Control en consola para revisión de texto transcrito y traducido con format
    print("""{:^15}Audio recibido y transcrito
    {}
    """.format('', transcripcion['text']))

    print("""
    {:^15}Traducción realizada a inglés
    {}
    """.format('', ingles['text']))

    return ingles['text']

def traduccion_japones(texto):

    # Generación y salvado de la Key
    #openai.api_key = os.getenv(OPENAI_API_KEY)

    # Preparación de la request a la API
    response = openai.Completion.create(
        api_key = OPENAI_API_KEY,
        model="text-davinci-003",
        prompt="Translate this into Japanese: " + texto,
        temperature=0.3,
        max_tokens=100,
        top_p=1.0,
        frequency_penalty=0.0,
        presence_penalty=0.0
    )

    texto_en_japones = response['choices'][0]['text'][2:]

    # Mostrado por consola de traducción para comprobación de traducción
    print("""{:^15}Texto en inglés recibido y traducido
    {}
    """.format('', texto_en_japones))

    return texto_en_japones

def sintetizado_texto_japones(texto):
    
    # URL de la API REST encargada de la sintetización del texto contenida en Docker
    api_url = 'http://127.0.0.1:50021/'

    # Endpoints para el sintetizado, el primero genera el JSON,
    # el segundo transforma el JSON en un archivo .wav
    endpoint_json = '{}audio_query?text={}&speaker={}'.format(api_url, texto, SPEAKER)
    endpoint_audio_japones = '{}synthesis?speaker={}'.format(api_url, SPEAKER)

    # Lanzamiento de querys
    response_json = requests.post(endpoint_json)
    response_audio_japones = requests.post(endpoint_audio_japones, json = response_json.json())
    
    # Guardado de audio generado en la respuesta
    with open("output_japones.wav", "wb") as vid:
        video_stream = response_audio_japones.content
        vid.write(video_stream)

def main():
    # Evento para que se ejecute el proceso
    keyboard.add_hotkey('º', inicio_proceso)

    # Mantiene el programa en ejecución hasta que se pulse la combinación de teclas
    keyboard.wait('ctrl+º')

    print("Cierre del programa al pulsar control + º, gracias por usar Espones.")

if __name__ == '__main__':
    main()