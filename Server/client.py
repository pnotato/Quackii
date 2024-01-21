import socket
import pickle
import random
import asyncio

def send_signal(signal): 
    host = '127.0.0.1'
    port = 12345
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((host, port))
    client_socket.setblocking(False)  # Set the socket to non-blocking mode

    serialized_signal = pickle.dumps(signal)

    try:
        client_socket.send(serialized_signal)
    except BlockingIOError:
        print("Server is not ready to receive data.")

    while True:
        try:
            serialized_response = client_socket.recv(1024)
            break  # If data is received, break the loop
        except BlockingIOError:
            continue  # If no data is received, continue the loop

    response = pickle.loads(serialized_response)

    client_socket.close()

    return response

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