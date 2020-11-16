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


def chunk(user_ids):
    """Chunk array of user ids"""
    for i in range(0, len(user_ids), 100):
        yield user_ids[i:i + 10]


class FetcherException(Exception):
    """Base class for Fetcher exceptions."""
    pass


class PrivateUserException(FetcherException):
    def __init__(self, user_id):
        self.user_id = user_id


class UserNotFoundException(FetcherException):
    def __init__(self, user_id):
        self.user_id = user_id


class Fetcher:
    
    baseUrl = "https://api.twitter.com"

    getFriendsUrl = f"{baseUrl}/1.1/friends/ids.json"
    
    userLookupUrl = f"{baseUrl}/2/users"

    def __init__(self, bearer_token, expand = False):
        self.headers = {
            "authorization": f"Bearer {bearer_token}",
            "content-type": "application/json",
        }
        self.expand = expand

    def __build_get_friends_url(self, user_id, cursor):
        return f"{Fetcher.getFriendsUrl}?user_id={user_id}&count=5000&stringify_ids=true&cursor={cursor}"  # noqa
    
    def __build_lookup_users(self, user_ids):
        user_ids_str = ','.join(user_ids)
        return f"{Fetcher.userLookupUrl}?ids={user_ids_str}"
    
    def __slice_response(self, response):
        return (
            response.status_code,
            response.json(),
            response.headers
        )

    
    def __fetch_friends(self, user_id, cursor):
        getFriendsEndpoint = self.__build_get_friends_url(user_id, cursor)
        response = requests.get(getFriendsEndpoint, headers=self.headers)
        return self.__slice_response(response)

    
    def __fetch_users(self, user_id):
        userLookupEndpoint = self.__build_get_user(user_id)
        response = requests.get(userLookupEndpoint, headers=self.headers)
        return self.__slice_response(response)
    
    def __wait_until(self, epoch_until_retry):
        now = int(time.time())
        seconds_until_retry = epoch_until_retry - now
        time.sleep(seconds_until_retry)
    
    
    def __handle_error(self, user_id, status_code, response_json, headers = None):
        if status_code == 401:
            raise PrivateUserException(user_id)
        elif status_code == 429:
            epoch_until_retry = int(headers["x-rate-limit-reset"])
            self.__wait_until(epoch_until_retry)
        elif status_code == 409:
            raise UserNotFoundException(user_id)
        else:
           raise Exception(
                f"""Error while getting users followed by {user_id}
                    with status code {status_code}"""
            )


    def __expand_user_ids(self, user_ids):
        expanded_users = []
        for user_ids_chunk in chunk(user_ids):
            status_code, response_json, headers = self.__fetch_user(user_ids_chunk)
            if status_code == 200:
                expanded_users.extend(response_json['data'])
            else:
                self.__handle_error(None, status_code, response_json, headers)

        return expanded_users


    def fetch(self, user_id):
        cursor = -1
        users = []
        while cursor != 0:
            status_code, response_json, headers = self.__fetch_friends(user_id, cursor)
            if status_code == 200:
                cursor = response_json["next_cursor"]
                friends_ids = response_json["ids"]
                users.extend(
                    self.__expand_user_ids(friends_ids) if self.expand is True else friends_ids
                )
            else:
                self.__handle_error(user_id, status_code, response_json, headers)

        return users
