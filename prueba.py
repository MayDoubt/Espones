import requests
from scipy.io.wavfile import write
import pygame._sdl2.audio as sdl2_audio
import pyaudio
from pygame import mixer #Playing sound
import time

def main():
    # URL de la API REST encargada de la sintetización del texto contenida en Docker
    api_url = 'http://127.0.0.1:50021/'

    # Endpoints para el sintetizado, el primero genera el JSON,
    # el segundo transforma el JSON en un archivo .wav
    endpoint_json = '{}audio_query?text={}&speaker={}'.format(api_url, 'こんにちは', 2)
    endpoint_audio_japones = '{}synthesis?speaker={}'.format(api_url, 2)

    # Lanzamiento de querys
    response_json = requests.post(endpoint_json)
    response_audio_japones = requests.post(endpoint_audio_japones, json = response_json.json())
    
    # Guardado de audio generado
    with open("output_japones.wav", "wb") as vid:
        video_stream = response_audio_japones.content
        vid.write(video_stream)

    p = pyaudio.PyAudio()
    info = p.get_host_api_info_by_index(0)
    numdevices = info.get('deviceCount')
    for i in range(0, numdevices):
        if (p.get_device_info_by_host_api_device_index(0, i).get('maxInputChannels')) > 0:
            print('Micrófono', i, " - ", p.get_device_info_by_host_api_device_index(0, i)['name'])
    
    mixer.init() # Initialize the mixer, this will allow the next command to work
    print(sdl2_audio.get_audio_device_names(False)) # Returns playback devices, Boolean value determines whether they are Input or Output devices.
    mixer.quit() # Quit the mixer as it's initialized on your main playback device

    mixer.init(devicename = 'CABLE Input (VB-Audio Virtual Cable)') # Initialize it with the correct device
    mixer.music.load("output_japones.wav") # Load the mp3
    mixer.music.play() # Play it

    while mixer.music.get_busy():  # wait for music to finish playing
        time.sleep(1)

if __name__ == '__main__':
    main()