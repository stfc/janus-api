"""Turn config options into constants that can be imported into other modules."""

from __future__ import annotations

import os
from pathlib import Path

from dotenv import find_dotenv, load_dotenv

load_dotenv(find_dotenv())

DATA_DIR = Path(os.getenv("DATA_DIR"))
OUTPUT_DIR = Path(os.getenv("DATA_DIR"))
PORT = int(os.getenv("PORT"))
FRONTEND_URL = os.getenv("FRONTEND_URL")
