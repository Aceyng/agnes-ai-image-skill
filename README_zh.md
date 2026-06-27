# Agnes AI Image Skill

> 用文字描述生成高质量图片 — 支持文生图和图生图，专为 Claude 用户打造。

[English Documentation](README.md)

## 一句话介绍

这是一个让 Claude 能帮你**生成图片**的技能。你只需要用文字描述你想要的画面，Claude 就会调用 Agnes AI 的图像生成接口，为你创建一张高清图片。

## 技术信息

- **底层模型：** `agnes-image-2.1-flash`（Agnes AI 出品）
- **API 地址：** [https://apihub.agnes-ai.com](https://apihub.agnes-ai.com)
- **功能：** 文生图（Text-to-Image）、图生图（Image-to-Image）
- **许可证：** MIT

## 快速开始

### 第一步：获取 API Key

1. 打开 [https://apihub.agnes-ai.com](https://apihub.agnes-ai.com)
2. 注册/登录账号
3. 进入 Dashboard，创建一个新的 API Key
4. 复制 Key 并保存（格式类似 `sk-xxxxxxxxxxxxxxxx`）

### 第二步：安装此 Skill

安装方式任选一种即可：

#### 方式一：一键安装（推荐，需 Node.js）

如果你的电脑上安装了 Node.js 和 npm，可以用一行命令安装：

```bash
npx skills add Aceyng/agnes-ai-image-skill
```

> 安装后重启 Claude 即可使用。

#### 方式二：手动安装

1. 下载本仓库（点击绿色 Code 按钮 → Download ZIP）
2. 解压后将文件夹重命名为 `agnes-ai-image-skill`
3. 将文件夹放入 Claude 的 skills 目录：

   ```
   # macOS/Linux
   cp -r agnes-ai-image-skill ~/.claude/skills/

   # Windows
   xcopy /E /I agnes-ai-image-skill %USERPROFILE%\.claude\skills\
   ```

4. 重启 Claude

### 第三步：配置 API Key

安装完成后，在终端中设置 API Key：

```bash
# Linux / macOS
export AGNES_IMAGE_API_KEY="sk-your-key-here"

# Windows (Command Prompt)
set AGNES_IMAGE_API_KEY=sk-your-key-here

# Windows (PowerShell)
$env:AGNES_IMAGE_API_KEY="sk-your-key-here"
```

也可以创建 `.env` 文件（需安装 `python-dotenv`）：

```bash
pip install python-dotenv
```

在 `.env` 文件中写入：
```
AGNES_IMAGE_API_KEY=sk-your-key-here
```

> **安全提醒：** 永远不要把 API Key 提交到公开仓库！`.env` 文件已在 `.gitignore` 中排除。

### 第四步：在 Claude 中使用

安装配置完成后，直接在对话中描述你想生成的图片即可：

#### 示例 1：文生图

> "帮我画一张复古海报，蒸汽朋克风格的伦敦塔桥，夕阳余晖，电影质感，4K高清"

#### 示例 2：社交媒体配图

> "生成一张竖版图片，9:16比例，适合发小红书的蒸汽朋克风格城市风光"

#### 示例 3：图生图

> "把这张照片 https://example.com/photo.jpg 变成油画风格"

#### 示例 4：使用命令行脚本

```bash
# 运行示例脚本
python examples/movie_poster.py
```

## 生成的图片在哪里

### 在 Claude 对话中使用

当你通过 Claude 对话生成图片时：

1. Claude 会返回一个**图片预览**，直接在对话框中显示
2. 同时会给你一个**图片链接**，点击即可在新标签页打开查看大图
3. 部分集成方式（如 Cowork）会将图片以文件卡片形式展示，点击即可打开

### 使用命令行脚本生成

运行脚本后，生成的图片会保存在**你运行脚本的当前目录**中。

例如：

```bash
# 在项目根目录下运行
python examples/movie_poster.py

# 图片会保存在当前目录，文件名是 movie_poster.jpg
```

你也可以在脚本中自定义保存路径：

```python
# 确保目录存在后再保存
import os
os.makedirs("my_custom_path", exist_ok=True)
save_image(url, "my_custom_path/output.png")
```

### 图片格式

- 默认保存为 **PNG** 格式（无损画质）
- 也可以通过修改扩展名保存为 **JPG** 格式（体积更小）

## 支持的功能

| 功能 | 说明 | 示例 |
|------|------|------|
| **文生图** | 用文字描述生成图片 | "一只坐在向日葵田里的金毛犬，柔光，写实风格" |
| **图生图** | 基于已有图片进行风格转换 | "把这张照片变成赛博朋克夜景" |
| **自定义尺寸** | 支持多种宽高比 | 竖版 9:16、横版 16:9、正方形 1:1 |

## 提示技巧

想要生成更好的图片，试试这个公式：

```
[主体] + [场景/背景] + [风格] + [光线] + [构图] + [画质要求]
```

**差示例：** "一只猫"

**好示例：** "一只橘色虎斑猫坐在窗台上，温暖的晨光透过窗户照射进来，城市背景虚化，写实摄影风格，4K高清"

**推荐尺寸：**

| 用途 | 尺寸 | 比例 |
|------|------|------|
| 竖版社交媒体（小红书/TikTok） | `768x1344` | 9:16 |
| 标准图片 | `1024x768` | 4:3 |
| 正方形 | `1024x1024` | 1:1 |
| 横版（YouTube缩略图） | `1024x576` | 16:9 |

### 常见问题

### Q: 生成的图片质量如何？

A: 默认生成高清图片，支持最高 4K 分辨率。图片质量取决于你的描述是否足够具体和清晰。

### Q: 生成图片需要多长时间？

A: 通常需要 30 秒到 2 分钟，取决于图片复杂度和服务器负载。

### Q: 支持中文描述吗？

A: 建议使用英文描述以获得更好的效果。如果只用中文，系统会自动翻译，但可能不够精准。

### Q: 免费吗？

A: 需要使用 Agnes AI 的 API，具体资费请参考 [Agnes AI 定价页面](https://apihub.agnes-ai.com)。

### Q: 安装后找不到 skill？

A: 请确认：
1. skill 文件夹中是否包含 `SKILL.md` 文件
2. 文件夹是否放在了正确的 skills 目录下
3. 是否重启了你的 AI 助手工具（Claude Desktop / Cursor 等）

## 项目结构

```
agnes-ai-image-skill/
├── SKILL.md              # Skill 核心文档（Claude 读取此文件）
├── README.md             # 项目说明文档（你正在看的这个）
├── LICENSE               # MIT 开源许可证
├── requirements.txt      # Python 依赖声明
├── .gitignore            # Git 忽略规则
├── examples/             # 示例脚本
│   ├── agnes_image.py    # Python 封装库（带自动重试和命令行参数）
│   ├── movie_poster.py   # 电影海报生成示例
│   └── image_to_image.py # 图生图示例
└── skills/
    └── README.md         # 子目录说明
```

## 贡献

欢迎提交 Issue 和 Pull Request！

## 跨平台兼容

这个 skill 本质上是 **Python 脚本 + API 调用**，不依赖于任何特定的 AI 助手工具。
只要你的开发环境支持执行 Python 代码，就可以直接使用。

### 支持的工具

| 工具 | 说明 |
|------|------|
| **Claude Desktop** | 原生支持，通过 skills-plugin 自动识别 `SKILL.md` |
| **Cursor** | 内置 Claude，配置方式与 Claude Desktop 相同 |
| **Codex CLI** | 可直接读取并执行 skill |
| **OpenClaw** | 如果支持 skill 机制即可使用 |
| **纯 Python 脚本** | 直接运行 `examples/` 下的脚本 |

### 关键前提

不管用什么工具，**唯一的硬性要求**是：

1. 工具支持读取 `SKILL.md` 文件（或类似的 skill 描述文件）
2. 你能配置好 `AGNES_IMAGE_API_KEY` 环境变量

### 命令行使用示例

即使不用任何 AI 助手，你也可以直接在终端生成图片。

**方法 1：使用 --prompt 参数**

```bash
# 安装依赖
pip install -r requirements.txt

# 设置 API Key
export AGNES_IMAGE_API_KEY="sk-your-key-here"

# 直接传入提示词
python examples/agnes_image.py --prompt "A steampunk London Tower Bridge at sunset, cinematic lighting"

# 指定尺寸
python examples/agnes_image.py --prompt "A cat on a windowsill" --size 768x1344

# 指定输出文件名
python examples/agnes_image.py --prompt "A sunset over the ocean" --output my_image.png
```

**方法 2：通过管道输入提示词**

```bash
# 从 echo 管道输入（Linux / macOS / Git Bash）
echo "A sunset over the ocean" | python examples/agnes_image.py

# 从文件读取（Linux / macOS）
cat prompt.txt | python examples/agnes_image.py

# 从文件读取（Windows CMD）
type prompt.txt | python examples/agnes_image.py

# 从文件读取（Windows PowerShell）
Get-Content prompt.txt | python examples/agnes_image.py
```

**方法 3：交互式模式**

```bash
# 交互式提问，逐次生成
python examples/agnes_image.py --interactive
```

**方法 4：运行示例脚本**

```bash
# 电影海报示例
python examples/movie_poster.py

# 图生图示例
python examples/image_to_image.py
```
