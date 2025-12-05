from flask import Flask, jsonify
import requests

app = Flask(__name__)

BASE_URL = "https://api.gios.gov.pl/pjp-api/rest"

@app.route("/")
def index():
    return "Działa! Sprawdź /stacje lub /pomiar/ID"

@app.route("/stacje")
def stacje():
    r = requests.get(f"{BASE_URL}/station/findAll")
    return jsonify(r.json())

@app.route("/pomiar/<int:id>")
def pomiar(id):
    r = requests.get(f"{BASE_URL}/data/getData/{id}")
    return jsonify(r.json())

@app.route("/index/<int:id>")
def indexJakosci(id):
    r = requests.get(f"{BASE_URL}/aqindex/getIndex/{id}")
    return jsonify(r.json())

if __name__ == "__main__":
    app.run()
