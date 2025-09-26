import socket                                                      # Import the socket module to create TCP connections
import json                                                        # Import JSON module to parse and send data in JSON format
import logging
import time


HOST = "0.0.0.0"                                                    # Listen on all network interfaces
PORT = 80                                                           # Use port 80 for this server (common for web apps)

def handle_request(data):
    """
    Receives a JSON string from the client and returns a response dictionary.
    Expected JSON format: 
    {
        "operation": "add",  // add, sub, mul, div
        "a": 10,
        "b": 5
    }   
    
    Returns:
        {"result": a * b, "code": 200} for successful multiplication
        {"error": "...", "code": ...} for errors
    """
#   Try to parse the JSON data

    possible_operations = ("add", "sub", "mul", "div")
    try: 
#       Convert JSON string to Python dictionary
        payload = json.loads(data)                                             
#       Extract 'a' and 'b' from dictionary
        operation, a, b = payload.get("operation"), payload.get("a"), payload.get("b")
#       Check if parameters are missing
        if a is None or b is None:
            return {"error": "Missing parameters", "code": 400}                 # 400 = Bad Request

#       Check if select operation is incorrect
        if operation not in possible_operations:
            return {"error": "Operation doesn't exit", "code": 400}

#       Check if parameters are numbers
        if not isinstance(a, (int, float)) or not isinstance(b, (int, float)):
            return {"error": "Invalid input", "code": 422}                      # 422 = Unprocessable Entity

#       If all good, multiply a and b
        if operation == "mul":
            return {"result": a * b, "code": 200}                                   # 200 = OK
        elif operation == "add":
            return {"result": a + b, "code": 200}
        elif operation == "sub":
            return {"result": a - b, "code": 200}
        elif operation == "div":
            try:
                return {"result": a / b, "code": 200}
            except ZeroDivisionError:
                return {"error": "Zero Division error", "code": 525}                # 525 = ZeroDivisionError
                
    except json.JSONDecodeError:
#       JSON is invalid
        return {"error": "Invalid JSON", "code": 400}

# Socket setup
server_socket = socket.socket()                                                 # Create a TCP socket (IPv4 + TCP)
server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)             # Allow reuse of the address
server_socket.bind((HOST, PORT))                                                # Bind socket to HOST and PORT
server_socket.listen(5)                                             # Listen for connections. '5' = max queued connections
print(f"Calculator server running on {HOST}:{PORT}")                            # Inform server is ready


logger = logging.getLogger(__name__)
logging.basicConfig(filename="server_information.log", level=logging.INFO)
# Main loop to accept clients
while True:
    conn, addr = server_socket.accept()                                         # Wait for a client to connect (blocking)
    
    # Shows the connection time with Year-Month-Day | Hour-Minutes-Seconds
    time.strftime("%Y-%m-%d %H:%M:%S")
    logger.info('Conection start!')
    logger.info(f'Connection START time: {time.strftime("%Y-%m-%d %H:%M:%S")}')
    
    # Client information
    logger.info(f'The clien IP is {addr[0]}')
    logger.info(f'The client port is {addr[1]}\n')
    
    # Data information
    data = conn.recv(1024).decode()                             # Receive up to 1024 bytes and decode from bytes to string
    logger.info(f'Received data from the client: {json.loads(data)}')
    logger.info(f"OPERATION: {json.loads(data['operation'])}")
    logger.info(f"VALUE_a: {json.loads(data['a'])}")
    logger.info(f"VALUE_b: {json.loads(data['b'])}\n")
    
    # Time processing to data
    start = time.time()
    response = handle_request(data)                             # Process the request and get response dictionary
    logger.info(f'Response by the server to client: {response}')
    logger.info(f"RESULT: {response['result']}")
    logger.info(f"CODE: {response['code']}")
    end = time.time()
    total_time = abs(start - end)
    logger.info(f'Time to process data was: {total_time:.8f} seconds\n')
    
    conn.send(json.dumps(response).encode())        # Convert/serialize response to JSON string, encode to bytes, and send
    
    # End connection time
    time.strftime("%Y-%m-%d %H:%M:%S")
    logger.info(f'Connection END time: {time.strftime("%Y-%m-%d %H:%M:%S")}')
    logger.info('Finished')
    conn.close()                                                                # Close connection with the client