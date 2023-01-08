FROM python:3.9

# Create the app directory and copy the source code to it
RUN mkdir -p /app
WORKDIR /app
COPY .. /app

# Install the dependencies
RUN pip install -r requirements.txt

# Run the client app
CMD ["python", "client.py"]
