import socket                                                         # Import socket library for network communication
import json                                                           # Import JSON library to serialize/deserialize data
import time


HOST = "13.58.165.247"                                              # Server IP address (replace with actual AWS server IP)
PORT = 80                                                              # Server port (must be the same as the server)
correct_choices = ("add", "sub", "mul", "div")

# Ask user for numbers first
print("Welcome to Kev's calculator, please select an operation")
print("\t- add")
print("\t- sub")
print("\t- mul")
print("\t- div")
operation = input("Write your selection -> ").lower()


while operation not in correct_choices:
    print("Incorrect selection!\nPlease try again")
    operation = input("Write your selection -> ").lower()

print(f"You choose the '{operation}' operation.")
a_input = input("Enter first number: ")                                 # Prompt user for first number
b_input = input("Enter second number: ")                                # Prompt user for second number

# Convert input to float (so server receives a number, not a string)
try:
    a = float(a_input)                                                  # Try to convert first input to float
    b = float(b_input)                                                  # Try to convert second input to float
except ValueError:                                                      # If conversion fails (non-numeric input)
    print("Invalid input! Please enter numeric values.")                # Show error message
#   Exit program with error code 1, indicating failure. 0 means success.
    exit(1)                                        

# Prepare payload (data to send to server)
payload = {"operation": operation, "a": a, "b": b}                                              # Create dictionary with the numbers
payload_json = json.dumps(payload)                                      # Convert dictionary to JSON string

# Connect to server and send data
client_socket = socket.socket()                                         # Create a TCP socket object
try:
    client_socket.connect((HOST, PORT))                                 # Establish connection to server
    client_socket.send(payload_json.encode())                           # Send JSON string encoded as bytes

#   Receive response from server
    response_data = client_socket.recv(1024)                            # Receive up to 1024 bytes
    response = json.loads(response_data.decode())                       # Decode bytes → str, then parse JSON → dict

#   Print result depending on server's response
    if response.get("code") == 200:                                     # If status code is OK
        print(f"Result from server: {response['result']}")              # Print calculation result
    else:
#       Print error message if server responded with an error
        print(f"Error from server: {response.get('error')} (code {response.get('code')})")

except ConnectionRefusedError:
		print("Could not connect to the server. Is it running?")