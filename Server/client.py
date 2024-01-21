import socket
import pickle

# Client configuration
host = '10.43.231.203'  # Replace with the IP address of Computer A
port = 12345  # Use the same port number as in the server

# Create a socket object
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Connect to the server
client_socket.connect((host, port))

# Loop to send and receive messages
while True:
    # Send a Python object (e.g., list, int) to the server
    message = input("Enter your message (list, int, etc.): ")

    # Serialize the message using pickle before sending
    message_data = pickle.dumps(message)
    client_socket.send(message_data)

    # Receive a response from the server
    response_data = client_socket.recv(1024)

    if not response_data:
        break  # If no data is received, break the loop

    # Deserialize the response using pickle
    response = pickle.loads(response_data)
    print(f"Received from server: {response}")

    # Send a Python object (e.g., list, int) to the server
    client_message = input("Enter your response to server: ")

    # Serialize the client message using pickle before sending
    client_message_data = pickle.dumps(client_message)
    client_socket.send(client_message_data)

# Close the socket
client_socket.close()
