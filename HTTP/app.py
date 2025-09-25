# app.py
# THIS CODES CREATE MY SERVER RESPONSES TO GET METHODS AND 
# SPECIALIZED METHODS DEFINED BY ME

from fastapi import FastAPI, Response, Request

# This is your main API object, used to define routes and run the server.
app = FastAPI()

# @app.get("/") tells FastAPI: 
# "Register this function to handle GET requests to the root path (/)"

@app.get("/")

# When someone visits http://localhost:8000/ with a GET request, this function executes
# It returns a Python dictionary that converts to JSON file to headers.
def read_root():
    return {"message": "Hello, GET request!"}

# POST requests are typically used to send data to the server (unlike GET which just retrieves data)
# When a client sends a POST request to http://localhost:8000/submit, this function runs

@app.post("/submit")

# 2. FastAPI automatically:
#       Reads the JSON from the request body
#       Converts it to a Python dictionary
#       Passes it as the data parameter to your function

# Parameter: data: dict means this function expects to receive a dictionary
def submit_data(data: dict):
    return {"received": data}


# Decorator that handles GET requests to the /cookie URL
# When someone visits http://localhost:8000/cookie, this function executes


@app.get("/cookie")

# response: Response - This gives you access to modify the HTTP response
def set_cookie(response: Response):
    
    # This cookie will be stored in the browser and sent back with future requests
    response.set_cookie(key="user", value="student123")
    
    # Returns a JSON response confirming the cookie was set
    # The browser receives both the JSON message AND the cookie
    return {"message": "Cookie set!"}