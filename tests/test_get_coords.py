from unittest.mock import MagicMock, PropertyMock

import pytest
import requests

from utilities import get_coords


def test_the_invalid_API_except_output(monkeypatch):
    mock = MagicMock(return_value=requests.models.Response)
    pock = PropertyMock(return_value=401)
    monkeypatch.setattr(requests.models.Response, "json", MagicMock(return_value=""))
    monkeypatch.setattr(requests, "get", mock)
    requests.get("smth.com").status_code = pock
    with pytest.raises(
        ConnectionRefusedError, match="An invalid API access key was supplied."
    ):
        get_coords("smth.com")


def test_the_reached_limit_except_output(monkeypatch):
    mock = MagicMock(return_value=requests.models.Response)
    pock = PropertyMock(return_value=429)
    monkeypatch.setattr(requests.models.Response, "json", MagicMock(return_value=""))
    monkeypatch.setattr(requests, "get", mock)
    requests.get("smth.com").status_code = pock
    with pytest.raises(
        ConnectionRefusedError,
        match="The given user account has reached its monthly allowed request volume.",
    ):
        get_coords("smth.com")


def test_output(monkeypatch):
    mock = MagicMock(return_value=requests.models.Response)
    pock = PropertyMock(return_value=200)
    data = {"data": [{"latitude": 40.68295, "longitude": -73.9708}]}
    monkeypatch.setattr(requests, "get", mock)
    requests.get("Moscow Russia").status_code = pock
    monkeypatch.setattr(requests.models.Response, "json", MagicMock(return_value=data))
    assert get_coords("Moscow Russia") == (40.68295, -73.9708)


def test_failed_output(monkeypatch):
    mock = MagicMock(return_value=requests.models.Response)
    pock = PropertyMock(return_value=200)
    data = {"data": [[], []]}
    monkeypatch.setattr(requests, "get", mock)
    requests.get("Moscow Russia").status_code = pock
    monkeypatch.setattr(requests.models.Response, "json", MagicMock(return_value=data))
    assert get_coords("Moscow Russia") == (None, None)
