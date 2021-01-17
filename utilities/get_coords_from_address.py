from typing import Tuple

import requests

from config import GEO_API_CONFIG


def get_coords(address: str) -> Tuple[float, float]:
    """
    Taking address and transform it to coordinates using 'positionstack.com' service.
    Detailed info about terms of usage you can find in readme file.
    """
    assert isinstance(
        address, str
    ), f"address '{address}' should be string not {type(address)}"
    url = "http://api.positionstack.com/v1/forward"
    payload = {
        "access_key": GEO_API_CONFIG,
        "query": address.replace(" ", ","),
        "limit": "1",
    }
    r = requests.get(url, params=payload)
    try:
        latitude = float(r.json()["data"][0]["latitude"])
        longitude = float(r.json()["data"][0]["longitude"])
    except (TypeError, IndexError):
        print(r.json())
        return 0.0, 0.0
    return latitude, longitude
