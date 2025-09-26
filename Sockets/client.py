# client.py

import socket  # Import the 'socket' module to create network connections (TCP/UDP).

HOST = 'your-public-ip-address'  # Server IP to connect to. 'localhost' means the same machine, or write the AWS' IP address.
PORT = 80           # Server port to connect to. Must match the server's port

client_socket = socket.socket()        # Creates a TCP socket (IPv4 + TCP by default)
client_socket.connect((HOST, PORT))   # Connects to the server at (HOST, PORT)

data = client_socket.recv(1024)        # Receives data from the server
                                       # 1024 = max number of bytes to read per call
print("Received:", data.decode())      # Decode bytes to string and print

client_socket.close()                  # Closes the connection with the server