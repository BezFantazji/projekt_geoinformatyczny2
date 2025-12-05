import requests
from flask import Flask, render_template, abort

app = Flask(__name__)


API_BASE = "https://api.gios.gov.pl/pjp-api/rest"


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/stacje")
def stacje():
    try:
        url = f"{API_BASE}/station/findAll"
        data = requests.get(url, timeout=10).json()
        return render_template("stacje.html", stacje=data)
    except Exception as e:
        return f"Błąd pobierania stacji: {e}"


@app.route("/pomiar/<int:station_id>")
def pomiar(station_id):
    try:
        url = f"{API_BASE}/data/getData/{station_id}"
        data = requests.get(url, timeout=10).json()

        if not data:
            abort(404)

        return render_template("pomiar.html", data=data)
    except Exception as e:
        return f"Błąd pobierania pomiarów: {e}"


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
