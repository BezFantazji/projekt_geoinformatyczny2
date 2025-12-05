import os
import time
from flask import Flask, render_template, request, jsonify
import requests
from cachetools import TTLCache, cached

app = Flask(__name__)

# Base URLs - spróbujemy najpierw wersji v1, a jeżeli zwróci HTML/nie JSON -> spróbujemy starej
GIOS_BASES = [
    "https://api.gios.gov.pl/pjp-api/v1/rest",
    "https://api.gios.gov.pl/pjp-api/rest"
]

# krótkie cache w pamięci: cache 300s, max 100 itemów
cache = TTLCache(maxsize=100, ttl=300)

REQUEST_TIMEOUT = 8  # sekundy na request do GIOS

def try_get(path):
    """
    Try to GET JSON from a list of base URLs. If a response is not JSON (HTML/info page),
    try the next base. Returns parsed JSON or raises requests.HTTPError/ValueError.
    """
    headers = {"Accept": "application/json"}
    last_err = None
    for base in GIOS_BASES:
        url = f"{base}/{path.lstrip('/')}"
        try:
            r = requests.get(url, headers=headers, timeout=REQUEST_TIMEOUT)
        except Exception as e:
            last_err = e
            continue
        # Some endpoints sometimes return an HTML page with message that service moved.
        content_type = r.headers.get("Content-Type", "")
        if r.status_code != 200:
            last_err = requests.HTTPError(f"{r.status_code} from {url}: {r.text[:200]}")
            continue
        # if JSON-like
        if "application/json" in content_type or r.text.strip().startswith(("{","[")):
            try:
                return r.json()
            except ValueError as e:
                # invalid json
                last_err = e
                continue
        else:
            # not JSON (HTML info) -> try next base
            last_err = ValueError(f"Not JSON response from {url}: {content_type}")
            continue
    # if got here, none worked
    raise last_err if last_err is not None else ValueError("No successful response")

# CACHED wrapper
@cached(cache)
def get_all_stations():
    # endpoint historically: station/findAll
    data = try_get("station/findAll")
    # normalize: data could be dict with 'stations' or list
    if isinstance(data, dict) and "stations" in data:
        return data["stations"]
    if isinstance(data, list):
        return data
    # fallback
    return list(data)

@cached(cache)
def get_station(station_id):
    return try_get(f"station/{station_id}")

@cached(cache)
def get_station_sensors(station_id):
    return try_get(f"station/sensors/{station_id}")

@cached(cache)
def get_sensor_data(sensor_id):
    return try_get(f"data/getData/{sensor_id}")

@cached(cache)
def get_index_for_station(station_id):
    # aqindex endpoint historically: aqindex/getIndex/{stationId}
    try:
        return try_get(f"aqindex/getIndex/{station_id}")
    except Exception:
        # some API variants may expose index under another path - ignore gracefully
        return None

@app.route("/")
def index():
    try:
        stations = get_all_stations()
    except Exception as e:
        # pokaż użytkownikowi czytelny komunikat
        stations = []
        fetch_error = str(e)
        return render_template("index.html", stations=stations, fetch_error=fetch_error)

    # przygotuj minimalny listę {id,stationName,city}
    simple = []
    for s in stations:
        # różne wersje API mogą używać slightly different field names
        sid = s.get("id") or s.get("stationId") or s.get("stId") or s.get("id_stacji")
        name = s.get("stationName") or s.get("name") or s.get("station") or s.get("stationName")
        city = None
        # try nested address or city
        if "city" in s and isinstance(s["city"], dict):
            city = s["city"].get("name")
        city = city or s.get("cityName") or s.get("addressStreet")
        simple.append({"id": sid, "name": name, "city": city})
    # sortowanie proste
    simple = sorted([x for x in simple if x["id"] is not None], key=lambda x: (x["city"] or "", x["name"] or ""))
    return render_template("index.html", stations=simple, fetch_error=None)

@app.route("/station/<int:station_id>")
def station_view(station_id):
    # Pobierz info o stacji, sensory, index, i dane dla każdego sensora
    try:
        station = get_station(station_id)
    except Exception as e:
        return render_template("station.html", error=f"Błąd pobierania stacji: {e}")

    try:
        sensors = get_station_sensors(station_id)
    except Exception as e:
        sensors = []
        sensor_error = f"Błąd pobierania sensorów: {e}"
    else:
        sensor_error = None

    # sensors might be list of dict {id, sensorName, param: {paramName,...}}
    readings = []
    for s in (sensors or []):
        sid = s.get("id") or s.get("sensorId")
        if sid is None:
            continue
        # fetch last data for sensor
        try:
            data = get_sensor_data(sid)
            # API returns list of measurements with fields 'date' and 'value'
            if isinstance(data, list) and len(data) > 0:
                latest = data[0]  # usually newest first
                value = latest.get("value")
                date = latest.get("date") or latest.get("Date")
            else:
                value = None
                date = None
        except Exception as e:
            value = None
            date = None
        param = s.get("param") or s.get("parameter") or {}
        param_name = param.get("paramName") or param.get("name") or param.get("code") or "unknown"
        readings.append({
            "sensor_id": sid,
            "param": param_name,
            "value": value,
            "date": date,
            "sensor_info": s
        })

    # AQ index
    try:
        index = get_index_for_station(station_id)
    except Exception:
        index = None

    return render_template("station.html",
                           station=station,
                           readings=readings,
                           sensor_error=sensor_error,
                           index=index)

# Lightweight API endpoints (JSON) for AJAX if you want client-side rendering
@app.route("/api/stations")
def api_stations():
    try:
        stations = get_all_stations()
        return jsonify({"ok": True, "stations": stations})
    except Exception as e:
        return jsonify({"ok": False, "error": str(e)}), 500

@app.route("/api/station/<int:station_id>")
def api_station(station_id):
    try:
        station = get_station(station_id)
        sensors = get_station_sensors(station_id)
        readings = []
        for s in sensors:
            sid = s.get("id")
            if sid is None:
                continue
            try:
                data = get_sensor_data(sid)
            except Exception:
                data = []
            readings.append({"sensor": s, "data": data})
        idx = None
        try:
            idx = get_index_for_station(station_id)
        except Exception:
            idx = None
        return jsonify({"ok": True, "station": station, "sensors": readings, "index": idx})
    except Exception as e:
        return jsonify({"ok": False, "error": str(e)}), 500


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8000))
    app.run(host="0.0.0.0", port=port)
