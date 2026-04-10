#!/usr/bin/env python3
"""Generate all course illustrations using Google Gemini image generation API.

Reads IMAGE-PLAN.md and generates each planned image.
Skips images that already exist unless --force is used.

Usage:
    uv run --with google-genai --with pillow python scripts/generate_images.py
    uv run --with google-genai --with pillow python scripts/generate_images.py --dry-run
    uv run --with google-genai --with pillow python scripts/generate_images.py --force
"""

import json
import os
import re
import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
IMAGES_DIR = ROOT / "images"
IMAGE_PLAN = ROOT / "IMAGE-PLAN.md"

MODEL = "gemini-3-pro-image-preview"


def load_api_key():
    env_path = ROOT / ".env"
    if env_path.exists():
        for line in env_path.read_text().splitlines():
            if line.startswith("GEMINI_API_KEY="):
                return line.split("=", 1)[1].strip().strip('"').strip("'")
    key = os.environ.get("GEMINI_API_KEY")
    if not key:
        print("ERROR: GEMINI_API_KEY not found in .env or environment")
        sys.exit(1)
    return key


def parse_image_plan():
    """Parse IMAGE-PLAN.md to extract all image entries."""
    text = IMAGE_PLAN.read_text()
    images = []

    # Split on ### Image blocks
    blocks = re.split(r'### Image \d+:', text)

    current_module = ""
    for chunk in text.split("\n"):
        m = re.match(r'^## Module \d+: (.+)', chunk)
        if m:
            current_module = m.group(1).strip()

    # Re-parse more carefully
    images = []
    current_module_title = ""
    lines = text.split("\n")
    i = 0
    while i < len(lines):
        line = lines[i]

        # Track current module
        mod_match = re.match(r'^## Module \d+: (.+)', line)
        if mod_match:
            current_module_title = mod_match.group(1).strip()

        # Find image entries
        img_match = re.match(r'^### Image \d+: (.+)', line)
        if img_match:
            short_name = img_match.group(1).strip()
            entry = {
                "short_name": short_name,
                "module_title": current_module_title,
                "file": "",
                "page": "",
                "placement": "",
                "description": "",
                "prompt_parts": {},
            }

            # Read ahead to extract fields
            j = i + 1
            in_prompt = False
            prompt_lines = []
            while j < len(lines):
                l = lines[j]
                if l.startswith("### Image ") or l.startswith("## Module ") or l.startswith("---"):
                    break

                if in_prompt:
                    if l.startswith("- **") or l.startswith("### ") or l.startswith("## ") or l.strip() == "---":
                        in_prompt = False
                    else:
                        prompt_lines.append(l.strip())
                        j += 1
                        continue

                file_match = re.match(r'- \*\*File\*\*:\s*`(.+?)`', l)
                if file_match:
                    entry["file"] = file_match.group(1)

                page_match = re.match(r'- \*\*Page\*\*:\s*(.+)', l)
                if page_match:
                    entry["page"] = page_match.group(1)

                desc_match = re.match(r'- \*\*Description\*\*:\s*(.+)', l)
                if desc_match:
                    entry["description"] = desc_match.group(1)

                if l.strip() == "- **Prompt**:":
                    in_prompt = True

                j += 1

            # Parse prompt lines into parts
            prompt_text = "\n".join(prompt_lines)
            for key in ["Goal", "Scene", "Style", "Aspect ratio", "Background", "Text in image", "Avoid"]:
                m = re.search(rf'{key}:\s*(.+?)(?:\n\s*(?:Goal|Scene|Style|Aspect|Background|Text in image|Avoid):|$)',
                              prompt_text, re.DOTALL)
                if m:
                    entry["prompt_parts"][key.lower().replace(" ", "_")] = m.group(1).strip()

            if entry["file"]:
                images.append(entry)

        i += 1

    return images


def assemble_prompt(parts):
    """Assemble a full prompt from parts."""
    sections = []
    if "goal" in parts:
        sections.append(f"Goal: {parts['goal']}")
    if "scene" in parts:
        sections.append(f"Scene: {parts['scene']}")
    if "style" in parts:
        sections.append(f"Style: {parts['style']}")
    if "aspect_ratio" in parts:
        sections.append(f"Aspect ratio: {parts['aspect_ratio']}")
    if "background" in parts:
        sections.append(f"Background: {parts['background']}")
    if "text_in_image" in parts:
        sections.append(f"Text in image: {parts['text_in_image']}")
    if "avoid" in parts:
        sections.append(f"Avoid: {parts['avoid']}")
    return "\n".join(sections)


