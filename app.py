import requests
from flask import Flask, render_template

app = Flask(__name__)

GIOS_STATIONS_URL = "https://api.gios.gov.pl/pjp-api/rest/station/findAll"
GIOS_INDEX_URL = "https://api.gios.gov.pl/pjp-api/rest/aqindex/getIndex/{}"

@app.route("/")
def home():
    # pobieramy listę stacji
    stations = requests.get(GIOS_STATIONS_URL).json()

    data = []
    for st in stations[:50]:  # 50 pierwszych stacji – szybciej
        idx = requests.get(GIOS_INDEX_URL.format(st["id"])).json()

        data.append({
            "city": st.get("city", {}).get("name", "Brak"),
            "station": st["stationName"],
            "pm10": idx.get("pm10IndexLevel", {}).get("indexLevelName"),
            "pm25": idx.get("pm25IndexLevel", {}).get("indexLevelName"),
            "overall": idx.get("stIndexLevel", {}).get("indexLevelName"),
        })

    return render_template("index.html", data=data)

if __name__ == "__main__":
    app.run()
