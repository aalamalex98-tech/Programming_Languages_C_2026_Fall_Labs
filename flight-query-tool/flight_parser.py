
"""Flight Schedule Parser and Query Tool - command-line entry point."""

import argparse
import json
import logging
import os
import sys
from datetime import datetime

from validator import load_airports
from csv_loader import parse_files
from query import run_queries


STUDENT_ID = "251ADB029"
FIRST_NAME = "Alex"
LAST_NAME = "Aalam"


def main(argv: list[str] | None = None) -> int:
    """Run the program and return exit code 0, 1 or 2."""

    parser = argparse.ArgumentParser(
        description="Flight Schedule Parser and Query Tool"
    )

    source = parser.add_mutually_exclusive_group(required=True)
    source.add_argument("-i", metavar="FILE", help="Parse one CSV file")
    source.add_argument("-d", metavar="FOLDER", help="Parse CSV files in a folder")
    source.add_argument("-j", metavar="FILE", help="Load an existing JSON database")

    parser.add_argument("-a", metavar="FILE", help="Airport list file")
    parser.add_argument("-o", metavar="FILE", help="Output database JSON file")
    parser.add_argument("-q", metavar="FILE", help="Query JSON file")
    parser.add_argument("-r", metavar="FOLDER", default=".",
                        help="Folder for the query response file")

    args = parser.parse_args(argv)

    # Check combinations of command-line arguments.
    if (args.i or args.d) and not args.a:
        parser.error("-a is required with -i or -d")

    if args.j and args.o:
        parser.error("-o cannot be used with -j")

    logger = logging.getLogger("flight_parser")
    handler = None

    try:
        # Load or create the flight database.
        if args.j:
            with open(args.j, "r", encoding="utf-8") as file:
                db = json.load(file)

            if not isinstance(db, list) or not all(
                isinstance(record, dict) for record in db
            ):
                raise ValueError("JSON database must be an array of objects")

        else:
            airports = load_airports(args.a)

            if args.i:
                paths = [args.i]
            else:
                if not os.path.isdir(args.d):
                    raise ValueError(f"Not a folder: {args.d}")

                paths = sorted(
                    os.path.join(args.d, name)
                    for name in os.listdir(args.d)
                    if name.lower().endswith(".csv")
                    and os.path.isfile(os.path.join(args.d, name))
                )

                if not paths:
                    raise ValueError("No CSV files found in the folder")

            db, errors = parse_files(paths, airports)

            output_path = args.o if args.o else "db.json"
            output_folder = os.path.dirname(os.path.abspath(output_path))
            log_path = os.path.join(output_folder, "errors.log")

            # Write the database.
            with open(output_path, "w", encoding="utf-8") as file:
                json.dump(db, file, indent=2, ensure_ascii=False)
                file.write("\n")

            # Write validation errors using the logging module.
            logger.setLevel(logging.INFO)
            logger.propagate = False

            handler = logging.FileHandler(
                log_path, mode="w", encoding="utf-8"
            )
            formatter = logging.Formatter(
                "%(asctime)s %(levelname)s %(message)s",
                datefmt="%Y-%m-%d %H:%M:%S",
            )
            handler.setFormatter(formatter)
            logger.addHandler(handler)

            for error in errors:
                logger.warning("%s", error)

            handler.flush()

        # Process queries if a query file was supplied.
        if args.q:
            with open(args.q, "r", encoding="utf-8") as file:
                queries = json.load(file)

            if isinstance(queries, dict):
                pass
            elif isinstance(queries, list) and all(
                isinstance(query, dict) for query in queries
            ):
                pass
            else:
                raise ValueError(
                    "Query file must contain an object or an array of objects"
                )

            if not os.path.isdir(args.r):
                raise ValueError(f"Response folder does not exist: {args.r}")

            responses = run_queries(db, queries)

            timestamp = datetime.now().strftime("%Y%m%d_%H%M")
            response_name = (
                f"response_{STUDENT_ID}_{FIRST_NAME}_{LAST_NAME}_{timestamp}.json"
            )
            response_path = os.path.join(args.r, response_name)

            with open(response_path, "w", encoding="utf-8") as file:
                json.dump(responses, file, indent=2, ensure_ascii=False)
                file.write("\n")

        return 0

    except (OSError, ValueError, json.JSONDecodeError) as error:
        print(f"Error: {error}", file=sys.stderr)
        return 1

    finally:
        if handler is not None:
            logger.removeHandler(handler)
            handler.close()


if __name__ == "__main__":
    sys.exit(main())
