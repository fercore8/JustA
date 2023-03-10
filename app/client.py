import asyncio
import aiohttp
import random
import metric_pb2
import os

# run on the right host if run locally or on docker.
try:
    if os.environ['withdocker'] != '0':
        base_url = 'http://server:8080'
    else:
        base_url = 'http://localhost:8080'
except KeyError:
    base_url = 'http://localhost:8080'

sensors_list = ["sensor_1", "sensor_2", "sensor_3"]  # if we were to measure heat sensors from an engine


# Define a function for generating the data
def generate_data():
    metric = metric_pb2.Metric()
    metric.name = random.choice(sensors_list)
    metric.type = "heat_sensor"
    metric.value = random.random()
    metric.tags = "main_engine"
    return metric


async def send_data():
    # Serialize the data using protobuf
    serialized_data = generate_data().SerializeToString()

    # Create an aiohttp client
    async with aiohttp.ClientSession() as session:
        # Send the data to the server as post request
        try:
            async with session.post(base_url, data=serialized_data) as resp:
                print(await resp.text())
        except Exception as e:
            print(e)
        await asyncio.sleep(5)

# Create a loop that sends the data to the server at a specific interval
while True:
    asyncio.run(send_data())
