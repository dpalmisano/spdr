# MIT License

# Copyright (c) 2020 Davide Palmisano

# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:

# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.

# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE

import requests
from ratelimit import limits, sleep_and_retry, RateLimitException

from spdr.fetcher import PrivateUserException

TIME_PERIOD = 900  # 15 minutes


class Spdr:
    @sleep_and_retry
    @limits(calls=15, period=TIME_PERIOD)
    def __fetch_following(self, current_id):
        print(f"Fetching users followed by {current_id}")
        try:
            return self.fetcher.fetch(current_id)
        except PrivateUserException as pue:
            print(f"User {pue.user_id} is private. Skipping.")
            return None

    def __save(self, following, current_id):
        output_file = self.writer.write(current_id, following)
        print(f"Users following {current_id} written to {output_file}")

    def __push_to_stack(self, following):
        for user_id in following:
            if self.stack.is_candidate(user_id):
                self.stack.push(user_id)

    def __init__(self, stack, fetcher, writer):
        self.stack = stack
        self.writer = writer
        self.fetcher = fetcher

    def start(self, max_depth=1):
        current_id = self.stack.pop()

        while current_id is not None:
            following = self.__fetch_following(current_id)
            if following is not None:
                self.__save(following, current_id)
                self.__push_to_stack(following)

            current_id = self.stack.pop()
