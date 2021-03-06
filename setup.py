# ------------------------------------------------ #
# -- LINE COMMANDS FOR TWINE (which uses HTTPS) -- #
# ------------------------------------------------ #

# Source: https://pypi.python.org/pypi/twine

#     1) Create some distributions in the normal way:
#         > python setup.py sdist bdist_wheel
#
#     2) Upload with twine:
#         > twine upload dist/* --skip-existing


# -------------------- #
# -- STANDARD TOOLS -- #
# -------------------- #

from setuptools import setup, find_packages
from pathlib import Path
import pypandoc


# ----------------- #
# -- README FILE -- #
# ----------------- #

readme = Path(__file__).parent / 'README.md'

longdesc = pypandoc.convert(str(readme), 'rst')


# ----------------- #
# -- OUR SETTNGS -- #
# ----------------- #

setup(
# General
    name         = "cdt",
    version      = "0.0.0-beta",
    url          = 'https://github.com/bc-python-pedagogy/cdt.git',
    license      = 'GPLv3',
    author       = "Christophe BAL",
    author_email = "projetmbc@gmail.com",

# Descritions
    long_description = longdesc,
    description      = "Pedagogical log - \"[C]ahier [d]e [T]exte\" in French",

# What to add ?
    packages = find_packages(),

# # Uggly classifiers
#     classifiers = [
#         'Development Status :: 5 - Production/Stable',
#         'Intended Audience :: Developers',
#         'License :: OSI Approved :: GNU General Public License (GPL)',
#         'Programming Language :: Python :: 3',
#         'Operating System :: MacOS',
#         'Operating System :: Microsoft :: Windows',
#         'Operating System :: POSIX :: Linux',
#         'Topic :: Utilities',
#         'Topic :: Software Development :: Libraries :: Python Modules',
#     ],
#
# # What does your project relate to?
#     keywords = 'python data',
)