def generate_image(prompt, output_path, api_key):
    """Generate an image using Gemini API. Returns metadata dict."""
    from google import genai
    from google.genai import types

    client = genai.Client(api_key=api_key)

    start_time = time.time()

    response = client.models.generate_content(
        model=MODEL,
        contents=prompt,
        config=types.GenerateContentConfig(
            response_modalities=["IMAGE", "TEXT"],
        ),
    )

    elapsed_ms = int((time.time() - start_time) * 1000)

    # Extract image from response
    if not response.candidates or not response.candidates[0].content.parts:
        raise ValueError("No image in response")

    image_data = None
    for part in response.candidates[0].content.parts:
        if part.inline_data and part.inline_data.mime_type.startswith("image/"):
            image_data = part.inline_data.data
            break

    if not image_data:
        raise ValueError("No image data found in response parts")

    # Save image
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_bytes(image_data)

    # Extract usage
    usage = {}
    if hasattr(response, 'usage_metadata') and response.usage_metadata:
        um = response.usage_metadata
        usage = {
            "prompt_tokens": getattr(um, 'prompt_token_count', 0),
            "candidates_tokens": getattr(um, 'candidates_token_count', 0),
            "total_tokens": getattr(um, 'total_token_count', 0),
        }

    metadata = {
        "timestamp": time.strftime("%Y-%m-%dT%H:%M:%S"),
        "model": MODEL,
        "prompt": prompt,
        "output_file": output_path.name,
        "generation_time_ms": elapsed_ms,
        "usage": usage,
    }

    return metadata


def main():
    import argparse
    parser = argparse.ArgumentParser(description="Generate course illustrations")
    parser.add_argument("--dry-run", action="store_true", help="Show what would be generated")
    parser.add_argument("--force", action="store_true", help="Regenerate existing images")
    parser.add_argument("--filter", help="Only generate images matching this string in the file path")
    args = parser.parse_args()

    api_key = load_api_key()
    images = parse_image_plan()

    if args.filter:
        images = [img for img in images if args.filter in img["file"]]

    print(f"Image Generator — {len(images)} images planned")
    print(f"Model: {MODEL}")
    print("=" * 60)

    total_tokens = 0
    total_time_ms = 0
    generated = 0
    skipped = 0
    errors = 0

    for idx, img in enumerate(images):
        file_path = IMAGES_DIR / img["file"].replace("images/", "")
        short = f"[{idx+1}/{len(images)}] {img['short_name']}"

        if file_path.exists() and not args.force:
            print(f"  {short} — exists, skipping")
            skipped += 1
            continue

        prompt = assemble_prompt(img["prompt_parts"])
        if not prompt:
            print(f"  {short} — no prompt found, skipping")
            skipped += 1
            continue

        if args.dry_run:
            print(f"  {short} — WOULD GENERATE → {img['file']}")
            continue

        print(f"  {short} — generating...", end="", flush=True)

        try:
            meta = generate_image(prompt, file_path, api_key)

            # Save metadata JSON alongside the image
            json_path = file_path.with_suffix(".json")
            json_path.write_text(json.dumps(meta, indent=2))

            tokens = meta.get("usage", {}).get("total_tokens", 0)
            elapsed = meta.get("generation_time_ms", 0)
            total_tokens += tokens
            total_time_ms += elapsed
            generated += 1

            size_kb = file_path.stat().st_size / 1024
            print(f" ✓ {size_kb:.0f} KB, {tokens} tokens, {elapsed/1000:.1f}s")

        except Exception as e:
            errors += 1
            print(f" ✗ Error: {e}")

    print("=" * 60)
    print(f"Generated: {generated}, Skipped: {skipped}, Errors: {errors}")
    if generated > 0:
        est_cost = total_tokens * 0.00007  # rough estimate
        print(f"Total tokens: {total_tokens:,}")
        print(f"Total time: {total_time_ms/1000:.1f}s ({total_time_ms/1000/generated:.1f}s avg)")
        print(f"Estimated cost: ${est_cost:.2f}")

    # Return stats for logging
    return {
        "generated": generated,
        "skipped": skipped,
        "errors": errors,
        "total_tokens": total_tokens,
        "total_time_ms": total_time_ms,
    }


if __name__ == "__main__":
    main()
