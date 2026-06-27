"""
Agnes Image Generation Helper

A simple wrapper for the Agnes Image 2.1 Flash API with retry logic.

Usage:
    pip install requests python-dotenv

    # Method 1: Import and use in your own script
    from agnes_image import generate_image
    url = generate_image("A sunset over the ocean", size="1024x768")

    # Method 2: Run from command line with --prompt
    python agnes_image.py --prompt "A sunset over the ocean" --size 1024x768

    # Method 3: Run with prompt from stdin (pipe)
    echo "A sunset over the ocean" | python agnes_image.py

    # Method 4: Use interactive mode
    python agnes_image.py --interactive
"""

import os
import sys
import argparse
import requests
import time
from typing import Optional, Union


ENDPOINT = "https://apihub.agnes-ai.com/v1/images/generations"
MODEL = "agnes-image-2.1-flash"


def generate_image(
    prompt: str,
    size: str = "1024x768",
    retries: int = 3,
    timeout: int = 120,
    response_format: str = "url",
    image_to_image: Optional[list[str]] = None,
) -> str:
    """
    Generate an image using the Agnes Image API.

    Args:
        prompt: Text description of the image to generate.
        size: Output dimensions, e.g. "1024x768".
        retries: Number of retry attempts on failure.
        timeout: Request timeout in seconds.
        response_format: "url" or "b64_json".
        image_to_image: List of input image URLs for image-to-image mode.

    Returns:
        Image URL or Base64 string (depending on response_format).

    Raises:
        ValueError: If API key is not configured.
        RuntimeError: If all retry attempts fail.
    """
    api_key = os.environ.get("AGNES_IMAGE_API_KEY")
    if not api_key:
        raise ValueError(
            "AGNES_IMAGE_API_KEY environment variable not set.\n"
            "Create a .env file or export the variable."
        )

    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
    }

    extra_body: dict = {"response_format": response_format}
    if image_to_image:
        extra_body["image"] = image_to_image

    payload = {
        "model": MODEL,
        "prompt": prompt,
        "size": size,
        "extra_body": extra_body,
    }

    for attempt in range(retries):
        try:
            response = requests.post(
                ENDPOINT, json=payload, headers=headers, timeout=timeout
            )

            if response.status_code == 200:
                result = response.json()
                data = result.get("data", [])
                if data:
                    if response_format == "b64_json":
                        return data[0].get("b64_json", "")
                    return data[0].get("url", "")

            elif response.status_code == 429:
                wait = (attempt + 1) * 2
                print(f"Rate limited. Retrying in {wait}s...")
                time.sleep(wait)
            else:
                print(f"Error {response.status_code}: {response.text}")

        except requests.exceptions.Timeout:
            print(f"Timeout on attempt {attempt + 1}. Retrying...")
            time.sleep(2)

    raise RuntimeError(f"Failed to generate image after {retries} attempts")


def save_image(url: str, filename: str = "generated_image.png") -> None:
    """Download an image from URL and save to file."""
    response = requests.get(url, timeout=60)
    with open(filename, "wb") as f:
        f.write(response.content)
    print(f"Saved to {filename} ({len(response.content)} bytes)")


def interactive_mode():
    """Interactive mode: ask for prompt in a loop."""
    print("Agnes AI Image Generator - Interactive Mode")
    print("Type your prompt and press Enter to generate.")
    print("Type 'quit' or 'exit' to quit.\n")

    while True:
        try:
            prompt = input("Prompt: ").strip()
        except (EOFError, KeyboardInterrupt):
            print("\nBye!")
            break

        if not prompt:
            print("Prompt cannot be empty.\n")
            continue
        if prompt.lower() in ("quit", "exit", "q"):
            print("Bye!")
            break

        try:
            size = input("Size (default 1024x768): ").strip() or "1024x768"
        except (EOFError, KeyboardInterrupt):
            size = "1024x768"

        print(f"\nGenerating image...\n")
        try:
            url = generate_image(prompt, size=size)
            print(f"Image URL: {url}")

            save = input("Save to file? (y/n, default n): ").strip().lower()
            if save == "y":
                filename = input("Filename (default generated_image.png): ").strip() or "generated_image.png"
                save_image(url, filename)
            print()
        except Exception as e:
            print(f"Error: {e}\n")


def main():
    parser = argparse.ArgumentParser(
        description="Generate images using Agnes AI Image API"
    )
    parser.add_argument(
        "--prompt", "-p",
        type=str,
        help="Image description (prompt). If not provided, reads from stdin."
    )
    parser.add_argument(
        "--size", "-s",
        type=str,
        default="1024x768",
        help="Output image size, e.g. 1024x768 (default: 1024x768)"
    )
    parser.add_argument(
        "--output", "-o",
        type=str,
        default=None,
        help="Output filename. If not provided, only prints the URL."
    )
    parser.add_argument(
        "--interactive", "-i",
        action="store_true",
        help="Run in interactive mode, prompts for input"
    )

    args = parser.parse_args()

    if args.interactive:
        interactive_mode()
        return

    # Get prompt: from --prompt arg, or from stdin pipe
    prompt = args.prompt
    if not prompt:
        if sys.stdin.isatty():
            print("Error: no prompt provided. Use --prompt 'your description' or pipe from stdin.")
            print("Example: echo 'A sunset over the ocean' | python agnes_image.py")
            sys.exit(1)
        else:
            prompt = sys.stdin.read().strip()

    if not prompt:
        print("Error: empty prompt.")
        sys.exit(1)

    try:
        url = generate_image(prompt, size=args.size)
        print(f"Generated image: {url}")

        if args.output:
            save_image(url, args.output)
        else:
            save = input("Save to file? (y/n, default n): ").strip().lower()
            if save == "y":
                filename = input("Filename (default generated_image.png): ").strip() or "generated_image.png"
                save_image(url, filename)
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
