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
def send_message(message):
    # Serialize the message using pickle before sending
    message_data = pickle.dumps(message)
    client_socket.send(message_data)

    # Receive a response from the server
    response_data = client_socket.recv(1024)

    # Deserialize the response using pickle
    response = pickle.loads(response_data)
    print(f"Received from server: {response}")

    return response

# Close the socket
#client_socket.close()
    
#send_message("testing function")
