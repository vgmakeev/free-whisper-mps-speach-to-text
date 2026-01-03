# 🎙️ Whisper Transcribe

Audio/video transcription using OpenAI Whisper with Apple Silicon MPS acceleration.

## Installation

```bash
uv tool install ~/.dev/whisper-transcribe
```

Or run without installing:

```bash
uvx --from ~/.dev/whisper-transcribe transcribe file.mp3
```

## Usage

```bash
transcribe <file> [options]
```

### Options

| Option | Description | Default |
|--------|-------------|---------|
| `-m, --model` | Whisper model (tiny/base/small/medium/large/large-v2/large-v3) | medium |
| `-l, --lang` | Language code (ru, en, etc.) | auto-detect |
| `-o, --output` | Output file path | `./Transcripts/<date> <name> Transcript.md` |
| `-p, --prompt` | Initial prompt for context | none |

### Examples

```bash
# Basic transcription (auto-detect language)
transcribe meeting.webm

# Use large model for better quality
transcribe podcast.mp3 --model large

# Specify language
transcribe interview.m4a --lang en

# Custom output path
transcribe call.wav --output ./my-transcript.md

# With context prompt
transcribe lecture.mp4 --prompt "Technical lecture about machine learning"
```

## Supported Formats

**Audio:** mp3, wav, m4a, flac, ogg, wma, aac  
**Video:** mp4, webm, mkv, avi, mov

## Models

| Model | Size | Speed | Quality |
|-------|------|-------|---------|
| tiny | 39 MB | Fastest | Basic |
| base | 74 MB | Fast | Good |
| small | 244 MB | Medium | Better |
| **medium** | 769 MB | Slower | Great |
| large | 1.5 GB | Slow | Best |
| large-v3 | 1.5 GB | Slow | Best |

Models are downloaded automatically to `~/.cache/whisper/` on first use.

## Output

Markdown file with YAML frontmatter:

```markdown
---
type: transcript
date: 2025-01-03
source: "[[meeting.webm]]"
duration: 45.2 min
language: ru
device: mps
model: medium
---

# Transcript: meeting

**[00:00]** Hello everyone...

**[00:15]** Let's discuss the project...
```

## Management

```bash
# Upgrade
uv tool upgrade whisper-transcribe

# Uninstall
uv tool uninstall whisper-transcribe

# Clear model cache
rm -rf ~/.cache/whisper
```
