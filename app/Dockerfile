FROM python:3.9-alpine

# Create the app directory and copy the source code to it
COPY . /app
COPY requirements.txt /app/requirements.txt
WORKDIR /app

ENV withdocker=1

# Install the dependencies
RUN pip install --no-cache-dir --upgrade -r requirements.txt
