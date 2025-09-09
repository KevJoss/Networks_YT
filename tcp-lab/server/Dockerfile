# This line tells Docker to use a lightweight version of Python 3.10 as 
# the base image for your container.
FROM python:3.10-slim

# Sets the working directory inside the container to /app. 
# All following commands will run in this folder.
WORKDIR /app

# Copies the server.py file from your project 
# into the /app directory inside the container.
COPY server.py .

# Specifies the default command to run when the container starts: 
# it will execute python server.py.
CMD ["python", "server.py"]