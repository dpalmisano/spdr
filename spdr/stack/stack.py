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
# SOFTWARE.

from collections import deque

"""
Stack to keep ids to be explored.
"""


class Stack:
    def __init__(self, initial_user_id=None):
        self.cache = set()
        if initial_user_id is not None:
            self.stack = deque([initial_user_id])
        else:
            self.stack = deque()

    def pop(self):
        try:
            user_id = self.stack.pop()
            self.cache.add(user_id)
            return user_id
        except IndexError:
            return None

    def push(self, user_id):
        if user_id not in self.cache:
            self.stack.append(user_id)

    def contains(self, user_id):
        return user_id in self.stack

    def is_candidate(self, user_id):
        return user_id not in self.cache and self.contains(user_id) == False
