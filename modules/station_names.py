CITY_DEFS = {
    "Wrocław": ["wroc", "bart", "wro"],
    "Bydgoszcz": ["byd", "pozna"],
    "Toruń": ["toru"],
    "Lublin": ["lubl"],
    "Zielona Góra": ["ziel"],
    "Łódź": ["lodz"],
    "Kraków": ["krak"],
    "Warszawa": ["wars", "wola", "waw"],
    "Opole": ["opol"],
    "Rzeszów": ["rzes"],
    "Białystok": ["bial"],
    "Gdańsk": ["gdan"],
    "Katowice": ["kato", "kat"],
    "Kielce": ["kiel"],
    "Olsztyn": ["olsz"],
    "Poznań": ["pozn"],
    "Szczecin": ["szcz"],
    "Gorzów Wlkp.": ["gorz"]
}

def station_to_city(station):
    s = station.lower()
    for city, keys in CITY_DEFS.items():
        for k in keys:
            if k in s:
                return city
    return station  # fallback
