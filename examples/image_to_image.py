"""
Example: Image-to-Image style transfer.
"""

import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from agnes_image import generate_image

# Transform a photo into a different art style
prompt = (
    "Transform this photo into an oil painting style "
    "while preserving the original composition and subject"
)

try:
    url = generate_image(
        prompt=prompt,
        size="1024x768",
        image_to_image=["https://example.com/source-photo.jpg"],
    )
    print(f"Generated: {url}")
except Exception as e:
    print(f"Error: {e}")
