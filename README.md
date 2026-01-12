# 🎙️ Whisper Transcribe

**Free, offline speech-to-text for Mac with Apple Silicon.**

Uses OpenAI Whisper running 100% locally with GPU acceleration (MPS).

---

## 📦 Install

### Option 1: One-shot with uvx (recommended)

```bash
# Using git URL (works without publishing to PyPI)
uvx git+https://github.com/vgmakeev/free-whisper-mps-speach-to-text.git meeting.mp4

# Or if published to PyPI:
uvx whisper-transcribe meeting.mp4
```

### Option 2: Install globally

```bash
uv tool install git+https://github.com/vgmakeev/free-whisper-mps-speach-to-text.git
```

Then use:
```bash
transcribe meeting.mp4
```

---

## 🚀 Use as CLI

```bash
# With uvx (one-shot, no installation needed)
uvx git+https://github.com/vgmakeev/free-whisper-mps-speach-to-text.git meeting.mp4

# Or if installed globally
transcribe meeting.mp4
```

### Options

```bash
# With uvx
uvx git+https://github.com/vgmakeev/free-whisper-mps-speach-to-text.git file.mp3 --model large
uvx git+https://github.com/vgmakeev/free-whisper-mps-speach-to-text.git file.mp3 --lang en
uvx git+https://github.com/vgmakeev/free-whisper-mps-speach-to-text.git file.mp3 --output out.md

# Or if installed globally
transcribe file.mp3 --model large    # Better quality
transcribe file.mp3 --lang en        # Specify language
transcribe file.mp3 --output out.md  # Custom output path
transcribe file.mp3 --prompt "..."   # Context hint
```

---

## 🤖 Use as MCP Server

Add to your Claude/Cursor config:

### Option 1: With uvx (no installation needed)

```json
{
  "mcpServers": {
    "whisper": {
      "command": "uvx",
      "args": [
        "git+https://github.com/vgmakeev/free-whisper-mps-speach-to-text.git",
        "transcribe-mcp"
      ]
    }
  }
}
```

### Option 2: With global installation

```json
{
  "mcpServers": {
    "whisper": {
      "command": "transcribe-mcp"
    }
  }
}
```

Then ask Claude:
> "Transcribe ~/Downloads/meeting.mp4"

### Available Tools

| Tool | Description |
|------|-------------|
| `transcribe` | Transcribe audio/video file |
| `transcribe_info` | List supported formats and models |

---

## 📋 Supported Formats

**Audio:** mp3, wav, m4a, flac, ogg, aac  
**Video:** mp4, webm, mkv, avi, mov

---

## 🧠 Models

| Model | Size | Speed | Quality |
|-------|------|-------|---------|
| tiny | 39 MB | ⚡⚡⚡ | Basic |
| base | 74 MB | ⚡⚡ | Good |
| small | 244 MB | ⚡ | Better |
| **medium** | 769 MB | 🐢 | **Recommended** |
| large | 1.5 GB | 🐢🐢 | Best |

Models download automatically on first use.

---

## 📜 License

MIT
