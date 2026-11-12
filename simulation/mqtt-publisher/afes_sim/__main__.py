"""Module entrypoint for ``python -m afes_sim``."""

from __future__ import annotations

import sys

from .cli import main

if __name__ == "__main__":
    raise SystemExit(main())
