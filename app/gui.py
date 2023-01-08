from flask import Flask, render_template
import requests

app = Flask(__name__)


@app.route("/")
def home():
    # Retrieve the data from the API
    api_response = requests.get("http://localhost:5000/api/data")
    data = api_response.json()

    # Render the template and pass the data to it
    return render_template("home.html", data=data)


@app.route("/name/<name>")  # search by sensor_1 in this example
def return_data_by_name(name):
    # Retrieve the data from the API
    api_response = requests.get(f"http://localhost:5000/api/data/search/name/{name}")
    data = api_response.json()

    # Render the template and pass the data to it
    return render_template("home.html", data=data)


@app.route("/count-by-name/<name>") # in this example sensor_1
def search_count_data_by_name(name):
    # Perform an Elasticsearch query for documents with the specified name
    api_response = requests.get(f"http://localhost:5000/api/data/search/count-by-name/{name}")
    data = api_response.json()
    print(data)

    # Render the template and pass the data to it
    return render_template("home.html", data=data)


@app.route("/average-by-name/<name>") # in this example sensor_1
def search_calculate_average_data_by_name(name):
    # Perform an Elasticsearch query for documents with the specified name
    api_response = requests.get(f"http://localhost:5000/api/data/search/average-by-name/{name}")
    data = api_response.json()
    print(data)
    # Render the template and pass the data to it
    return render_template("home.html", data=data)



if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5001, debug=True)
