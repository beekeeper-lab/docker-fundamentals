#!/usr/bin/env bash
# Run the quiz for this day's lesson.
# Works on Linux and macOS.

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"

if command -v python3 &> /dev/null; then
    python3 "$SCRIPT_DIR/run_quiz.py"
elif command -v python &> /dev/null; then
    python "$SCRIPT_DIR/run_quiz.py"
else
    echo "Error: Python is not installed or not in PATH."
    echo "Please install Python 3 from https://www.python.org/downloads/"
    exit 1
fi
