# -*- coding: UTF-8 -*-
#
# Copyright (c) 2023 Sergey Bashirov
# All rights reserved.
#
# This source code is licensed under the BSD-style license found in the
# LICENSE file in the root directory of this source tree.

import sys
import os.path

sys.path.insert(1, os.path.join(sys.path[0], "jazzpy"))
import __about__

from setuptools import setup, find_packages

setup(name = "jazzpy",
      version = __about__.__version__,
      description = "CLI tool and library for Jazz app",
      author = __about__.__author__,
      author_email = __about__.__email__,
      license = __about__.__license__,
      url = "https://github.com/sbashiro/jazzpy",
      packages = find_packages(include = ["jazzpy"]),
      entry_points = {
          "console_scripts": ["jazzpy = jazzpy.cli:main"],
      },
      python_requires = ">=3.6",
      install_requires = [
      ],
)
