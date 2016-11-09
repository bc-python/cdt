#!/usr/bin/env python3

import datetime

from mistool.date_use import translate

def datename(yearnb, monthnb, daynb):
    return translate(
        date      = datetime.date(int(yearnb), int(monthnb), int(daynb)),
        strformat = "%A %d %B %Y",
        lang      = "fr_FR"
    )
