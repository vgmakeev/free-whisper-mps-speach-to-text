# 🎙️ Whisper Transcribe

**Free, offline speech-to-text for Mac with Apple Silicon.**

Uses MLX Whisper running 100% locally with native Apple Silicon GPU acceleration.

---

## 📦 Install

### Option 1: One-shot with uvx (recommended)

```bash
uvx git+https://github.com/vgmakeev/free-whisper-mps-speach-to-text.git meeting.mp4
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
transcribe meeting.mp4
transcribe podcast.mp3 --model large --lang en
transcribe interview.m4a --output ./result.md
transcribe call.wav --prompt "Technical discussion about Python"
```

### Options

| Option | Description |
|--------|-------------|
| `-m, --model` | Model: tiny, base, small, **medium** (default), large, turbo |
| `-l, --lang` | Language code (e.g., ru, en). Auto-detect if not specified |
| `-o, --output` | Custom output path |
| `-p, --prompt` | Context hint for better accuracy |

---

## 🤖 Use as MCP Server

Add to your Claude/Cursor config:

### With uvx (no installation needed)

```json
{
  "mcpServers": {
    "whisper": {
      "command": "uvx",
      "args": [
        "--from",
        "git+https://github.com/vgmakeev/free-whisper-mps-speach-to-text.git",
        "transcribe-mcp"
      ]
    }
  }
}
```

### With global installation

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

| Model | Speed | Quality |
|-------|-------|---------|
| tiny | ⚡⚡⚡ | Basic |
| base | ⚡⚡ | Good |
| small | ⚡ | Better |
| **medium** | 🐢 | **Recommended** |
| large | 🐢🐢 | Best |
| **turbo** | ⚡⚡ | Great (fast + quality) |

Models download automatically from Hugging Face on first use.

---

## 🍎 Why MLX?

This tool uses [MLX Whisper](https://github.com/ml-explore/mlx-examples) — Apple's native ML framework optimized for Apple Silicon. Benefits:

- **Native GPU acceleration** — uses Metal directly, no PyTorch/MPS issues
- **Fast** — optimized for M1/M2/M3 chips
- **Reliable** — no NaN errors or compatibility problems

---

## 📜 License

MIT
