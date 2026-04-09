#!/usr/bin/env python3
"""
Package the Docker Fundamentals course for distribution.
Creates a versioned zip file in dist/.
"""

import os
import sys
import shutil
import subprocess
from datetime import datetime
from pathlib import Path
from zipfile import ZipFile

ROOT = Path(__file__).resolve().parent.parent
HTML_OUT = ROOT / "html"
DIST = ROOT / "dist"
COURSE_NAME = "docker-fundamentals"


def get_version(explicit=None):
    if explicit:
        return explicit
    date = datetime.now().strftime("%Y%m%d")
    try:
        git_hash = subprocess.check_output(
            ["git", "rev-parse", "--short", "HEAD"],
            cwd=ROOT, stderr=subprocess.DEVNULL
        ).decode().strip()
        return f"{date}-{git_hash}"
    except Exception:
        return date


def build_course():
    print("Building course...")
    subprocess.check_call(
        [sys.executable, str(ROOT / "scripts" / "build_course.py")],
        cwd=ROOT,
    )


def package(version, output_dir=None):
    output_dir = Path(output_dir) if output_dir else DIST
    output_dir.mkdir(exist_ok=True)

    folder_name = f"{COURSE_NAME}-v{version}"
    zip_path = output_dir / f"{folder_name}.zip"

    print(f"Packaging {folder_name}...")

    with ZipFile(zip_path, "w") as zf:
        # Add index.html
        index_path = ROOT / "index.html"
        if index_path.exists():
            zf.write(index_path, f"{folder_name}/index.html")

        # Add all HTML files
        if HTML_OUT.exists():
            for html_file in sorted(HTML_OUT.glob("*.html")):
                zf.write(html_file, f"{folder_name}/html/{html_file.name}")

        # Add VERSION file
        version_content = f"Version: {version}\nBuilt: {datetime.now().isoformat()}\n"
        zf.writestr(f"{folder_name}/VERSION", version_content)

    size_mb = zip_path.stat().st_size / (1024 * 1024)
    print(f"✓ {zip_path} ({size_mb:.1f} MB)")
    return zip_path


def main():
    import argparse
    parser = argparse.ArgumentParser(description="Package Docker Fundamentals course")
    parser.add_argument("--version", help="Explicit version string")
    parser.add_argument("--skip-build", action="store_true", help="Skip rebuilding")
    parser.add_argument("--out", help="Output directory (default: dist/)")
    args = parser.parse_args()

    version = get_version(args.version)

    if not args.skip_build:
        build_course()

    package(version, args.out)
    print("Done!")


if __name__ == "__main__":
    main()
