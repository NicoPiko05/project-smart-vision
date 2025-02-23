from vosk import Model, KaldiRecognizer
import wave
import json

model = Model("vosk-model-small-cs-0.4-rhasspy")# Load Czech model
rec = KaldiRecognizer(model, 16000)

wf = wave.open("../raspberry/code/output.wav", "rb")
while True:
    data = wf.readframes(4000)
    if len(data) == 0:
        break
    if rec.AcceptWaveform(data):
        print(rec.Result())

