from flask import Flask, render_template, request
import requests

app = Flask(__name__)

# Przykładowy URL do pobrania stacji i danych
BASE_URL = "https://api.gios.gov.pl/pjp-api/rest"

@app.route("/", methods=["GET"])
def index():
    # Pobranie listy stacji pomiarowych
    stations_url = f"{BASE_URL}/station/findAll"
    response = requests.get(stations_url)
    
    if response.status_code == 200:
        stations = response.json()
    else:
        stations = []

    return render_template("index.html", stations=stations)

@app.route("/data/<int:station_id>")
def get_station_data(station_id):
    data_url = f"{BASE_URL}/data/getData/{station_id}"
    response = requests.get(data_url)
    
    if response.status_code == 200:
        data = response.json()
    else:
        data = {"error": "Nie udało się pobrać danych"}

    return render_template("index.html", data=data, station_id=station_id)

if __name__ == "__main__":
    app.run(debug=True)
