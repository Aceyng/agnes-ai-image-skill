# Agnes AI Image Skill

> Generate high-quality images from text descriptions — supports Text-to-Image and Image-to-Image, designed for Claude users.

[中文说明](README_zh.md)

## At a Glance

This is a skill that lets Claude **generate images** for you. Simply describe what you want in words, and Claude will call the Agnes AI image generation API to create a high-resolution image.

## Technical Details

- **Underlying Model:** `agnes-image-2.1-flash` (by Agnes AI)
- **API URL:** [https://apihub.agnes-ai.com](https://apihub.agnes-ai.com)
- **Features:** Text-to-Image, Image-to-Image
- **License:** MIT

## Quick Start

### Step 1: Get Your API Key

1. Visit [https://apihub.agnes-ai.com](https://apihub.agnes-ai.com)
2. Register / log in to your account
3. Go to your Dashboard and create a new API Key
4. Copy and save the key (format: `sk-xxxxxxxxxxxxxxxx`)

### Step 2: Install This Skill

Choose one of the following methods:

#### Method 1: One-Click Install (Recommended, requires Node.js)

```bash
npx skills add Aceyng/agnes-ai-image-skill
```

> Restart Claude after installation.

#### Method 2: Manual Install

1. Download this repository (click the green Code button → Download ZIP)
2. Extract and rename the folder to `agnes-ai-image-skill`
3. Place the folder into Claude's skills directory:

   ```bash
   # macOS / Linux
   cp -r agnes-ai-image-skill ~/.claude/skills/

   # Windows (Command Prompt)
   xcopy /E /I agnes-ai-image-skill %USERPROFILE%\.claude\skills\
   ```

4. Restart Claude

### Step 3: Configure Your API Key

After installation, set the API Key in your terminal:

```bash
# Linux / macOS
export AGNES_IMAGE_API_KEY="sk-your-key-here"

# Windows (Command Prompt)
set AGNES_IMAGE_API_KEY=sk-your-key-here

# Windows (PowerShell)
$env:AGNES_IMAGE_API_KEY="sk-your-key-here"
```

Alternatively, create a `.env` file (requires `python-dotenv`):

```bash
pip install python-dotenv
```

Then write into `.env`:
```
AGNES_IMAGE_API_KEY=sk-your-key-here
```

> **Security Reminder:** Never commit your API Key to a public repository! The `.env` file is excluded by `.gitignore`.

### Step 4: Use in Claude

Once installed and configured, simply describe the image you want in your conversation with Claude:

#### Example 1: Text-to-Image

> "Draw a vintage poster — Steampunk London Tower Bridge at sunset, cinematic lighting, 4K"

#### Example 2: Social Media Image

> "Generate a vertical image, 9:16 ratio, Steampunk cityscape for Instagram"

#### Example 3: Image-to-Image

> "Convert this photo https://example.com/photo.jpg into an oil painting style"

#### Example 4: Using the Command-Line Script

```bash
python examples/movie_poster.py
```

## Where Are Generated Images Saved?

### Via Claude Conversation

1. Claude returns a **thumbnail preview** directly in the chat
2. A **direct link** is provided to open the full-size image in a new tab
3. Some integrations (like Cowork) display the image as a clickable card

### Via Command-Line Scripts

After running a script, the image is saved in your **current working directory**.

```bash
# Run from the project root
python examples/movie_poster.py

# The image is saved as movie_poster.jpg in the current directory
```

You can customize the output path in the script:

```python
import os
os.makedirs("my_custom_path", exist_ok=True)
save_image(url, "my_custom_path/output.png")
```

### Image Formats

- Default: **PNG** (lossless quality)
- Optional: **JPG** (smaller file size)

## Supported Features

| Feature | Description | Example |
|---------|-------------|---------|
| **Text-to-Image** | Generate images from text descriptions | "A golden retriever puppy in a sunflower field" |
| **Image-to-Image** | Transform an existing image while preserving composition | "Convert this photo to a cyberpunk night scene" |
| **Custom Sizes** | Support various aspect ratios | Vertical 9:16, Horizontal 16:9, Square 1:1 |

## Prompt Tips

For better results, use this formula:

```
[Subject] + [Scene/Background] + [Style] + [Lighting] + [Composition] + [Quality]
```

**Bad Example:** "a cat"

**Good Example:** "An orange tabby cat sitting on a windowsill, warm morning sunlight, blurred city background, photorealistic, 4K"

**Recommended Sizes:**

| Use Case | Size | Aspect Ratio |
|----------|------|--------------|
| Vertical social media (TikTok/Instagram) | `768x1344` | 9:16 |
| Standard image | `1024x768` | 4:3 |
| Square | `1024x1024` | 1:1 |
| Horizontal (YouTube thumbnail) | `1024x576` | 16:9 |

## Frequently Asked Questions

### Q: What quality are the generated images?

A: Default output is high-definition, supporting up to 4K resolution. Image quality depends on how specific and clear your description is.

### Q: How long does generation take?

A: Typically 30 seconds to 2 minutes, depending on image complexity and server load.

### Q: Does it support Chinese descriptions?

A: English descriptions work best. If you use Chinese, the system will auto-translate, but results may be less precise.

### Q: Is it free?

A: You need an Agnes AI API key. Check pricing at [Agnes AI Pricing](https://apihub.agnes-ai.com).

### Q: Can't find the skill after installation?

A: Please verify:
1. The skill folder contains the `SKILL.md` file
2. The folder is placed in the correct skills directory
3. You restarted your AI assistant tool (Claude Desktop, Cursor, etc.)

## Project Structure

```
agnes-ai-image-skill/
├── SKILL.md              # Core skill file (read by Claude)
├── README.md             # Project documentation (this file)
├── README_zh.md          # Chinese documentation
├── LICENSE               # MIT License
├── requirements.txt      # Python dependencies
├── .gitignore            # Git ignore rules
├── examples/             # Example scripts
│   ├── agnes_image.py    # Python wrapper (with auto-retry and CLI args)
│   ├── movie_poster.py   # Movie poster generation example
│   └── image_to_image.py # Image-to-image example
└── skills/
    └── README.md         # Subdirectory notes
```

## Contributing

Issues and Pull Requests are welcome!

## Cross-Platform Compatibility

This skill is essentially **Python scripts + API calls**, with no dependency on any specific AI assistant tool. As long as your environment supports running Python code, you can use it directly.

### Supported Tools

| Tool | Notes |
|------|-------|
| **Claude Desktop** | Native support via skills-plugin, auto-detects `SKILL.md` |
| **Cursor** | Built-in Claude, same config as Claude Desktop |
| **Codex CLI** | Can directly read and execute the skill |
| **OpenClaw** | Usable if it supports the skill mechanism |
| **Pure Python** | Run scripts directly from `examples/` |

### Key Requirements

Regardless of the tool you use, **the only hard requirement is**:

1. Your tool supports reading `SKILL.md` (or an equivalent skill description file)
2. You have configured the `AGNES_IMAGE_API_KEY` environment variable

### Command-Line Usage

You can generate images directly from the terminal without any AI assistant.

**Method 1: Using `--prompt` argument**

```bash
pip install -r requirements.txt
export AGNES_IMAGE_API_KEY="sk-your-key-here"
python examples/agnes_image.py --prompt "A steampunk London Tower Bridge at sunset, cinematic lighting"
python examples/agnes_image.py --prompt "A cat on a windowsill" --size 768x1344
python examples/agnes_image.py --prompt "A sunset over the ocean" --output my_image.png
```

**Method 2: Piping input**

```bash
# Linux / macOS
echo "A sunset over the ocean" | python examples/agnes_image.py
cat prompt.txt | python examples/agnes_image.py

# Windows
type prompt.txt | python examples/agnes_image.py
Get-Content prompt.txt | python examples/agnes_image.py
```

**Method 3: Interactive mode**

```bash
python examples/agnes_image.py --interactive
```

**Method 4: Run example scripts**

```bash
python examples/movie_poster.py
python examples/image_to_image.py
```
