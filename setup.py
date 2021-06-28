# -*- coding: utf-8 -*-
#
# This file is part of the python-draughts library.
# Copyright (C) 2012-2014 Niklas Fiekas <niklas.fiekas@tu-clausthal.de>
# Copyright (C) 2015- Tasuku SUENAGA <tasuku-s-github@titech.ac>
# Copyright (C) 2021- TheYoBots (Yohaan Seth Nathan)
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.

import os
import io
import draughts
import setuptools

def read_description():
  description = io.open(os.path.join(os.path.dirname(__file__), 'README.rst'), encoding='utf-8').read()
  return description

setuptools.setup(
    name = 'python-draughts',
    version = draughts.__version__,
    author = draughts.__author__,
    author_email = draughts.__email__,
    description = 'A pure Python draughts library with move generation and validation and handling of common formats.',
    long_description = read_description(),
    license = "GPL3",
    keywords = 'draughts hub pdn',
    url = 'https://github.com/TheYoBots/python-draughts',
    packages = ['draughts'],
    scripts = [],
    test_suite = 'nose.collector',
    tests_require = ['nose>=1.0', 'mock'],
    classifiers = [
      'Development Status :: 5 - Production/Stable',
      'Intended Audience :: Developers',
      'License :: OSI Approved :: GNU General Public License (GPL)',
      'Operating System :: OS Independent',
      'Programming Language :: Python',
      'Programming Language :: Python :: 2',
      'Programming Language :: Python :: 2.7',
      'Programming Language :: Python :: 3',
      'Topic :: Games/Entertainment :: Board Games',
      'Topic :: Software Development :: Libraries :: Python Modules',
    ],
)
