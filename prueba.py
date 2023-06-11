import requests
from scipy.io.wavfile import write
import simpleaudio

def main():
    # URL de la API REST encargada de la sintetización del texto contenida en Docker
    api_url = 'http://127.0.0.1:50021/'

    # Endpoints para el sintetizado, el primero genera el JSON,
    # el segundo transforma el JSON en un archivo .wav
    endpoint_json = '{}audio_query?text={}&speaker={}'.format(api_url, 'こんにちは、私はジョナサンです、お会いできて嬉しいです。', 13)
    endpoint_audio_japones = '{}synthesis?speaker={}'.format(api_url, 13)

    # Lanzamiento de querys
    response_json = requests.post(endpoint_json)
    response_audio_japones = requests.post(endpoint_audio_japones, json = response_json.json())
    
    # Guardado de audio generado
    write('output_japones.wav', 16000, response_audio_japones.content)

if __name__ == '__main__':
    main()