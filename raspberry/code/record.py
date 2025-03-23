import pyaudio
import wave
import queue
import json
import connection
from vosk import Model, KaldiRecognizer

from raspberry.code.connection import show_on_display

FRAMES_PER_BUFFER = 8192 #no idea what this all means
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 16000


#loads the recognizer model
model = Model("../../Phone/vosk-model-small-cs-0.4-rhasspy")
rec = KaldiRecognizer(model, 16000)

p = pyaudio.PyAudio()

stream = p.open(
    format=FORMAT,
    channels=CHANNELS,
    rate=RATE,
    input=True,
    frames_per_buffer=FRAMES_PER_BUFFER
)
print("Recording...")
stream.start_stream()

#speech to text
while True:
    data = stream.read(4096)

    if rec.AcceptWaveform(data):
        data = rec.Result()[14:-3]
        show_on_display(data)
        print(data)
        if (data) == "konec":
            break

print("Recording finished")
stream.stop_stream()
stream.close()