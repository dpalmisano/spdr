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

import requests
import time


class FetcherException(Exception):
    """Base class for Fetcher exceptions."""

    pass


class PrivateUserException(FetcherException):
    def __init__(self, user_id):
        self.user_id = user_id


class Fetcher:

    baseUrl = "https://api.twitter.com/1.1/friends/ids.json"

    def __init__(self, bearer_token):
        self.headers = {
            "authorization": f"Bearer {bearer_token}",
            "content-type": "application/json",
        }

    def __build_url(self, user_id, cursor):
        return f"{Fetcher.baseUrl}?user_id={user_id}&count=5000&stringify_ids=true&cursor={cursor}"  # noqa

    def fetch(self, user_id):
        cursor = -1
        users = []
        while cursor != 0:
            endpointUrl = self.__build_url(user_id, cursor)
            response = requests.get(endpointUrl, headers=self.headers)
            status_code = response.status_code
            response_json = response.json()

            if status_code == 200:
                cursor = response_json["next_cursor"]
                users.extend(response_json["ids"])
            elif status_code == 401:
                raise PrivateUserException(user_id)
            elif status_code == 429:
                epoch_until_retry = int(response.headers["x-rate-limit-reset"])
                now = int(time.time())
                seconds_until_retry = epoch_until_retry - now
                time.sleep(seconds_until_retry)
            else:
                raise Exception(
                    f"""Error while getting users followed by {user_id}
                        with status code {status_code}"""
                )

        return users
