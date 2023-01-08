from flask import Flask, render_template, request
import requests

app = Flask(__name__)


@app.route("/")
def home():
    # Render the template and pass the data to it
    return render_template("home.html")


@app.route("/search", methods=["GET"])
def search():
    search_type = request.args.get("search-type")
    name = request.args.get("name")

    if search_type == "count-by-name":
        api_response = requests.get(f"http://localhost:5000/api/data/search/count-by-name/{name}")
    elif search_type == "average-by-name":
        api_response = requests.get(f"http://localhost:5000/api/data/search/average-by-name/{name}")
    else:
        api_response = requests.get("http://localhost:5000/api/data")

    data = api_response.json()

    return render_template("home.html", data=data)


'''HERE ARE APIS WE WONT USE FOR THE GUI, LEFT THEM THERE AFTER TESTING...'''


@app.route("/name/<name>")  # search by sensor_1 in this example
def return_data_by_name(name):
    # Retrieve the data from the API
    api_response = requests.get(f"http://localhost:5000/api/data/search/name/{name}")
    data = api_response.json()

    # Render the template and pass the data to it
    return render_template("home.html", data=data)


@app.route("/count-by-name/<name>")  # in this example sensor_1
def search_count_data_by_name(name):
    # Perform an Elasticsearch query for documents with the specified name
    api_response = requests.get(f"http://localhost:5000/api/data/search/count-by-name/{name}")
    data = api_response.json()
    print(data)

    # Render the template and pass the data to it
    return render_template("home.html", data=data)


@app.route("/average-by-name/<name>")  # in this example sensor_1
def search_calculate_average_data_by_name(name):
    # Perform an Elasticsearch query for documents with the specified name
    api_response = requests.get(f"http://localhost:5000/api/data/search/average-by-name/{name}")
    data = api_response.json()
    # Render the template and pass the data to it
    return render_template("home.html", data=data)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5001, debug=True)
