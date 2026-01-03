#!/usr/bin/env python3
"""
Audio/video transcription using OpenAI Whisper with Apple Silicon MPS support.
"""

import argparse
import sys
import os
import whisper
import torch
from rich.console import Console
from rich.progress import Progress, SpinnerColumn, TextColumn, BarColumn, TimeElapsedColumn
from datetime import datetime

console = Console()

SUPPORTED_FORMATS = {".mp3", ".wav", ".m4a", ".flac", ".ogg", ".wma", ".aac", ".mp4", ".webm", ".mkv", ".avi", ".mov"}
AVAILABLE_MODELS = ["tiny", "base", "small", "medium", "large", "large-v2", "large-v3"]
DEFAULT_PROMPT = "Это деловая встреча на русском языке. Участники обсуждают проекты, задачи и сроки."


def format_timestamp(seconds: float) -> str:
    """Format seconds as MM:SS."""
    mins = int(seconds // 60)
    secs = int(seconds % 60)
    return f"{mins:02d}:{secs:02d}"


def transcribe(
    file_path: str,
    model_name: str = "medium",
    language: str | None = None,
    prompt: str | None = None,
    output: str | None = None,
) -> None:
    """Transcribe audio/video file and save result as Markdown."""
    
    # Validate file exists
    if not os.path.exists(file_path):
        console.print(f"[red]❌ File not found: {file_path}[/red]")
        sys.exit(1)
    
    # Validate format
    ext = os.path.splitext(file_path)[1].lower()
    if ext not in SUPPORTED_FORMATS:
        console.print(f"[yellow]⚠️ Unknown format {ext}, attempting anyway...[/yellow]")
    
    # Detect device
    if torch.backends.mps.is_available():
        device = "mps"
        console.print("[green]🚀 Using MPS (Apple Silicon)[/green]")
    else:
        device = "cpu"
        console.print("[yellow]⚠️ MPS unavailable, using CPU[/yellow]")
    
    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        BarColumn(),
        TimeElapsedColumn(),
        console=console
    ) as progress:
        
        # Load model
        task = progress.add_task(f"[cyan]Loading {model_name} model...", total=None)
        model = whisper.load_model(model_name, device=device)
        progress.update(task, completed=True, description=f"[green]✅ Model {model_name} loaded")
        
        # Transcribe
        task2 = progress.add_task("[cyan]Transcribing...", total=None)
        
        transcribe_options = {"verbose": False}
        if language:
            transcribe_options["language"] = language
        if prompt:
            transcribe_options["initial_prompt"] = prompt
        
        result = model.transcribe(file_path, **transcribe_options)
        progress.update(task2, completed=True, description="[green]✅ Transcription complete")
    
    # Detected language
    detected_lang = result.get("language", "unknown")
    
    # Build output path
    if output:
        output_file = output
        os.makedirs(os.path.dirname(os.path.abspath(output_file)) or ".", exist_ok=True)
    else:
        file_dir = os.path.dirname(os.path.abspath(file_path))
        transcripts_dir = os.path.join(file_dir, "Transcripts")
        os.makedirs(transcripts_dir, exist_ok=True)
        
        date_str = datetime.now().strftime("%Y-%m-%d")
        file_name = os.path.splitext(os.path.basename(file_path))[0]
        output_file = os.path.join(transcripts_dir, f"{date_str} {file_name} Transcript.md")
    
    # Calculate duration
    if result["segments"]:
        duration_sec = result["segments"][-1]["end"]
        duration_min = duration_sec / 60
    else:
        duration_min = 0
    
    # Write Markdown
    date_str = datetime.now().strftime("%Y-%m-%d")
    file_name = os.path.splitext(os.path.basename(file_path))[0]
    
    with open(output_file, "w", encoding="utf-8") as f:
        f.write("---\n")
        f.write("type: transcript\n")
        f.write(f"date: {date_str}\n")
        f.write(f"source: \"[[{os.path.basename(file_path)}]]\"\n")
        f.write(f"duration: {duration_min:.1f} min\n")
        f.write(f"language: {detected_lang}\n")
        f.write(f"device: {device}\n")
        f.write(f"model: {model_name}\n")
        f.write("---\n\n")
        f.write(f"# Transcript: {file_name}\n\n")
        
        for segment in result["segments"]:
            timestamp = format_timestamp(segment["start"])
            text = segment["text"].strip()
            f.write(f"**[{timestamp}]** {text}\n\n")
    
    console.print(f"\n[green]✅ Saved:[/green] {output_file}")
    console.print(f"[dim]Duration: {duration_min:.1f} min | Segments: {len(result['segments'])} | Language: {detected_lang}[/dim]")


def main() -> None:
    """CLI entry point."""
    parser = argparse.ArgumentParser(
        prog="transcribe",
        description="Transcribe audio/video files using OpenAI Whisper with Apple Silicon MPS support.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  transcribe meeting.webm
  transcribe podcast.mp3 --model large --lang en
  transcribe interview.m4a --output ./result.md
  transcribe call.wav --prompt "Technical discussion about Python"
        """,
    )
    
    parser.add_argument(
        "file",
        help="Path to audio/video file (mp3, wav, m4a, mp4, webm, etc.)",
    )
    parser.add_argument(
        "-m", "--model",
        choices=AVAILABLE_MODELS,
        default="medium",
        help="Whisper model to use (default: medium)",
    )
    parser.add_argument(
        "-l", "--lang",
        default=None,
        help="Language code (e.g., ru, en). Auto-detect if not specified.",
    )
    parser.add_argument(
        "-o", "--output",
        default=None,
        help="Output file path. Default: ./Transcripts/<date> <name> Transcript.md",
    )
    parser.add_argument(
        "-p", "--prompt",
        default=None,
        help="Initial prompt to guide transcription style/context.",
    )
    
    args = parser.parse_args()
    
    transcribe(
        file_path=args.file,
        model_name=args.model,
        language=args.lang,
        prompt=args.prompt,
        output=args.output,
    )


if __name__ == "__main__":
    main()
