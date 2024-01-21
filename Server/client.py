import socket
import pickle


def send_signal():
    host = '10.43.231.203'  # Replace with the IP address or hostname of the server
    port = 12345         # Use the same port as the server

    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((host, port))

    signal = {"banana":"yellow","blueberry":"blue"}
    serialized_signal = pickle.dumps(signal)
    client_socket.send(serialized_signal)

    client_socket.close()


send_signal()