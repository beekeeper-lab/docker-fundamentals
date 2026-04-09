#!/usr/bin/env python3
"""Launch the Day 10 quiz."""

import subprocess
import sys
from pathlib import Path

quiz_app = Path(__file__).resolve().parent.parent.parent / "quiz_app.py"
subprocess.run([sys.executable, str(quiz_app), "Docker_Fundamentals", "10"])
