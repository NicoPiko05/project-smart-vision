#echo server
import socket

HOST =        #IPv4 !!!!
PORT = 65432 #random number chosen by me :3

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s: #registers socket as "s"
    s.bind((HOST, PORT)) #binds host and port to socket
    s.listen() #finds port
    conn, addr = s.accept() #connects and creates a new socket object, saves the connection (host) and adress (port)
    with conn: #with the connection (host)
        print(f"Connected by {addr}") #prints adress (port)
        while True:
            data = conn.recv(1024) #recieves 1024 bytes of data
            if not data: #closes the connection if it doesn't recieve any data (b'')
                break
            conn.sendall(data) #sends back?
