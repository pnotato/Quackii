import socket
import pickle
import random

def start_server(): 
    host = '0.0.0.0'
    port = 12345
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((host, port))
    server_socket.listen(10)
    server_socket.setblocking(False)  # Set the socket to non-blocking mode

    print(f"Server listening on {host}:{port}")

    messages = []

    while True:
        try:
            client_socket, client_address = server_socket.accept()
            print(f"Connection from {client_address}")

            serialized_signal = client_socket.recv(1024)
            signal = pickle.loads(serialized_signal)
            messages.append(signal)
            print(f"Received data: {signal}")

            response = random.choice(messages)
            serialized_response = pickle.dumps(response)
            client_socket.send(serialized_response)

            #client_socket.close()
        except BlockingIOError:
            continue  # If no client is ready to connect, continue the loop

if __name__ == "__main__":
    start_server()
