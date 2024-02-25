#echo server
import socket

addr = ''
channel = 4

server = socket.socket(socket.AF_BLUETOOTH, socket.SOCK_STREAM, socket.BTPROTO_RFCOMM)
server.connect((addr, channel))
server.listen(1)

client, addr = server.accept()

try:
    while True:
        data = client.recv(1024)
        if not data:
            break
        print(f"Message: {data.decode('utf-8')}")
        message = input("Enter message:")
        client.send(message.encode("utf-8"))

except OSError as e:
    pass

client.close()
server.close()