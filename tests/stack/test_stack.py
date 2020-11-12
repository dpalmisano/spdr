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

from spdr.stack import Stack

initial_user_id = "initial_user_id"


@pytest.fixture
def get_stack():
    return Stack(initial_user_id)


def test_constructor(get_stack):
    assert get_stack.contains(initial_user_id) is True


def test_pop(get_stack):
    user_id = get_stack.pop()
    assert user_id == initial_user_id


def test_push(get_stack):
    new_user_id = "new_user_id"
    assert get_stack.contains(new_user_id) is False
    get_stack.push(new_user_id)
    assert get_stack.contains(new_user_id) is True


def test_is_candidate(get_stack):
    new_user_id = "new_user_id"
    assert get_stack.is_candidate(new_user_id) is True
    get_stack.push(new_user_id)
    assert get_stack.is_candidate(new_user_id) is False
    get_stack.pop()
    assert get_stack.is_candidate(new_user_id) is False
