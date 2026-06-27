---
name: "agnes-ai-image-skill"
description: "Generate images using the Agnes Image 2.1 Flash API — text-to-image and image-to-image editing. Triggers when the user asks to generate, create, draw, render, or produce any image from a text description, or requests image editing/transformation via image-to-image. Requires an Agnes AI API key."
license: MIT
---

# Agnes AI Image Generation Skill

## What Is This

A skill that enables Claude to generate images via the Agnes Image 2.1 Flash API. Two modes:

- **Text-to-image** — describe what you want, get an image
- **Image-to-image** — provide a source image, transform it while preserving composition

## Prerequisites

- Python 3.8+ with `requests` library
- A valid Agnes AI API key set as the `AGNES_IMAGE_API_KEY` environment variable

### Getting an API Key

1. Sign up at [https://apihub.agnes-ai.com](https://apihub.agnes-ai.com)
2. Navigate to your dashboard
3. Create a new API key
4. Set it as an environment variable:

```bash
# Linux / macOS
export AGNES_IMAGE_API_KEY="sk-your-key-here"

# Windows (Command Prompt)
set AGNES_IMAGE_API_KEY=sk-your-key-here

# Windows (PowerShell)
$env:AGNES_IMAGE_API_KEY="sk-your-key-here"
```

Or use a `.env` file with `python-dotenv`. **Never commit `.env` files to version control.**

## API Reference

| Property | Value |
|----------|-------|
| **Base URL** | `https://apihub.agnes-ai.com` |
| **Endpoint** | `POST /v1/images/generations` |
| **Model** | `agnes-image-2.1-flash` |
| **Auth** | `Authorization: Bearer <API_KEY>` |

### Request Body

```json
{
    "model": "agnes-image-2.1-flash",
    "prompt": "Your image description here",
    "size": "1024x768",
    "extra_body": {
        "response_format": "url"
    }
}
```

### Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `model` | string | Yes | Always `agnes-image-2.1-flash` |
| `prompt` | string | Yes | Text description of the image |
| `size` | string | Yes | Output dimensions, e.g. `1024x768` |
| `extra_body.response_format` | string | No | `"url"` or `"b64_json"` |
| `extra_body.image` | array | No | Image-to-image input URLs |

### Response

```json
{
    "created": 1782563111,
    "data": [{
        "url": "https://platform-outputs.agnes-ai.space/images/t2i/abc123.png",
        "b64_json": null,
        "revised_prompt": null
    }]
}
```

## Prompt Engineering

### Structure for Best Results

```
[Subject] + [Scene/Environment] + [Style] + [Lighting] + [Composition] + [Quality]
```

| Element | What to Include | Example |
|---------|----------------|---------|
| Subject | Main focus | "A group of football players" |
| Scene | Background, setting | "on a football pitch under stadium lights" |
| Style | Artistic direction | "cinematic movie poster, photorealistic" |
| Lighting | Mood | "dramatic golden hour lighting, deep shadows" |
| Composition | Framing | "heroic low-angle shot, wide composition" |
| Quality | Resolution cues | "4K, ultra-detailed, professional photography" |

### Tips

- **Be specific** — vague prompts produce generic results
- **Use concrete nouns and adjectives** — "red jersey with gold trim" beats "colorful shirt"
- **Specify aspect ratio** — add "vertical 9:16 composition" to the prompt
- **Avoid contradictions** — don't mix conflicting styles
- **English prompts work best** — the model is optimized for English

### Bad vs Good

```
❌ Bad: "a cat"
✅ Good: "A fluffy orange tabby cat sitting on a windowsill, soft morning sunlight, bokeh city background, photorealistic, 4K"
```

```
❌ Bad: "make it cool"
✅ Good: "Cyberpunk cityscape at night, neon reflections on wet streets, cinematic wide-angle, blade runner style"
```

## Image Sizes

| Use Case | Size | Aspect Ratio |
|----------|------|-------------|
| Portrait / Social Media | `768x1344` | 9:16 |
| Standard | `1024x768` | 4:3 |
| Square | `1024x1024` | 1:1 |
| Landscape | `1024x576` | 16:9 |
| Tall Poster | `768x1792` | 3:7 |
| Wide Banner | `1792x768` | 7:3 |

## Text-to-Image Example

```python
import requests
import os

API_KEY = os.environ.get("AGNES_IMAGE_API_KEY")
ENDPOINT = "https://apihub.agnes-ai.com/v1/images/generations"

headers = {
    "Authorization": f"Bearer {API_KEY}",
    "Content-Type": "application/json",
}

payload = {
    "model": "agnes-image-2.1-flash",
    "prompt": "A cute golden retriever puppy sitting in a field of sunflowers, soft lighting, photorealistic style",
    "size": "1024x768",
    "extra_body": {
        "response_format": "url"
    }
}

response = requests.post(ENDPOINT, json=payload, headers=headers, timeout=120)
result = response.json()

if response.status_code == 200 and result.get("data"):
    image_url = result["data"][0]["url"]
    print(f"Generated image: {image_url}")
else:
    print(f"Error: {result}")
```

## Image-to-Image Example

Transform an existing image while preserving composition:

```python
payload = {
    "model": "agnes-image-2.1-flash",
    "prompt": "Transform the scene into a cyberpunk night with neon reflections while preserving the original composition",
    "size": "1024x768",
    "extra_body": {
        "image": ["https://example.com/input-image.png"],
        "response_format": "url"
    }
}

response = requests.post(ENDPOINT, json=payload, headers=headers, timeout=120)
result = response.json()
image_url = result["data"][0]["url"]
```

**Requirements:** Input image URLs must be publicly accessible (no login/cookies).

## Save Generated Images

```python
import requests

image_response = requests.get(image_url, timeout=60)
with open("generated_image.png", "wb") as f:
    f.write(image_response.content)
```

## Base64 Output

```python
payload = {
    "model": "agnes-image-2.1-flash",
    "prompt": "A serene mountain lake at sunset",
    "size": "1024x768",
    "extra_body": {
        "response_format": "b64_json"
    }
}

response = requests.post(ENDPOINT, json=payload, headers=headers, timeout=120)
result = response.json()
import base64

image_data = result["data"][0]["b64_json"]
with open("generated_image.png", "wb") as f:
    f.write(base64.b64decode(image_data))
```

## Error Handling

| Status Code | Error | Solution |
|-------------|-------|----------|
| 401 | Invalid API key | Check `AGNES_IMAGE_API_KEY` is set correctly |
| 422 | Invalid prompt | Review prompt for forbidden content |
| 429 | Rate limited | Wait and retry |
| 500 | Server error | Retry the request |
| Timeout | Request exceeded limit | Increase timeout or simplify prompt |

### Robust Wrapper with Retry

```python
import requests
import time
import os

def generate_image(prompt, size="1024x768", retries=3, timeout=120):
    """Generate an image with automatic retry on failure."""
    api_key = os.environ.get("AGNES_IMAGE_API_KEY")
    if not api_key:
        raise ValueError("AGNES_IMAGE_API_KEY environment variable not set")

    endpoint = "https://apihub.agnes-ai.com/v1/images/generations"
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
    }
    payload = {
        "model": "agnes-image-2.1-flash",
        "prompt": prompt,
        "size": size,
        "extra_body": {"response_format": "url"},
    }

    for attempt in range(retries):
        try:
            response = requests.post(endpoint, json=payload, headers=headers, timeout=timeout)
            if response.status_code == 200:
                result = response.json()
                return result["data"][0]["url"]
            elif response.status_code == 429:
                wait = (attempt + 1) * 2
                print(f"Rate limited. Retrying in {wait}s...")
                time.sleep(wait)
            else:
                print(f"Error {response.status_code}: {response.text}")
        except requests.exceptions.Timeout:
            print(f"Timeout on attempt {attempt + 1}. Retrying...")
            time.sleep(2)

    raise RuntimeError(f"Failed after {retries} attempts")
```

## Critical Rules

1. **`response_format` goes inside `extra_body`** — never at the top level
2. **Never pass `tags: ["img2img"]`** — not needed, may cause errors
3. **Never expose API keys** in code, docs, or shared files
4. **Request timeout** should be 60s–360s depending on complexity
5. **Image URLs for image-to-image** must be publicly accessible (HTTPS, no login)
6. **Always check `response.status_code`** before accessing result data
7. **Handle missing `data` array** gracefully — API may return errors without images

## Troubleshooting

- **401 "Invalid token"** — API key is missing or incorrect. Verify `AGNES_IMAGE_API_KEY`.
- **Blank or empty image** — Prompt may be too vague or contain restricted content. Refine and retry.
- **Timeout** — Simplify the prompt or increase timeout.
- **Wrong aspect ratio** — Specify ratio in both the prompt AND the `size` parameter.
- **Image-to-image fails** — Ensure the source URL is publicly accessible and uses HTTPS.
