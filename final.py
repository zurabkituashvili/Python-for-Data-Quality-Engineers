import math
import sqlite3
from typing import Tuple, Optional


DB_PATH = "cities.db"
EARTH_RADIUS_KM = 6371.0088


def init_db(db_path: str = DB_PATH) -> None:
    with sqlite3.connect(db_path) as conn:
        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS cities (
                name TEXT PRIMARY KEY,
                latitude REAL NOT NULL,
                longitude REAL NOT NULL
            )
            """
        )
        conn.commit()


def normalize_city_name(city_name: str) -> str:
    return city_name.strip().lower()


def get_city_coordinates(
    city_name: str, db_path: str = DB_PATH
) -> Optional[Tuple[float, float]]:
    normalized_name = normalize_city_name(city_name)

    with sqlite3.connect(db_path) as conn:
        cursor = conn.execute(
            "SELECT latitude, longitude FROM cities WHERE name = ?",
            (normalized_name,),
        )
        row = cursor.fetchone()

    if row is None:
        return None

    return row[0], row[1]


def save_city_coordinates(
    city_name: str, latitude: float, longitude: float, db_path: str = DB_PATH
) -> None:
    normalized_name = normalize_city_name(city_name)

    with sqlite3.connect(db_path) as conn:
        conn.execute(
            """
            INSERT INTO cities (name, latitude, longitude)
            VALUES (?, ?, ?)
            ON CONFLICT(name) DO UPDATE SET
                latitude = excluded.latitude,
                longitude = excluded.longitude
            """,
            (normalized_name, latitude, longitude),
        )
        conn.commit()


def ask_for_coordinates(city_name: str) -> Tuple[float, float]:
    print(f"Coordinates for '{city_name}' were not found.")
    print("Please enter them in decimal degrees.")
    print("Examples: latitude 41.7151, longitude 44.8271")

    while True:
        try:
            latitude = float(input(f"Latitude for {city_name}: ").strip())
            longitude = float(input(f"Longitude for {city_name}: ").strip())

            if not (-90 <= latitude <= 90):
                print("Latitude must be between -90 and 90.")
                continue

            if not (-180 <= longitude <= 180):
                print("Longitude must be between -180 and 180.")
                continue

            return latitude, longitude

        except ValueError:
            print("Invalid input. Please enter numeric values.")


def get_or_create_city_coordinates(
    city_name: str, db_path: str = DB_PATH
) -> Tuple[float, float]:
    coords = get_city_coordinates(city_name, db_path)
    if coords is not None:
        return coords

    latitude, longitude = ask_for_coordinates(city_name)
    save_city_coordinates(city_name, latitude, longitude, db_path)
    return latitude, longitude


def haversine_distance_km(
    lat1: float,
    lon1: float,
    lat2: float,
    lon2: float,
) -> float:

    lat1_rad = math.radians(lat1)
    lon1_rad = math.radians(lon1)
    lat2_rad = math.radians(lat2)
    lon2_rad = math.radians(lon2)

    delta_lat = lat2_rad - lat1_rad
    delta_lon = lon2_rad - lon1_rad

    a = (
        math.sin(delta_lat / 2) ** 2
        + math.cos(lat1_rad) * math.cos(lat2_rad) * math.sin(delta_lon / 2) ** 2
    )
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))

    return EARTH_RADIUS_KM * c


def main() -> None:
    init_db()

    print("City distance calculator")
    print(
        "Distances are calculated along Earth's surface using the Haversine formula.\n"
    )

    city1 = input("Enter the first city name: ").strip()
    city2 = input("Enter the second city name: ").strip()

    if not city1 or not city2:
        print("City names cannot be empty.")
        return

    lat1, lon1 = get_or_create_city_coordinates(city1)
    lat2, lon2 = get_or_create_city_coordinates(city2)

    distance = haversine_distance_km(lat1, lon1, lat2, lon2)

    print(f"\nDistance between {city1} and {city2}: {distance:.2f} km")


if __name__ == "__main__":
    main()
