from fastapi import FastAPI
from elasticsearch import Elasticsearch
import os
import uvicorn
from dotenv import load_dotenv

load_dotenv('.env')

# run on the right host if run locally or on docker.
try:
    if os.environ['withdocker'] != '0':
        base_url = 'elasticsearch'
    else:
        base_url = 'localhost'
except KeyError:
    base_url = 'localhost'


# Connect to Elasticsearch
es = Elasticsearch([{"host": base_url, "port": 9200, "scheme": "http"}])

app = FastAPI()


@app.get("/api/data")
async def get_data():
    # Perform an Elasticsearch query and return the results as a JSON response
    res = es.search(index="parsed_data", body={"query": {"match_all": {}}})
    print(res)
    return {res["hits"]["hits"]}


@app.get("/api/data/search/name/{name}")  # in this example sensor_1
def search_data_by_name(name):
    # Perform an Elasticsearch query for documents with the specified name
    res = es.search(index="parsed_data", q=f"name:{name}")
    print(res["hits"]["hits"][0]['_source']['value'])
    return {res["hits"]["hits"]}


@app.get("/api/data/search/count-by-name/{name}")  # in this example sensor_1
def search_count_data_by_name(name):
    # Perform an Elasticsearch query for documents with the specified name
    res = es.search(index="parsed_data", q=f"name:{name}", size=1000)
    measurements_count = len(res['hits']['hits'])

    return {
        "sensor_name": name,
        "count": measurements_count}


@app.get("/api/data/search/average-by-name/{name}")  # in this example sensor_1
def search_calculate_average_data_by_name(name):
    # Perform an Elasticsearch query for documents with the specified name
    try:
        res = es.search(index="parsed_data", q=f"name:{name}", size=1000)

        print(res)

        measurement_values = [hit['_source']['value'] for hit in res["hits"]["hits"]]

        if sum(measurement_values) > 0:
            average = sum(measurement_values) / len(measurement_values)
        else:
            average = 0

        return {
            "sensor_name": name,
            "average": average}
    except Exception as e:
        print(e)
        return {'sensor doesnt exist': name}


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=5000)
