import socket                                                      # Import the socket module to create TCP connections
import json                                                        # Import JSON module to parse and send data in JSON format
import logging
import time


HOST = "0.0.0.0"                                                    # Listen on all network interfaces
PORT = 8080                                                           # Use port 80 for this server (common for web apps)

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
#       Extract 'a' and 'b' and 'operation' from dictionary
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

conection = True
# Main loop to accept clients
while conection:
    # Wait for a client to connect (blocking)
    conn, addr = server_socket.accept()  

    # START CONECTION
    logger.info(f"[CONNECTION OPENED] Timestamp: {time.strftime('%Y-%m-%d %H:%M:%S')}")
    logger.info(f"[CLIENT INFO] IP: {addr[0]}, Port: {addr[1]}\n")

    # RECEIVED DATA
    data = conn.recv(1024).decode()
    parsed_data = json.loads(data)
    if parsed_data['operation'] == 'quit':
        conection = False
        logger.info("[REQUEST RECEIVED] Raw Data: {CONECTION END: 100}")

        # END CONECTION
        logger.info(f"[CONNECTION CLOSED] Timestamp: {time.strftime('%Y-%m-%d %H:%M:%S')}\n")
        conn.close()
    logger.info(f"[REQUEST RECEIVED] Raw Data: {data}")
    logger.info(f"[REQUEST DETAILS] Operation: {parsed_data['operation']}, Operand A: {parsed_data['a']}, Operand B: {parsed_data['b']}\n")

    # PROCESSING
    start = time.time()
    response = handle_request(data)
    end = time.time()
    total_time = end - start
    logger.info(f"[RESPONSE SENT] Data: {response}")
    logger.info(f"[RESPONSE DETAILS] Result: {response.get('result', 'N/A')}, Code: {response.get('code', 'N/A')}")
    logger.info(f"[PROCESSING TIME] {total_time:.7f} seconds\n")

    conn.send(json.dumps(response).encode())

    # END CONECTION
    logger.info(f"[CONNECTION CLOSED] Timestamp: {time.strftime('%Y-%m-%d %H:%M:%S')}\n")
    
# # Close connection with the client
# conn.close()                                                          