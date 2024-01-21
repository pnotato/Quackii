import socket
import pickle

def start_server():
    host = '0.0.0.0'  # Listen on all available interfaces
    port = 12345       # Choose a port (ensure it's open and not in use)

    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((host, port))
    server_socket.listen(1)  # Listen for one incoming connection

    print(f"Server listening on {host}:{port}")

    while True:
        client_socket, client_address = server_socket.accept()
        print(f"Connection from {client_address}")
        
        # Handle the signal or data received from the client
        serialized_signal = client_socket.recv(1024)
        signal = pickle.loads(serialized_signal)
        print(f"Received data: {signal}")

        # Close the connection
        client_socket.close()

if __name__ == "__main__":
    start_server()
