from flask import Flask, render_template
import requests

app = Flask(__name__)
BASE_URL = "https://api.gios.gov.pl/pjp-api/v1/rest/aqindex/getIndex/52"

@app.route("/")
def index():
    stations_url = f"{BASE_URL}/station/findAll"
    response = requests.get(stations_url)
    stations = response.json() if response.status_code == 200 else []
    return render_template("index.html", stations=stations)

@app.route("/data/<int:station_id>")
def get_station_data(station_id):
    # Pobranie listy sensorów dla stacji
    sensors_url = f"{BASE_URL}/station/sensors/{station_id}"
    sensors_response = requests.get(sensors_url)
    if sensors_response.status_code != 200:
        return "Błąd pobierania sensorów"

    sensors = sensors_response.json()
    data_list = []

    # Pobranie danych dla każdego sensora
    for sensor in sensors:
        sensor_id = sensor["id"]
        data_url = f"{BASE_URL}/data/getData/{sensor_id}"
        data_response = requests.get(data_url)
        if data_response.status_code == 200:
            sensor_data = data_response.json()
            # Dodanie nazwy parametru do danych
            data_list.append({
                "param": sensor["param"]["paramName"],
                "values": sensor_data.get("values", [])
            })

    return render_template("index.html", data=data_list, station_id=station_id)

if __name__ == "__main__":
    app.run(debug=True)
