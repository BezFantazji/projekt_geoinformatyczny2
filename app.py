from flask import Flask, render_template, request
import requests

app = Flask(__name__)

BASE_URL = "https://api.gios.gov.pl/pjp-api/v1/rest"


@app.route("/")
def index():
    try:
        stations = requests.get(f"{BASE_URL}/station/findAll").json()
    except Exception as e:
        stations = []
        print("Błąd pobierania stacji:", e)

    return render_template("index.html", stations=stations)


@app.route("/stacja/<int:station_id>")
def station(station_id):
    try:
        sensors = requests.get(f"{BASE_URL}/station/sensors/{station_id}").json()
    except Exception as e:
        sensors = []
        print("Błąd sensorów:", e)

    return render_template("station.html", sensors=sensors, station_id=station_id)


@app.route("/sensor/<int:sensor_id>")
def sensor(sensor_id):
    try:
        data = requests.get(f"{BASE_URL}/data/getData/{sensor_id}").json()
    except Exception as e:
        data = {}
        print("Błąd pobierania danych:", e)

    return render_template("sensor.html", data=data, sensor_id=sensor_id)


if __name__ == "__main__":
    app.run(debug=True)
