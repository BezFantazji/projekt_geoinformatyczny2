# Dashboard jakości powietrza – projekt_geoinf

Aplikacja webowa umożliwiająca wizualizację danych o jakości powietrza w miastach wojewódzkich w Polsce.  
Dane pochodzą z GIOŚ (plik CSV), przetworzone są do lokalnej bazy SQLite i prezentowane przez interaktywny dashboard.

---

## Technologie

- Python 3.11
- Flask
- SQLite (air.db)
- Chart.js (frontend)
- HTML + CSS (Jinja2 Templates)
- Docker (gotowy obraz)

---

## Struktura projektu

projekt_geoinf/
├── app/
│ ├── app.py # Główna aplikacja Flask
│ ├── config.py # Konfiguracja (opcjonalna)
│ ├── db/
│ │ └── air.db # Baza danych (niewersjonowana)
│ ├── modules/
│ │ ├── queries.py
│ │ ├── excel_loader.py
│ │ └── station_names.py
│ ├── templates/
│ │ └── index.html
│ └── static/
│ └── style.css
├── requirements.txt
├── Dockerfile
├── .gitignore
└── README.md


---

## Jak uruchomić aplikację?

### Opcja 1: Lokalnie (bez Dockera)

#### 1. Utwórz środowisko wirtualne:

```bash
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
