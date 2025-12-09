import csv
import sqlite3
import os

BASE_DIR = os.path.dirname(os.path.dirname(__file__))
DB_PATH = os.path.join(BASE_DIR, "db", "air.db")
CSV_PATH = os.path.join(BASE_DIR, "data", "gios.csv")


def load_csv():
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()

    with open(CSV_PATH, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)

        for row in reader:
            cur.execute(
                """
                INSERT INTO measurements (station_code, date, hour, pollutant, value)
                VALUES (?, ?, ?, ?, ?)
                """,
                (
                    row["kod_stacji"],
                    row["data_pomiaru"],
                    int(row["godzina"]),
                    row["parametr"],
                    float(row["wartosc"])
                )
            )

    conn.commit()
    conn.close()


if __name__ == "__main__":
    load_csv()
