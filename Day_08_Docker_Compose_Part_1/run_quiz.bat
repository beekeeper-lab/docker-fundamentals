@echo off
REM Run the quiz for this day's lesson.
REM Works on Windows.

cd /d "%~dp0"

where python >/dev/null 2>/dev/null
if %errorlevel% equ 0 (
    python run_quiz.py
) else (
    where python3 >/dev/null 2>/dev/null
    if %errorlevel% equ 0 (
        python3 run_quiz.py
    ) else (
        echo Error: Python is not installed or not in PATH.
        echo Please install Python 3 from https://www.python.org/downloads/
        pause
    )
)
