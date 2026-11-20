
"""Reading CSV files into flight records and error messages."""

import csv
import os

from validator import validate_row, to_record


def parse_files(paths: list[str], airports: set[str]) -> tuple[list[dict], list[str]]:
    """Process CSV files in the given order.

    Returns valid records and validation errors in input order.
    Detects duplicate flights across all supplied files.
    """
    records = []
    errors = []
    seen_flights = set()

    for path in paths:
        filename = os.path.basename(path)
        physical_line = 0

        def data_lines(file):
            nonlocal physical_line

            for line_number, line in enumerate(file, start=1):
                physical_line = line_number

                # The first physical line is always the CSV header.
                if line_number == 1:
                    continue

                stripped = line.strip()

                # Ignore blank lines and comment lines.
                if not stripped or stripped.startswith("#"):
                    continue

                yield line

        with open(path, "r", encoding="utf-8", newline="") as file:
            reader = csv.reader(data_lines(file))

            for fields in reader:
                line_number = physical_line
                fields = [field.strip() for field in fields]

                error = validate_row(fields, airports)

                if error is not None:
                    errors.append(
                        f"{filename}:{line_number}: {error}"
                    )
                    continue

                record = to_record(fields)
                duplicate_key = (
                    record["flight_id"],
                    record["departure_datetime"],
                )

                if duplicate_key in seen_flights:
                    errors.append(
                        f"{filename}:{line_number}: DUPLICATE_FLIGHT"
                    )
                    continue

                seen_flights.add(duplicate_key)
                records.append(record)

    return records, errors
