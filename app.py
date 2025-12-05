# app.py
from flask import Flask, render_template
import requests

app = Flask(__name__)

BASE_URL = "https://api.gios.gov.pl/pjp-api/v1/rest"

def get_stations():
    try:
        resp = requests.get(f"{BASE_URL}/station/findAll", params={"page":1, "size":500}, timeout=10)
        resp.raise_for_status()
        data = resp.json()
        # Jeśli API opakowuje dane inaczej — np. pod kluczem "data" lub "results"
        if isinstance(data, list):
            return data
        # jeśli to dict z kluczem 'data' albo 'results', rozpakuj
        if isinstance(data, dict):
            for key in ("data", "results", "stations"):
                if key in data and isinstance(data[key], list):
                    return data[key]
        return []
    except Exception as e:
        print("Błąd pobierania stacji:", e)
        return []


def get_sensors(station_id):
    """Pobierz listę sensorów dla danej stacji."""
    try:
        resp = requests.get(f"{BASE_URL}/station/sensors/{station_id}", timeout=10)
        resp.raise_for_status()
        data = resp.json()
        if isinstance(data, list):
            return data
        else:
            return []
    except Exception as e:
        print(f"Błąd pobierania sensorów dla stacji {station_id}:", e)
        return []

def get_latest_measurements(sensor_id):
    """Pobierz najnowsze dane pomiarowe dla sensora."""
    try:
        resp = requests.get(f"{BASE_URL}/data/getData/{sensor_id}", timeout=10)
        resp.raise_for_status()
        data = resp.json()
        # oczekujemy klucza "values" zawierającego listę pomiarów
        values = data.get("values")
        if isinstance(values, list) and values:
            # zwracamy pierwszy element (najświeższy)
            return values[0]
        else:
            return None
    except Exception as e:
        print(f"Błąd pobierania danych dla sensora {sensor_id}:", e)
        return None

@app.route("/")
def index():
    stations = get_stations()
    # upewnij się, że masz listę
    if not isinstance(stations, list):
        stations = []

    stations_data = []
    for station in stations:
        station_id = station.get("id")
        name = station.get("stationName")
        city = station.get("city", {}).get("name")
        if station_id is None or name is None or city is None:
            continue

        # pobierz sensory
        sensors = get_sensors(station_id)
        measurements = []
        for s in sensors:
            param = s.get("param", {}).get("paramName")
            sensor_id = s.get("id")
            if param and sensor_id:
                m = get_latest_measurements(sensor_id)
                if m and m.get("value") is not None:
                    measurements.append({
                        "param": param,
                        "value": m.get("value"),
                        "date": m.get("date")
                    })
        stations_data.append({
            "id": station_id,
            "name": name,
            "city": city,
            "measurements": measurements
        })

    return render_template("index.html", stations=stations_data)

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)
