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

import pytest
from unittest.mock import patch, call

from spdr.writer import Writer


@pytest.fixture
def writer():
    return Writer("/path/to/dir/", "prefix")


@patch("builtins.open")
@patch("os.makedirs")
@patch("os.path.exists")
def test_create_directory(mock_exists, mock_makedirs, mock_open, writer):
    mock_exists.return_value = False

    expected_filepath = writer.write("user-1", [])

    mock_open.assert_called_once_with("/path/to/dir/prefix-user-1.out", "a+")
    assert mock_makedirs.called == True
    assert expected_filepath == "/path/to/dir/prefix-user-1.out"


@patch("builtins.open")
@patch("os.makedirs")
@patch("os.path.exists")
def test_call_write(mock_exists, mock_makedirs, mock_open, writer):
    mock_exists.return_value = True

    expected_filepath = writer.write("user-1", ["user-2", "user-3"])

    mock_fp = mock_open.return_value.__enter__()
    mock_fp.write.assert_has_calls([call("user-2\n"), call("user-3\n")])
