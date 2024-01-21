import socket

# Server configuration
host = '0.0.0.0'  # Listen on all available interfaces
port = 12345  # Choose a port number

# Create a socket object
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Bind the socket to a specific address and port
server_socket.bind((host, port))

# Listen for incoming connections
server_socket.listen(1)

print(f"Server listening on {host}:{port}")

# Accept a connection from the client
client_socket, client_address = server_socket.accept()
print(f"Connection from {client_address}")

# Loop to receive and send messages
while True:
    # Receive data from the client
    data = client_socket.recv(1024).decode('utf-8')
    
    if not data:
        break  # If no data is received, break the loop
    
    print(f"Received from client: {data}")

    # Send a response back to the client
    response = input("Enter your response: ")
    client_socket.send(response.encode('utf-8'))

    # Receive a message from the client
    client_message = client_socket.recv(1024).decode('utf-8')
    print(f"Received from client: {client_message}")

# Close the sockets
client_socket.close()
server_socket.close()
