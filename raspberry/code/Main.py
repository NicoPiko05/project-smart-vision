import bluetooth
import pyaudio
from raspberry.code.connection import show_on_display
import numpy as np

# Audio Configuration
RATE = 16000  # 16kHz sample rate
CHANNELS = 1  # Mono audio (one mic)
FORMAT = pyaudio.paInt16  # 16-bit PCM
CHUNK_SIZE = 1024  # 1024 samples per frame

# PyAudio stream Setup
audio = pyaudio.PyAudio()
stream = audio.open(format=FORMAT, channels=CHANNELS, rate=RATE, input=True, frames_per_buffer=CHUNK_SIZE)

# Bluetooth Setup
server_sock = bluetooth.BluetoothSocket(bluetooth.RFCOMM)
server_sock.bind(("", bluetooth.PORT_ANY))
server_sock.listen(1)

port = server_sock.getsockname()[1]
bluetooth.advertise_service(server_sock, "AudioStream",
                            service_classes=[bluetooth.SERIAL_PORT_CLASS],
                            profiles=[bluetooth.SERIAL_PORT_PROFILE])

print(f"Waiting for connection on RFCOMM channel {port}...")

client_sock, client_info = server_sock.accept()
print(f"Connected to {client_info}")

try:
    while True:
        data = stream.read(CHUNK_SIZE, exception_on_overflow=False)  # Read PCM audio
        client_sock.sendall(data)  # Send raw PCM data
        response = client_sock.recv(1024).decode("utf-8")  # Receive recognized text
        if response:
            show_on_display(response)

except KeyboardInterrupt:
    print("\n Stopping...")

finally:
    stream.stop_stream()
    stream.close()
    audio.terminate()
    client_sock.close()
    server_sock.close()