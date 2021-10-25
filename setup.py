# coding: utf-8

# Copyright 2021 GADG <https://github.com/MinisterioPublicoRJ/leis-brasileiras/>

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
#
from __future__ import unicode_literals
from os import path

from setuptools import find_packages, setup

__version__ = '0.0.1'

here = path.abspath(path.dirname(__file__))

with open(path.join(here, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

# get the dependencies and installs
# with open(path.join(here, 'requirements.txt'), encoding='utf-8') as f:
#     all_reqs = f.read().split('\n')

# install_requires = [x.strip() for x in all_reqs if 'git+' not in x]

setup(
    name='leis-brasileiras-ministeriopublicorj',
    version=__version__,
    description='Pacote para baixar leis brasileiras',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/MinisterioPublicoRJ/leis-brasileiras',
    license='MIT',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Programming Language :: Python :: 3',
    ],
    keywords='',
    packages=find_packages(exclude=['docs', 'tests*']),
    include_package_data=True,
    author='GADG',
    install_requires=[
        "beautifulsoup4==4.8.0",
        "certifi==2019.6.16",
        "chardet==3.0.4",
        "python-decouple==3.1",
        "idna==2.8",
        "lxml==4.3.4",
        "requests==2.22.0",
        "selenium==3.141.0",
        "soupsieve==1.9.2",
        "tqdm==4.32.2",
        "urllib3==1.25.3",
        "Unidecode==1.0.23",
        "SQLAlchemy==1.3.8",
        "pandas==0.23.4",
        "numpy==1.15.4"
    ]
)
