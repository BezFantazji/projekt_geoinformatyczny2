from flask import Flask, render_template, abort
import requests

app = Flask(__name__)
BASE_URL = "https://api.gios.gov.pl/pjp-api/v1"

def fetch_json(url):
    """Pomocnicza funkcja do pobierania danych JSON z API."""
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        return response.json()
    except requests.RequestException:
        return None

@app.route("/")
def index():
    """Wyświetla listę wszystkich stacji wraz z indeksem jakości powietrza."""
    stations = fetch_json(f"{BASE_URL}/station/findAll")
    if not stations:
        abort(500, description="Nie udało się pobrać listy stacji")

    # Pobranie indeksów jakości powietrza dla każdej stacji
    stations_data = []
    for station in stations:
        station_id = station.get("id")
        index_data = fetch_json(f"{BASE_URL}/aqindex/getIndex/{station_id}")
        stations_data.append({
            "id": station_id,
            "stationName": station.get("stationName"),
            "city": station.get("city", {}).get("name"),
            "province": station.get("city", {}).get("province", {}).get("name"),
            "aqIndex": index_data.get("stIndexLevel", {}).get("indexLevelName") if index_data else "Brak danych"
        })

    return render_template("index.html", stations=stations_data)

@app.route("/station/<int:station_id>")
def station_details(station_id):
    """Wyświetla szczegółowe dane dla wybranej stacji."""
    station = fetch_json(f"{BASE_URL}/station/sensors/{station_id}")
    if station is None:
        abort(404, description="Stacja nie istnieje lub brak danych sensorów")

    sensors_data = []
    for sensor in station:
        sensor_id = sensor.get("id")
        sensor_data = fetch_json(f"{BASE_URL}/data/getData/{sensor_id}")
        sensors_data.append({
            "param": sensor.get("param", {}).get("paramName"),
            "values": sensor_data.get("values", []) if sensor_data else []
        })

    index_data = fetch_json(f"{BASE_URL}/aqindex/getIndex/{station_id}")
    aq_index = index_data.get("stIndexLevel", {}).get("indexLevelName") if index_data else "Brak danych"

    return render_template("station.html", station_id=station_id, sensors=sensors_data, aq_index=aq_index)

if __name__ == "__main__":
    app.run(debug=True)
