from flask import Flask, jsonify, request, render_template
from modules.queries import (
    get_available_pollutants,
    get_available_cities,
    get_daily_city_avg,
    get_multi_city_daily_avg,
    get_city_stats,
    get_city_multi_pollutants,
    get_matrix_data
)


app = Flask(__name__)


@app.route("/")
def index():
    return render_template("index.html")

@app.route("/api/city-multi", methods=["POST"])
def api_city_multi():
    data = request.get_json()
    city = data["city"]
    pollutants = data["pollutants"]
    rows = get_city_multi_pollutants(city, pollutants)
    return jsonify(rows)

@app.route("/api/pollutants")
def api_pollutants():
    rows = get_available_pollutants()
    return jsonify([r[0] for r in rows])


@app.route("/api/cities")
def api_cities():
    return jsonify(get_available_cities())


@app.route("/api/city/<city>/<pollutant>")
def api_city(city, pollutant):
    return jsonify(get_daily_city_avg(city, pollutant))


@app.route("/api/multi", methods=["POST"])
def api_multi():
    data = request.json
    cities = data["cities"]
    pollutant = data["pollutant"]
    rows = get_multi_city_daily_avg(cities, pollutant)
    return jsonify(rows)


@app.route("/api/stats/<city>/<pollutant>")
def api_stats(city, pollutant):
    return jsonify(get_city_stats(city, pollutant))

@app.route("/api/matrix", methods=["POST"])
def api_matrix():
    data = request.get_json()
    cities = data["cities"]
    pollutants = data["pollutants"]
    rows = get_matrix_data(cities, pollutants)
    return jsonify(rows)



if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)

