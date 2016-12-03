#!/usr/bin/env python3

# --------------------- #
# -- SEVERAL IMPORTS -- #
# --------------------- #

from mistool.os_use import PPath, runthis


# --------------- #
# -- CONSTANTS -- #
# --------------- #

THIS_FILE = PPath(__file__)
THIS_DIR  = THIS_FILE.parent


# -------------------------------------- #
# -- LAUNCHING ALL THE BUILDING TOOLS -- #
# -------------------------------------- #

for onepath in THIS_DIR.walk("file::**/build_*.py"):
    print('+ Launching "{0}"'.format(onepath.name))

    runthis(
        cmd        = 'python "{0}"'.format(THIS_DIR / onepath),
        showoutput = True
    )
