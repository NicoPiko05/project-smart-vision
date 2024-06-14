#!/usr/bin/env python3
import socket

def start_server():
    try:
        # Server address and port
        server_address = '192.168.158.223'  # IP address to bind to (localhost)
        server_port = 65432  # Port number to listen on
        print(1)
        # Create a socket object
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        print(2)
        # Bind the socket to the address and port
        server_socket.bind((server_address, server_port))
        print(3)
        # Listen for incoming connections (max 1 connection in the queue)
        server_socket.listen(1)
        print(f"Server listening on {server_address}:{server_port}")

        # Accept a connection
        connection, client_address = server_socket.accept()
        print(f"Connection from {client_address}")

        try:
            while(1 == 1):
                # Receive the message from the client
                message = connection.recv(1024).decode('utf-8')
                print(f"Message from client: {message}")

                # Send a response back to the client
                response_message = "Hello, Client!"
                connection.sendall(response_message.encode('utf-8'))
                print(f"Sent response to client: {response_message}")

        finally:
            # Clean up the connection
            connection.close()
            print("Connection closed")
    except Exception as e:
        print(f"An error occured: {e}")
if __name__ == "__main__":
    start_server()