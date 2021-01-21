import argparse
import json
from pathlib import Path
from typing import Set, Tuple

import requests


def args_parse(args):
    """
    Used to set the arguments for the app. Run it from console:
    python main.py -p path to csv.files [addition path ...] -t [amount of threads to run with]
    """
    parser = argparse.ArgumentParser(
        description="Parser for files' path and threads amount"
    )
    parser.add_argument(
        "-p", "--path", nargs="+", help='set the path to the folder with "*.csv" files'
    )
    parser.add_argument(
        "-t",
        "--threads",
        nargs="?",
        const="threads",
        default=1,
        help="set the number of threads for the script",
        type=int,
    )
    return parser.parse_args(args)


def collect_and_check_files(list_of_paths) -> Set[Path]:
    """
    Checking if the files are present on the path from your input and giving collection of files
    """
    files_to_read = set()
    for path in list_of_paths:
        files_to_read.update(set(Path(path).glob("**/*.csv")))
    if not files_to_read:
        raise FileNotFoundError("Your path has no csv files. Please set another path")
    return files_to_read


def get_coords(address: str) -> Tuple:
    """
    Taking address and transform it to coordinates using 'positionstack.com' service.
    Detailed info about terms of usage you can find in readme file.
    """
    with open("config.json") as json_file:
        key = json.load(json_file)["API_KEY"]
    url = "http://api.positionstack.com/v1/forward"
    payload = {
        "access_key": key,
        "query": address.replace(" ", ","),
        "limit": "1",
    }
    r = requests.get(url, params=payload)
    if r.status_code == 429:
        raise ConnectionRefusedError(
            "The given user account has reached its monthly allowed request volume."
        )
    elif r.status_code == 401:
        raise ConnectionRefusedError("An invalid API access key was supplied.")
    try:
        latitude = float(r.json()["data"][0]["latitude"])
        longitude = float(r.json()["data"][0]["longitude"])
    except (TypeError, IndexError):
        return None, None
    return latitude, longitude
