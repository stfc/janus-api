"""Turn config options into constants that can be imported into other modules."""

from __future__ import annotations

import configparser
from pathlib import Path

config = configparser.ConfigParser()

config.read("config.ini")

DATA_DIR = Path(config["settings"]["DATA_DIR"])
PORT = int(config["settings"]["PORT"])
FRONTEND_URL = config["settings"]["FRONTEND_URL"].split(", ")
