#!/usr/bin/env python3
"""
Gemini Image Generation Script
Calls Gemini API to generate images from text prompts.
Saves output image as PNG file.

Usage:
  python3 gemini_image_gen.py --prompt "a cute cat" --output /path/to/output.png
  python3 gemini_image_gen.py --prompt "a cute cat"  # saves to ./gemini_output.png
"""

import argparse
import base64
import json
import os
import sys
import urllib.request
import urllib.error

# Config - read from openclaw.json or use defaults
BASE_URL = "https://llm-gateway-proxy.inner.chj.cloud/llm-gateway/v1beta"
API_KEY = os.environ.get("GEMINI_API_KEY")
MODEL = "gemini-3-pro-image-preview"


def generate_image(prompt: str, output_path: str, ref_image: str = None) -> str:
    """Call Gemini API to generate an image from a text prompt, optionally with a reference image."""

    url = f"{BASE_URL}/models/{MODEL}:generateContent"

    # Build parts list
    parts = []

    # Add reference image if provided
    if ref_image:
        with open(ref_image, "rb") as f:
            img_data = base64.b64encode(f.read()).decode("utf-8")
        # Detect mime type
        mime_type = "image/jpeg"
        if ref_image.lower().endswith(".png"):
            mime_type = "image/png"
        elif ref_image.lower().endswith(".webp"):
            mime_type = "image/webp"
        parts.append({"inline_data": {"mime_type": mime_type, "data": img_data}})
        print(f"Reference image loaded: {ref_image} ({mime_type})")

    # Add text prompt
    parts.append({"text": prompt})

    payload = {
        "contents": [
            {
                "role": "user",
                "parts": parts
            }
        ],
        "generationConfig": {
            "responseModalities": ["TEXT", "IMAGE"],
            "temperature": 1.0
        }
    }

    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {API_KEY}",
        "x-goog-api-key": API_KEY
    }

    data = json.dumps(payload).encode("utf-8")
    req = urllib.request.Request(url, data=data, headers=headers, method="POST")

    try:
        print(f"Calling Gemini API with prompt: {prompt[:80]}...")
        with urllib.request.urlopen(req, timeout=120) as resp:
            body = json.loads(resp.read().decode("utf-8"))
    except urllib.error.HTTPError as e:
        error_body = e.read().decode("utf-8") if e.fp else ""
        print(f"HTTP Error {e.code}: {error_body[:500]}", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"Request failed: {e}", file=sys.stderr)
        sys.exit(1)

    # Parse response - look for inline_data with image
    candidates = body.get("candidates", [])
    if not candidates:
        print(f"No candidates in response. Full response:\n{json.dumps(body, indent=2)[:1000]}", file=sys.stderr)
        sys.exit(1)

    content = candidates[0].get("content", {})
    parts = content.get("parts", [])

    image_saved = False
    text_response = ""

    for part in parts:
        if "inlineData" in part:
            inline = part["inlineData"]
            mime = inline.get("mimeType", "image/png")
            b64_data = inline.get("data", "")

            if b64_data:
                img_bytes = base64.b64decode(b64_data)

                # Determine extension from mime
                ext = ".png"
                if "jpeg" in mime or "jpg" in mime:
                    ext = ".jpg"
                elif "webp" in mime:
                    ext = ".webp"

                # Adjust output path extension if needed
                if not output_path.endswith(ext):
                    base = os.path.splitext(output_path)[0]
                    output_path = base + ext

                os.makedirs(os.path.dirname(output_path) or ".", exist_ok=True)
                with open(output_path, "wb") as f:
                    f.write(img_bytes)

                print(f"Image saved to: {output_path} ({len(img_bytes)} bytes, {mime})")
                image_saved = True

        elif "text" in part:
            text_response = part["text"]

    if text_response:
        print(f"Model text: {text_response[:200]}")

    if not image_saved:
        print(f"No image data in response. Parts: {json.dumps(parts, indent=2)[:1000]}", file=sys.stderr)
        sys.exit(1)

    return output_path


def main():
    parser = argparse.ArgumentParser(description="Generate images using Gemini API")
    parser.add_argument("--prompt", "-p", required=True, help="Text prompt for image generation")
    parser.add_argument("--output", "-o", default="gemini_output.png", help="Output file path")
    parser.add_argument("--ref", "-r", default=None, help="Reference image path (for style transfer / image editing)")
    args = parser.parse_args()

    result = generate_image(args.prompt, args.output, ref_image=args.ref)
    print(f"SUCCESS: {result}")


if __name__ == "__main__":
    main()
