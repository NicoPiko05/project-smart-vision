#echo server
#CLIENT: raspberry (tenhle kód, pc)
import socket

HOST = "14:99:3E:DB:03:97" #server ip
PORT = 4

sock = socket.socket(socket.AF_BLUETOOTH, socket.SOCK_STREAM, socket.BTPROTO_RFCOMM)
sock.connect((HOST, PORT))

message = ("Connected !")
sock.send(message.encode("utf-8"))

while True:
    data = sock.recv(1024)
    if not data:
        break
    print(f"Message: {data.decode('utf-8')}")
    message = input("Enter message:")
    sock.send(message.encode("utf-8"))

sock.close()