# SPDX-License-Identifier: MIT
# Copyright (c) 2022 Andriel Ferreira <https://github.com/AndrielFR>

from mews import database

conn = database.get_conn()

from .posts import *
from .words import *
