
"""Running queries against the flight database."""

import math
import re
from datetime import datetime


VALID_FIELDS = {
    "flight_id",
    "origin",
    "destination",
    "departure_datetime",
    "arrival_datetime",
    "price",
}

STRING_FILTERS = {"flight_id", "origin", "destination"}


def _valid_datetime(value: str) -> bool:
    """Check that a datetime uses the exact required format."""
    if not re.fullmatch(r"\d{4}-\d{2}-\d{2} \d{2}:\d{2}", value):
        return False

    try:
        parsed = datetime.strptime(value, "%Y-%m-%d %H:%M")
        return parsed.strftime("%Y-%m-%d %H:%M") == value
    except ValueError:
        return False


def _valid_query(query: dict) -> bool:
    """Check query keys and values before filtering."""
    if not isinstance(query, dict):
        return False

    allowed_keys = VALID_FIELDS | {
        "min_price",
        "sort_by",
        "order",
        "limit",
    }

    if not set(query).issubset(allowed_keys):
        return False

    for key in STRING_FILTERS:
        if key in query and not isinstance(query[key], str):
            return False

    for key in ("departure_datetime", "arrival_datetime"):
        if key in query:
            if not isinstance(query[key], str):
                return False
            if not _valid_datetime(query[key]):
                return False

    for key in ("price", "min_price"):
        if key in query:
            value = query[key]
            if isinstance(value, bool) or not isinstance(value, (int, float)):
                return False
            if not math.isfinite(value):
                return False

    if "sort_by" in query:
        if not isinstance(query["sort_by"], str):
            return False
        if query["sort_by"] not in VALID_FIELDS:
            return False

    if "order" in query:
        if "sort_by" not in query:
            return False
        if query["order"] not in ("asc", "desc"):
            return False

    if "limit" in query:
        limit = query["limit"]
        if isinstance(limit, bool) or not isinstance(limit, int):
            return False
        if limit < 0:
            return False

    return True


def run_query(db: list[dict], query: dict) -> dict:
    """Return matching records for one query object."""
    if not _valid_query(query):
        return {
            "query": query,
            "error": "INVALID_QUERY",
            "matches": [],
        }

    matches = []

    for flight in db:
        # Exact string matches.
        if "flight_id" in query:
            if flight["flight_id"] != query["flight_id"]:
                continue

        if "origin" in query:
            if flight["origin"] != query["origin"]:
                continue

        if "destination" in query:
            if flight["destination"] != query["destination"]:
                continue

        # Departure must be on or after the requested datetime.
        if "departure_datetime" in query:
            if flight["departure_datetime"] < query["departure_datetime"]:
                continue

        # Arrival must be on or before the requested datetime.
        if "arrival_datetime" in query:
            if flight["arrival_datetime"] > query["arrival_datetime"]:
                continue

        # Maximum price.
        if "price" in query:
            if flight["price"] > query["price"]:
                continue

        # Minimum price.
        if "min_price" in query:
            if flight["price"] < query["min_price"]:
                continue

        matches.append(flight)

    # Stable sorting, preserving database order for equal values.
    if "sort_by" in query:
        reverse = query.get("order", "asc") == "desc"
        matches.sort(
            key=lambda flight: flight[query["sort_by"]],
            reverse=reverse,
        )

    # Apply the limit after sorting.
    if "limit" in query:
        matches = matches[:query["limit"]]

    return {
        "query": query,
        "matches": matches,
    }


def run_queries(db: list[dict], queries: dict | list) -> list[dict]:
    """Accept one query object or a list of query objects."""
    if isinstance(queries, dict):
        queries = [queries]

    if not isinstance(queries, list):
        return [
            {
                "query": queries,
                "error": "INVALID_QUERY",
                "matches": [],
            }
        ]

    return [run_query(db, query) for query in queries]
