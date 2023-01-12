from flask import Flask, jsonify
from elasticsearch import Elasticsearch
import os
import uvicorn
from dotenv import load_dotenv

try:
    if os.environ['withdocker'] != '0':
        base_url = 'elasticsearch'
    else:
        base_url = 'localhost'
except KeyError:
    base_url = 'localhost'

load_dotenv('.env')

app = Flask(__name__)

# Connect to Elasticsearch
es = Elasticsearch([{"host": base_url, "port": 9200, "scheme": "http"}])


@app.route("/api/data")
def get_data():
    # Perform an Elasticsearch query and return the results as a JSON response
    res = es.search(index="parsed_data", body={"query": {"match_all": {}}})
    print(res)
    return jsonify(res["hits"]["hits"])


@app.route("/api/data/search/name/<name>")  # in this example sensor_1
def search_data_by_name(name):
    # Perform an Elasticsearch query for documents with the specified name
    res = es.search(index="parsed_data", q=f"name:{name}")
    print(res["hits"]["hits"][0]['_source']['value'])
    return jsonify(res["hits"]["hits"])


@app.route("/api/data/search/count-by-name/<name>")  # in this example sensor_1
def search_count_data_by_name(name):
    # Perform an Elasticsearch query for documents with the specified name
    res = es.search(index="parsed_data", q=f"name:{name}", size=1000)
    measurements_count = len(res['hits']['hits'])

    return jsonify({
        "sensor_name": name,
        "count": measurements_count})


@app.route("/api/data/search/average-by-name/<name>")  # in this example sensor_1
def search_calculate_average_data_by_name(name):
    # Perform an Elasticsearch query for documents with the specified name
    try:
        res = es.search(index="parsed_data", q=f"name:{name}", size=1000)

        measurement_values = [hit['_source']['value'] for hit in res["hits"]["hits"]]

        average = sum(measurement_values) / len(measurement_values)

        return jsonify({
            "sensor_name": name,
            "average": average})
    except Exception as e:
        print(e)
        return jsonify({'sensor doesnt exist': name})


if __name__ == "__main__":
    try:
        if os.environ['withdocker'] != '0':
            uvicorn.run(app, host="0.0.0.0", port=5000)  # Production
        else:
            app.run(host="0.0.0.0", port=5000, debug=True)  # Dev

    except KeyError:
        app.run(host="0.0.0.0", port=5000, debug=True)    # Dev
