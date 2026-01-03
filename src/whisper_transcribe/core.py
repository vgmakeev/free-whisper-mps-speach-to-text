"""
Core transcription logic using OpenAI Whisper.
"""

import os
from dataclasses import dataclass
from datetime import datetime

import torch
import whisper

SUPPORTED_FORMATS = {
    ".mp3", ".wav", ".m4a", ".flac", ".ogg", ".wma", ".aac",
    ".mp4", ".webm", ".mkv", ".avi", ".mov",
}
AVAILABLE_MODELS = ["tiny", "base", "small", "medium", "large", "large-v2", "large-v3"]


@dataclass
class TranscriptSegment:
    """A single segment of transcription."""
    start: float
    end: float
    text: str


@dataclass
class TranscriptResult:
    """Result of transcription."""
    text: str
    segments: list[TranscriptSegment]
    language: str
    duration_min: float
    device: str
    model: str


def format_timestamp(seconds: float) -> str:
    """Format seconds as MM:SS."""
    mins = int(seconds // 60)
    secs = int(seconds % 60)
    return f"{mins:02d}:{secs:02d}"


def get_device() -> str:
    """Detect best available device."""
    if torch.backends.mps.is_available():
        return "mps"
    return "cpu"


def transcribe_file(
    file_path: str,
    model_name: str = "medium",
    language: str | None = None,
    prompt: str | None = None,
    on_progress: callable = None,
) -> TranscriptResult:
    """
    Transcribe audio/video file.
    
    Args:
        file_path: Path to audio/video file
        model_name: Whisper model name
        language: Language code (auto-detect if None)
        prompt: Initial prompt for context
        on_progress: Optional callback(stage: str, message: str)
    
    Returns:
        TranscriptResult with text, segments, and metadata
    
    Raises:
        FileNotFoundError: If file doesn't exist
        ValueError: If model is invalid
    """
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"File not found: {file_path}")
    
    if model_name not in AVAILABLE_MODELS:
        raise ValueError(f"Invalid model: {model_name}. Available: {AVAILABLE_MODELS}")
    
    device = get_device()
    
    if on_progress:
        on_progress("device", f"Using {device.upper()}")
    
    # Load model
    if on_progress:
        on_progress("loading", f"Loading {model_name} model...")
    
    model = whisper.load_model(model_name, device=device)
    
    if on_progress:
        on_progress("loaded", f"Model {model_name} loaded")
    
    # Transcribe
    if on_progress:
        on_progress("transcribing", "Transcribing...")
    
    transcribe_options = {"verbose": False}
    if language:
        transcribe_options["language"] = language
    if prompt:
        transcribe_options["initial_prompt"] = prompt
    
    result = model.transcribe(file_path, **transcribe_options)
    
    if on_progress:
        on_progress("complete", "Transcription complete")
    
    # Parse segments
    segments = [
        TranscriptSegment(
            start=seg["start"],
            end=seg["end"],
            text=seg["text"].strip(),
        )
        for seg in result["segments"]
    ]
    
    # Calculate duration
    duration_min = segments[-1].end / 60 if segments else 0
    
    # Full text
    full_text = result.get("text", "").strip()
    
    return TranscriptResult(
        text=full_text,
        segments=segments,
        language=result.get("language", "unknown"),
        duration_min=duration_min,
        device=device,
        model=model_name,
    )


def result_to_markdown(
    result: TranscriptResult,
    source_filename: str,
    date_str: str | None = None,
) -> str:
    """Convert TranscriptResult to Markdown string."""
    if date_str is None:
        date_str = datetime.now().strftime("%Y-%m-%d")
    
    file_name = os.path.splitext(source_filename)[0]
    
    lines = [
        "---",
        "type: transcript",
        f"date: {date_str}",
        f"source: \"[[{source_filename}]]\"",
        f"duration: {result.duration_min:.1f} min",
        f"language: {result.language}",
        f"device: {result.device}",
        f"model: {result.model}",
        "---",
        "",
        f"# Transcript: {file_name}",
        "",
    ]
    
    for segment in result.segments:
        timestamp = format_timestamp(segment.start)
        lines.append(f"**[{timestamp}]** {segment.text}")
        lines.append("")
    
    return "\n".join(lines)


def save_transcript(
    result: TranscriptResult,
    source_path: str,
    output_path: str | None = None,
) -> str:
    """
    Save transcript to Markdown file.
    
    Args:
        result: TranscriptResult to save
        source_path: Original audio/video file path
        output_path: Custom output path (auto-generate if None)
    
    Returns:
        Path to saved file
    """
    if output_path:
        output_file = output_path
        output_dir = os.path.dirname(os.path.abspath(output_file))
        if output_dir:
            os.makedirs(output_dir, exist_ok=True)
    else:
        file_dir = os.path.dirname(os.path.abspath(source_path))
        transcripts_dir = os.path.join(file_dir, "Transcripts")
        os.makedirs(transcripts_dir, exist_ok=True)
        
        date_str = datetime.now().strftime("%Y-%m-%d")
        file_name = os.path.splitext(os.path.basename(source_path))[0]
        output_file = os.path.join(transcripts_dir, f"{date_str} {file_name} Transcript.md")
    
    source_filename = os.path.basename(source_path)
    markdown = result_to_markdown(result, source_filename)
    
    with open(output_file, "w", encoding="utf-8") as f:
        f.write(markdown)
    
    return output_file
