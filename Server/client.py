import socket
import pickle
import random
import asyncio

def send_signal(message):
    host = '10.43.231.203'  # Replace with the IP address or hostname of the server
    port = 12345         # Use the same port as the server

    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((host, port))

    serialized_signal = pickle.dumps(message)
    client_socket.send(serialized_signal)

    client_socket.close()

def receive_signal(): 
    host = '0.0.0.0'
    port = 12346         # Arbitrary non-privileged port
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    
    server_socket.bind((host, port))
    server_socket.listen()
    client_socket, address = server_socket.accept()
    print(f"Connection from {address} has been established!")
    serialized_message = client_socket.recv(1024)
    message = pickle.loads(serialized_message)
    return message

#send_signal()