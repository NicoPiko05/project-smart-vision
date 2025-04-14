import bluetooth
import pyaudio
import struct

# Audio constants
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 16000
CHUNK = 1024

#packet constants
HEADER = b'\xAA\xBB'
FOOTER = b'\xCC\xDD'

def initbluetooth():

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

    p = pyaudio.PyAudio()
    stream = p.open(
        format=FORMAT,
        channels=CHANNELS,
        rate=RATE,
        input=True,
        frames_per_buffer=CHUNK)

    try:
        while True:
            # Read audio chunk
            audio_data = stream.read(CHUNK, exception_on_overflow=False)
            # Create payload size field (2 bytes, big-endian)
            payload_size = struct.pack('>H', len(audio_data))
            # Build packet without checksum
            packet_body = HEADER + payload_size + audio_data
            # Compute checksum (sum modulo 256)
            checksum = bytes([sum(packet_body) & 0xFF])
            # Construct final packet
            packet = packet_body + checksum + FOOTER

            # Send packet via Bluetooth
            client_sock.send(packet)
    except KeyboardInterrupt:
        print("Terminating connection.")
    finally:
        stream.stop_stream()
        stream.close()
        p.terminate()
        client_sock.close()
        server_sock.close()