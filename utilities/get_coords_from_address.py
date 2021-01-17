"""Use the module to parse the address(in string format) to get the tuple with geographical coordinates
"""

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
        return 0.0, 0.0
    return latitude, longitude
