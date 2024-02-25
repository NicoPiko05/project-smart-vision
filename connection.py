#echo server
#CLIENT: raspberry (tenhle kód, pc)
import socket

HOST = '10.0.0.85'
PORT = 12345

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.connect((HOST, PORT))
message = ("Connected ! :3")
sock.send(message.encode("utf-8"))

while True:
    data = sock.recv(1024)
    if not data:
        break
    print(f"Message: {data.decode('utf-8')}")
    message = input("Enter message:")
    sock.send(message.encode("utf-8"))

sock.close()