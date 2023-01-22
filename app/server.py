import asyncio
import pika
from fastapi import FastAPI, Request
import uvicorn
import os

"""
SSL/TLS is a protocol that provides secure communication over the internet by encrypting data that is
transmitted between the client and the server. This server upon request is not secured.
"""
try:
    if os.environ['withdocker'] != '0':
        rabbitmq_host = 'rabbitmq'
    else:
        rabbitmq_host = 'localhost'
except KeyError:
    rabbitmq_host = 'localhost'

print(f'current environment {rabbitmq_host}')

app = FastAPI()


# Connect to RabbitMQ
connection = pika.BlockingConnection(pika.ConnectionParameters(host=rabbitmq_host))  # Production
channel = connection.channel()

# Declare a queue
channel.queue_declare("data_queue")


async def publish_to_queue(data):  # made this async so when asyncio calls it, the function will run on the same thread.
    # Publish the data to the queue
    channel.basic_publish(exchange="", routing_key="data_queue", body=data)


@app.post('/')
async def receive_data(request: Request):
    # Get the data from the request
    print(request.headers)
    print(request.body)

    data = await request.body()
    # Run the queue publishing in a separate asyncio task
    asyncio.create_task(publish_to_queue(data))
    return {'message': "Data received and published to queue"}


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8080)
