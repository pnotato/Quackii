import socket
import pickle

class Client:
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.connect_to_server()

    def connect_to_server(self):
        # Connect to the server
        self.client_socket.connect((self.host, self.port))

    def send_message(self, message):
        # Serialize the message using pickle before sending
        message_data = pickle.dumps(message)
        self.client_socket.send(message_data)

    def receive_message(self):
        data = self.client_socket.recv(1024)
        if not data:
            return None
        # Deserialize the received data using pickle
        received_data = pickle.loads(data)
        return received_data

    def close_connection(self):
        # Close the socket
        self.client_socket.close()

# Example usage:
client = Client('10.43.231.203', 12345)
client.send_message("Hello, server!")
response = client.receive_message()
client.close_connection()
