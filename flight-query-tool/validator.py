
"""Row validation: airport list loading, single-row checks, record building."""

import math
import re
from datetime import datetime


def load_airports(path: str) -> set[str]:
    airports = set()

    with open(path, "r", encoding="utf-8") as file:
        for line in file:
            code = line.strip()
            if code and not code.startswith("#"):
                airports.add(code)

    return airports


def _valid_datetime(value: str) -> bool:
    if not re.fullmatch(r"\d{4}-\d{2}-\d{2} \d{2}:\d{2}", value):
        return False

    try:
        parsed = datetime.strptime(value, "%Y-%m-%d %H:%M")
        return parsed.strftime("%Y-%m-%d %H:%M") == value
    except ValueError:
        return False


def validate_row(fields: list[str], airports: set[str]) -> str | None:
    if len(fields) != 6:
        return "WRONG_FIELD_COUNT"

    values = [field.strip() for field in fields]

    if any(value == "" for value in values):
        return "MISSING_FIELD"

    flight_id, origin, destination, departure, arrival, price_text = values

    if not re.fullmatch(r"[A-Za-z0-9]{2,8}", flight_id):
        return "INVALID_FLIGHT_ID"

    if not re.fullmatch(r"[A-Z]{3}", origin) or origin not in airports:
        return "INVALID_ORIGIN"

    if not re.fullmatch(r"[A-Z]{3}", destination) or destination not in airports:
        return "INVALID_DESTINATION"

    if origin == destination:
        return "SAME_ORIGIN_DESTINATION"

    if not _valid_datetime(departure):
        return "INVALID_DEPARTURE"

    if not _valid_datetime(arrival):
        return "INVALID_ARRIVAL"

    departure_dt = datetime.strptime(departure, "%Y-%m-%d %H:%M")
    arrival_dt = datetime.strptime(arrival, "%Y-%m-%d %H:%M")

    if arrival_dt <= departure_dt:
        return "ARRIVAL_NOT_AFTER_DEPARTURE"

    try:
        price = float(price_text)
    except ValueError:
        return "INVALID_PRICE"

    if not math.isfinite(price):
        return "INVALID_PRICE"

    if price <= 0:
        return "NON_POSITIVE_PRICE"

    return None


def to_record(fields: list[str]) -> dict:
    values = [field.strip() for field in fields]

    return {
        "flight_id": values[0],
        "origin": values[1],
        "destination": values[2],
        "departure_datetime": values[3],
        "arrival_datetime": values[4],
        "price": float(values[5]),
    }
