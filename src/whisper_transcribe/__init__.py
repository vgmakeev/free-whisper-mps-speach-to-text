"""Whisper Transcribe - Audio/video transcription using OpenAI Whisper."""

__version__ = "0.2.0"

from .core import (
    AVAILABLE_MODELS,
    SUPPORTED_FORMATS,
    TranscriptResult,
    TranscriptSegment,
    transcribe_file,
    save_transcript,
    result_to_markdown,
)
