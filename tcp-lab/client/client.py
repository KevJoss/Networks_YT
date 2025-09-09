import socket

# Give the AWS EC2 instance's public IP address here and the port number
# where the server is listening
HOST = '13.58.165.247'
PORT = 12345

# Create a TCP socket and connect to the server
s = socket.socket()

# Initiates a conection from the client to the server at the specified HOST and PORT
s.connect((HOST, PORT))

# Waits to receive up to 1024 bytes of data from the server.
data = s.recv(1024)

# Decodes the received bytes into a string and prints it.
print("Received:", data.decode())

# Closes the socket connection.
s.close()