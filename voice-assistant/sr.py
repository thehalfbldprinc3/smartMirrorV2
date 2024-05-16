import sys
import os
import wave
import pyaudio
from vosk import Model, KaldiRecognizer

model=Model("./vosk-small")
recognizer=KaldiRecognizer(model, 16000)

audio=pyaudio.PyAudio()

stream = audio.open(format=pyaudio.paInt16,
                    channels=1,
                    rate=16000,
                    input=True,
                    frames_per_buffer=4000)

print("Listing...")


def get_audio():
    while True:
        data = stream.read(1000)
        if len(data) == 0:
            continue
        if recognizer.AcceptWaveform(data):
            result = recognizer.Result()
            return result


if __name__ == "__main__":
        get_audio()
        stream.stop_stream()
        stream.close()
        audio.terminate()
