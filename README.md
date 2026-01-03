# 🎙️ Whisper Transcribe

**Free, offline speech-to-text for Mac with Apple Silicon.**

Uses OpenAI Whisper running 100% locally with GPU acceleration (MPS).

---

## 📦 Install

```bash
uv tool install git+https://github.com/vgmakeev/free-whisper-mps-speach-to-text.git
```

---

## 🚀 Use as CLI

```bash
transcribe meeting.mp4
```

### Options

```bash
transcribe file.mp3 --model large    # Better quality
transcribe file.mp3 --lang en        # Specify language
transcribe file.mp3 --output out.md  # Custom output path
transcribe file.mp3 --prompt "..."   # Context hint
```

---

## 🤖 Use as MCP Server

Add to your Claude/Cursor config:

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
