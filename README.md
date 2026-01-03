# 🎙️ Whisper Transcribe

**Free, fast, offline speech-to-text for Mac with Apple Silicon.**

Convert any audio or video file to text using OpenAI's Whisper model — running 100% locally on your Mac with GPU acceleration via Metal Performance Shaders (MPS).

> ✅ No API keys · ✅ No cloud upload · ✅ No costs · ✅ Works offline

---

## ⚡ Quick Start

**1. Install [uv](https://docs.astral.sh/uv/getting-started/installation/) (if you haven't):**

```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

**2. Install the tool:**

```bash
uv tool install git+https://github.com/vgmakeev/free-whisper-mps-speach-to-text.git
```

**3. Transcribe!**

```bash
transcribe meeting.mp4
```

That's it! The transcript will be saved as a Markdown file next to your video.

---

## 🎯 Features

| Feature | Description |
|---------|-------------|
| 🚀 **Apple Silicon optimized** | Uses MPS for GPU acceleration on M1/M2/M3/M4 |
| 🌍 **99 languages** | Auto-detects language or specify manually |
| 📁 **Any format** | MP3, WAV, M4A, MP4, WebM, MKV, and more |
| 📝 **Markdown output** | Clean format with timestamps |
| 🔒 **100% private** | Everything runs locally on your Mac |
| 💰 **Completely free** | No API costs, no subscriptions |

---

## 📖 Usage

```bash
transcribe <file> [options]
```

### Options

| Option | Description | Default |
|--------|-------------|---------|
| `-m, --model` | Model size: `tiny`, `base`, `small`, `medium`, `large` | `medium` |
| `-l, --lang` | Language code (`en`, `ru`, `es`, etc.) | auto-detect |
| `-o, --output` | Custom output path | `./Transcripts/<name>.md` |
| `-p, --prompt` | Context hint for better accuracy | none |

### Examples

```bash
# Basic usage (auto-detect language)
transcribe podcast.mp3

# Use larger model for better accuracy
transcribe interview.wav --model large

# Specify language for faster processing
transcribe meeting.webm --lang en

# Add context for domain-specific terms
transcribe lecture.mp4 --prompt "Machine learning lecture about neural networks"

# Custom output location
transcribe call.m4a --output ~/Documents/call-notes.md
```

---

## 🧠 Models

Models are downloaded automatically on first use (~1-2 min).

| Model | Size | Speed* | Best for |
|-------|------|--------|----------|
| `tiny` | 39 MB | ~10x | Quick drafts |
| `base` | 74 MB | ~7x | Casual use |
| `small` | 244 MB | ~4x | Good balance |
| **`medium`** | 769 MB | ~2x | **Recommended** |
| `large` | 1.5 GB | 1x | Maximum accuracy |

*Speed relative to audio duration on Apple Silicon

---

## 📄 Output Format

Transcripts are saved as Markdown with metadata:

```markdown
---
type: transcript
date: 2025-01-03
source: "[[meeting.mp4]]"
duration: 45.2 min
language: en
model: medium
---

# Transcript: meeting

**[00:00]** Hello everyone, let's get started...

**[00:15]** Today we'll discuss the quarterly results...
```

---

## 🔧 Management

```bash
# Update to latest version
uv tool upgrade whisper-transcribe

# Uninstall
uv tool uninstall whisper-transcribe

# Clear downloaded models (to free ~1.5 GB)
rm -rf ~/.cache/whisper
```

---

## 💻 Requirements

- macOS with Apple Silicon (M1/M2/M3/M4)
- Python 3.12+
- [uv](https://docs.astral.sh/uv/) package manager
- ~2 GB free disk space (for models)

---

## 🤔 FAQ

<details>
<summary><b>Does it work on Intel Macs?</b></summary>

Yes, but without GPU acceleration. It will use CPU which is significantly slower.
</details>

<details>
<summary><b>How accurate is it?</b></summary>

Whisper is one of the best open-source speech recognition models. The `medium` model provides excellent accuracy for most use cases. Use `large` for critical transcriptions.
</details>

<details>
<summary><b>Can I transcribe in multiple languages?</b></summary>

Yes! Whisper supports 99 languages. It auto-detects the language, or you can specify it with `--lang`.
</details>

<details>
<summary><b>How long does transcription take?</b></summary>

With `medium` model on Apple Silicon: roughly 4-5 minutes for a 1-hour recording.
</details>

---

## 📜 License

MIT — use freely for personal and commercial projects.

---

<p align="center">
  <b>⭐ Star this repo if you find it useful!</b>
</p>
