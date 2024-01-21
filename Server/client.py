import socket

# Client configuration
host = '10.43.231.203'  # Replace with the IP address of Computer A
port = 12345  # Use the same port number as in the server

# Create a socket object
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Connect to the server
client_socket.connect((host, port))

# Loop to send and receive messages
while True:
    # Send a message to the server
    message = input("Enter your message: ")
    client_socket.send(message.encode('utf-8'))

    # Receive a response from the server
    response = client_socket.recv(1024).decode('utf-8')
    print(f"Received from server: {response}")

    # Send a message to the server
    client_message = input("Enter your response to server: ")
    client_socket.send(client_message.encode('utf-8'))

# Close the socket
client_socket.close()
