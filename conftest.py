"""Make the backend package importable from the repo root under pytest."""
from __future__ import annotations

import sys
from pathlib import Path

BACKEND = Path(__file__).resolve().parent / "backend"
if str(BACKEND) not in sys.path:
    sys.path.insert(0, str(BACKEND))
