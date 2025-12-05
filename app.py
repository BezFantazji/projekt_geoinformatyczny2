from flask import Flask, render_template
import requests

app = Flask(__name__)

BASE_URL = "https://api.gios.gov.pl/pjp-api/v1/rest"

def get_stations():
    try:
        return requests.get(f"{BASE_URL}/station/findAll").json()
    except:
        return []

def get_air_quality(station_id):
    try:
        sensors = requests.get(f"{BASE_URL}/station/sensors/{station_id}").json()
        results = []
        for sensor in sensors:
            sensor_data = requests.get(f"{BASE_URL}/data/getData/{sensor['id']}").json()
            if sensor_data['values']:
                results.append({
                    'param': sensor['param']['paramName'],
                    'value': sensor_data['values'][0]['value']
                })
        return results
    except:
        return []

@app.route("/")
def index():
    stations = get_stations()
    # Pobieramy tylko kilka pierwszych stacji dla demo
    stations_data = []
    for station in stations[:20]:
        stations_data.append({
            'name': station['stationName'],
            'city': station['city']['name'],
            'id': station['id'],
            'air_quality': get_air_quality(station['id'])
        })
    return render_template("index.html", stations=stations_data)

if __name__ == "__main__":
    app.run(debug=True)
