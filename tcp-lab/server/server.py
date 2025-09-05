import socket

# Define the host for that the server liste all avaible network interfaces
HOST = '0.0.0.0'

# Set the port number where it will listen for incoming connections
PORT = 12345

# Create a new socket object (endpoint network communication)
s = socket.socket()

# Associate the socket with the specified host and port
# This tells the OS, "Send any data arriving at port 12345 to this program."
s.bind((HOST, PORT))

# Starts listening for incoming connections
# The 1 means it can queue up to one connection.
s.listen(1)

print("TCP server waiting for connection...")

# Waits for a client to connect
# When someone connects, accept() returns a new socket object (for communication) representing the connection and the address of the client.
conn, addr = s.accept()


print(f"Connected to {addr}")

# The new socket object can now be used to send and receive data on the connection
# b to refers send to bytes
conn.send(b"Hello from Dockerized EC2 server!")
conn.close()