import pika
from elasticsearch import Elasticsearch
from time import sleep
import metric_pb2
import os

try:
    if os.environ['withdocker'] != '0':
        elastic_host = 'elasticsearch'
        rabbitmq_host = 'rabbitmq'
    else:
        elastic_host = 'localhost'
        rabbitmq_host = 'localhost'
except KeyError:
    elastic_host = 'localhost'
    rabbitmq_host = 'localhost'


# Connect to RabbitMQ
connection = pika.BlockingConnection(pika.ConnectionParameters(host=rabbitmq_host))  # Production
channel = connection.channel()

# Connect to ElasticSearch
es = Elasticsearch([{"host": elastic_host, "port": 9200, "scheme": "http"}])

# Create the indexes if needed
if not es.indices.exists(index="parsed_data"):
    es.indices.create(index="parsed_data")

if not es.indices.exists(index="data_queue"):
    es.indices.create(index="data_queue")


def parse_data(data):
    # Parse data from the queue.
    metric = metric_pb2.Metric()
    metric.ParseFromString(data)

    # Extract the values from the metric object
    name = metric.name
    type = metric.type
    value = metric.value
    tags = metric.tags

    # Create a dictionary with the extracted values
    parsed_data = {
        "name": name,
        "type": type,
        "value": value,
        "tags": tags
    }
    return parsed_data


def callback(ch, method, properties, body):
    # Parse the data and store it in Elasticsearch
    data = parse_data(body)
    print(f'callback {data}')
    response = es.index(index="parsed_data", document=data)
    print(response)


# Start a consumer to read from the message queue
try:
    channel.basic_consume(queue="data_queue", on_message_callback=callback, auto_ack=True)
    channel.start_consuming()
except Exception as e:
    print(f"There was an error processing the callback. Check the queue, error type: {e}")
    sleep(20)
    channel.basic_consume(queue="data_queue", on_message_callback=callback, auto_ack=True)
    channel.start_consuming()
