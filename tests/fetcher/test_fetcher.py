# MIT License

# Copyright (c) 2020 Davide Palmisano

# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:

# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.

# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

import pytest
from pytest import raises
from unittest.mock import patch, call

import time

from spdr.fetcher import Fetcher, PrivateUserException

token = "test-bearer-token"
baseUrl = "https://api.twitter.com/1.1/friends/ids.json"

expected_headers = {
    "authorization": f"Bearer {token}",
    "content-type": "application/json",
}


class MockResponse:
    def __init__(self, status_code, cursor, ids, x_rate_limit_reset=None):
        self.status_code = status_code
        self.cursor = cursor
        self.ids = ids
        self.headers = {"x-rate-limit-reset": x_rate_limit_reset}

    def json(self):
        return {"next_cursor": self.cursor, "ids": self.ids}


def build_url(user_id, cursor):
    # fmt: off
    return (
        f"{baseUrl}?user_id={user_id}&count=5000&stringify_ids=true&cursor={cursor}" # noqa
    )
    # fmt: on


@pytest.fixture
def fetcher():
    return Fetcher(token)


@patch("requests.get")
def test_build_url(mock_requests_get, fetcher):
    mock_response = MockResponse(200, 0, ["user-1", "user-2"])
    mock_requests_get.return_value = mock_response

    actual_users = fetcher.fetch("user-id")

    expected_url = build_url("user-id", -1)

    mock_requests_get.assert_called_once_with(
        expected_url, headers=expected_headers
    )  # noqa
    assert actual_users == ["user-1", "user-2"]


mock_responses = [
    MockResponse(200, 1, ["user-1", "user-2"]),
    MockResponse(200, 0, ["user-3", "user-4"]),
]


@patch("requests.get", side_effect=mock_responses)
def test_cursor(mock_requests_get, fetcher):
    actual_users = fetcher.fetch("user-id")

    mock_requests_get.assert_has_calls(
        [
            call(build_url("user-id", -1), headers=expected_headers),
            call(build_url("user-id", 1), headers=expected_headers),
        ]
    )
    assert actual_users == ["user-1", "user-2", "user-3", "user-4"]


@patch("requests.get")
def test_handle_private_user(mock_requests_get, fetcher):
    mock_response = MockResponse(401, 0, ["user-1", "user-2"])
    mock_requests_get.return_value = mock_response

    with raises(PrivateUserException) as pue:
        actual_users = fetcher.fetch("user-id")
        assert pue.user_id == "user-id"
        assert actual_users == ["user-1", "user-2"]


@patch("time.sleep")
@patch("requests.get")
def test_handle_too_many_requests(mock_requests_get, mock_time_sleep, fetcher):
    time_until_retry = int(time.time()) + 500
    mock_responses = [
        MockResponse(429, 1, ["user-3"], time_until_retry),
        MockResponse(200, 0, ["user-3"]),
    ]
    mock_requests_get.side_effect = mock_responses

    actual_users = fetcher.fetch("user-id")

    mock_time_sleep.assert_called_once_with(500)

    mock_requests_get.assert_has_calls(
        [call(build_url("user-id", -1), headers=expected_headers)]
    )
    assert actual_users == ["user-3"]
