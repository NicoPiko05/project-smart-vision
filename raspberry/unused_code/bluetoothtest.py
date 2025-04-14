#!/usr/bin/env python3
"""PyBluez simple example rfcomm-server.py

Simple demonstration of a server application that uses RFCOMM sockets.

Author: Albert Huang <albert@csail.mit.edu>
$Id: rfcomm-server.py 518 2007-08-10 07:20:07Z albert $
"""

import bluetooth
import pyaudio
import struct

# Audio constants:
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 16000  # Use 16kHz for speech recognition
CHUNK = 1024  # Number of frames per chunk

# Packet constants (markers) (header and footer)
HEADER = b'\xAA\xBB'
FOOTER = b'\xCC\xDD'


server_sock = bluetooth.BluetoothSocket(bluetooth.RFCOMM)
server_sock.bind(("", bluetooth.PORT_ANY))
server_sock.listen(1)

port = server_sock.getsockname()[1]

uuid = "94f39d29-7d6d-437d-973b-fba39e49d4ee"

bluetooth.advertise_service(server_sock, "SampleServer", service_id=uuid,
                            service_classes=[uuid, bluetooth.SERIAL_PORT_CLASS],
                            profiles=[bluetooth.SERIAL_PORT_PROFILE],
                            # protocols=[bluetooth.OBEX_UUID]
                            )

print("Waiting for connection on RFCOMM channel", port)

client_sock, client_info = server_sock.accept()
print("Accepted connection from", client_info)

# Initialize PyAudio
p = pyaudio.PyAudio()
stream = p.open(format=FORMAT,
                channels=CHANNELS,
                rate=RATE,
                input=True,
                frames_per_buffer=CHUNK)

try:
    while True:
        # Read an audio chunk from the microphone
        audio_data = stream.read(CHUNK, exception_on_overflow=False)
        # Package the audio: [HEADER][Payload Size (2 bytes)][Payload][Checksum (1 byte)][FOOTER]
        payload_size = struct.pack('>H', len(audio_data))
        packet_body = HEADER + payload_size + audio_data
        checksum = bytes([sum(packet_body) & 0xFF])
        packet = packet_body + checksum + FOOTER
        # Send the packet via Bluetooth
        client_sock.send(packet)
except KeyboardInterrupt:
    print("Stopping audio stream...")
finally:
    stream.stop_stream()
    stream.close()
    p.terminate()
    client_sock.close()
    server_sock.close()


print("All done.")