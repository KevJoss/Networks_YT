# calculator_server.py

import socket  # Import the socket module to create TCP connections
import json    # Import JSON module to parse and send data in JSON format

HOST = "0.0.0.0"  # Listen on all network interfaces
PORT = 80       # Use port 80 for this server (common for web apps)

def handle_request(data):
    """
    Receives a JSON string from the client and returns a response dictionary.
    Expected JSON format: {"a": number, "b": number}
    Returns:
        {"result": a * b, "code": 200} for successful multiplication
        {"error": "...", "code": ...} for errors
    """
    # Try to parse the JSON data
    try: 
        payload = json.loads(data)  # Convert JSON string to Python dictionary
        a, b = payload.get("a"), payload.get("b")  # Extract 'a' and 'b' from dictionary

        # Check if parameters are missing
        if a is None or b is None:
            return {"error": "Missing parameters", "code": 400}  # 400 = Bad Request

        # Check if parameters are numbers
        if not isinstance(a, (int, float)) or not isinstance(b, (int, float)):
            return {"error": "Invalid input", "code": 422}  # 422 = Unprocessable Entity

        # If all good, multiply a and b
        return {"result": a * b, "code": 200}  # 200 = OK

    except json.JSONDecodeError:
        # JSON is invalid
        return {"error": "Invalid JSON", "code": 400}

# Socket setup
server_socket = socket.socket()        # Create a TCP socket (IPv4 + TCP)
server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)  # Allow reuse of the address
server_socket.bind((HOST, PORT))      # Bind socket to HOST and PORT
server_socket.listen(5)                # Listen for connections. '5' = max queued connections
print(f"Calculator server running on {HOST}:{PORT}")  # Inform server is ready

# Main loop to accept clients
while True:
    conn, addr = server_socket.accept()  # Wait for a client to connect (blocking)
    data = conn.recv(1024).decode()      # Receive up to 1024 bytes and decode from bytes to string
    response = handle_request(data)      # Process the request and get response dictionary
    conn.send(json.dumps(response).encode())  # Convert/serialize response to JSON string, encode to bytes, and send
    conn.close()                         # Close connection with the client