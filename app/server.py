import asyncio
import pika
from aiohttp import web

"""
SSL/TLS is a protocol that provides secure communication over the internet by encrypting data that is
transmitted between the client and the server. This server upon request is not secured.
"""


# Connect to RabbitMQ
connection = pika.BlockingConnection(pika.ConnectionParameters("localhost"))
channel = connection.channel()

# Declare a queue
channel.queue_declare("data_queue")


async def publish_to_queue(data):  # made this async so when asyncio calls it, the function will run on the same thread.
    # Publish the data to the queue
    channel.basic_publish(exchange="", routing_key="data_queue", body=data)


async def receive_data(request):
    # Get the data from the request
    data = await request.read()
    # Run the queue publishing in a separate asyncio task
    asyncio.create_task(publish_to_queue(data))
    return web.Response(text="Data received and published to queue")


app = web.Application()
app.add_routes([web.post("/", receive_data)])

web.run_app(app)


# # Option with fastapi. Its getting weird with asyncio so ill stick to the previous script.
# from fastapi import FastAPI
# import pika
# import asyncio
# import uvicorn
#
# # Connect to RabbitMQ
# connection = pika.BlockingConnection(pika.ConnectionParameters("localhost"))
# channel = connection.channel()
#
# # Declare a queue
# channel.queue_declare("data_queue")
#
# app = FastAPI()
#
#
# async def publish_to_queue(_data):
#     # Publish the data to the queue
#     await channel.basic_publish(exchange="", routing_key="data_queue", body=_data)
#
#
# @app.post("/")
# async def receive_data(_request):
#     # Run the queue publishing in a separate asyncio task
#     _data = await _request.read()
#     asyncio.create_task(publish_to_queue(_data))
#     return {"message": "Data received and published to queue"}
#
# if __name__ == '__main__':
#     uvicorn.run(app, host="0.0.0.0", port=8080)

