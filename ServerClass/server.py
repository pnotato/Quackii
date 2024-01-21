import socket
import pickle

class Server:
    def __init__(self, host='0.0.0.0', port=12345):
        self.host = host
        self.port = port
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client_socket = None
        self.start_server()

    def start_server(self):
        # Bind the socket to a specific address and port
        self.server_socket.bind((self.host, self.port))
        # Listen for incoming connections
        self.server_socket.listen(1)
        print(f"Server listening on {self.host}:{self.port}")

        # Accept a connection from the client
        self.client_socket, client_address = self.server_socket.accept()
        print(f"Connection from {client_address}")

    def receive_messages(self):
        try:
            while True:
                # Receive data from the client
                data = self.client_socket.recv(1024)
                if not data:
                    break  # If no data is received, break the loop

                # Deserialize the received data using pickle
                received_data = pickle.loads(data)
                print(f"Received from client: {received_data}")

                # Send a response back to the client
                response = input("Enter your response: ")

                # Serialize the response using pickle before sending
                response_data = pickle.dumps(response)
                self.client_socket.send(response_data)

        except KeyboardInterrupt:
            pass
        finally:
            self.close_connection()

    def close_connection(self):
        # Close the sockets
        self.client_socket.close()
        self.server_socket.close()

# Example usage:
server = Server()
server.receive_messages()
