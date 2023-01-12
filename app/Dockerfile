FROM python:3.9

# Create the app directory and copy the source code to it
COPY . /app
COPY requirements.txt /app/requirements.txt
WORKDIR /app

ENV withdocker=1

# Install the dependencies
RUN pip install -r requirements.txt

## Run the client app
#CMD ["python"]
