"""
Example: Generate a steampunk London Bridge movie poster.
"""

import os
import sys

# Add parent directory to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from agnes_image import generate_image, save_image

prompt = (
    "A vintage steampunk movie poster of Tower Bridge in London at sunset. "
    "The bridge is adorned with brass gears, copper pipes, and steam vents. "
    "Victorian airships float in the golden sky above. "
    "Rich sepia and amber tones, cinematic lighting with dramatic shadows. "
    "Retro typography elements, ornate decorative borders. "
    "Movie poster composition, vertical 9:16 aspect ratio, 4K quality, photorealistic style."
)

try:
    url = generate_image(prompt, size="768x1344")
    print(f"Generated: {url}")
    save_image(url, "steampunk_london_poster.jpg")
except Exception as e:
    print(f"Error: {e}")
