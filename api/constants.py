"""Turn config options into constants that can be imported into other modules."""

from __future__ import annotations

import configparser
from pathlib import Path

# Create a ConfigParser object
config = configparser.ConfigParser()

# Read the config.ini file
config.read("config.ini")

# Read the settings from the config file
DATA_DIR = Path(config["settings"]["DATA_DIR"])
OUTPUT_DIR = Path(config["settings"]["OUTPUT_DIR"])
PORT = int(config["settings"]["PORT"])
FRONTEND_URL = config["settings"]["FRONTEND_URL"].split(", ")

# Optionally, you can print the values to verify they are loaded correctly
print(f"DATA_DIR: {DATA_DIR}")
print(f"OUTPUT_DIR: {OUTPUT_DIR}")
print(f"PORT: {PORT}")
print(f"FRONTEND_URL: {FRONTEND_URL}")
