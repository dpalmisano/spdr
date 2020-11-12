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


import os
from setuptools import setup, find_packages


def load_readme():
    path = os.path.join(os.path.dirname(__file__), "README.rst")
    with open(path) as fp:
        content = fp.read()
    return content


setup(
    name="spdr",
    description="Python library for crawling the Twitter user graph.",
    long_description=load_readme(),
    url="",
    author="Davide Palmisano",
    author_email="dpalmisano@gmail.com",
    license="MIT License",
    packages=find_packages(),
    setup_requires=["setuptools_scm"],
    install_requires=["requests", "ratelimit"],
)
