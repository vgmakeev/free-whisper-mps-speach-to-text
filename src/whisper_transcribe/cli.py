#!/usr/bin/env python3
"""
Video transcription using OpenAI Whisper with Apple Silicon MPS support.
"""

import sys
import os
import whisper
import torch
from rich.console import Console
from rich.progress import Progress, SpinnerColumn, TextColumn, BarColumn, TimeElapsedColumn
from datetime import datetime

console = Console()


def format_timestamp(seconds: float) -> str:
    """Format seconds as MM:SS."""
    mins = int(seconds // 60)
    secs = int(seconds % 60)
    return f"{mins:02d}:{secs:02d}"


def transcribe_video(video_path: str) -> None:
    """Transcribe video and save result as Markdown."""
    if not os.path.exists(video_path):
        console.print(f"[red]❌ File not found: {video_path}[/red]")
        sys.exit(1)
    
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
        task = progress.add_task("[cyan]Loading medium model...", total=None)
        model = whisper.load_model("medium", device=device)
        progress.update(task, completed=True, description="[green]✅ Model loaded")
        
        # Transcribe
        task2 = progress.add_task("[cyan]Transcribing...", total=None)
        result = model.transcribe(
            video_path,
            language="ru",
            initial_prompt="Это деловая встреча на русском языке. Участники обсуждают проекты, задачи и сроки.",
            verbose=False
        )
        progress.update(task2, completed=True, description="[green]✅ Transcription complete")
    
    # Build output path
    video_dir = os.path.dirname(os.path.abspath(video_path))
    transcripts_dir = os.path.join(video_dir, "Transcripts")
    os.makedirs(transcripts_dir, exist_ok=True)
    
    date_str = datetime.now().strftime("%Y-%m-%d")
    video_name = os.path.splitext(os.path.basename(video_path))[0]
    output_file = os.path.join(transcripts_dir, f"{date_str} {video_name} Transcript.md")
    
    # Calculate duration
    if result["segments"]:
        duration_sec = result["segments"][-1]["end"]
        duration_min = duration_sec / 60
    else:
        duration_min = 0
    
    # Write Markdown
    with open(output_file, "w", encoding="utf-8") as f:
        f.write("---\n")
        f.write("type: transcript\n")
        f.write(f"date: {date_str}\n")
        f.write(f"source: \"[[{os.path.basename(video_path)}]]\"\n")
        f.write(f"duration: {duration_min:.1f} мин\n")
        f.write(f"device: {device}\n")
        f.write("model: medium\n")
        f.write("---\n\n")
        f.write(f"# Транскрипт: {video_name}\n\n")
        
        for segment in result["segments"]:
            timestamp = format_timestamp(segment["start"])
            text = segment["text"].strip()
            f.write(f"**[{timestamp}]** {text}\n\n")
    
    console.print(f"\n[green]✅ Saved:[/green] {output_file}")
    console.print(f"[dim]Duration: {duration_min:.1f} min | Segments: {len(result['segments'])}[/dim]")


def main() -> None:
    """CLI entry point."""
    if len(sys.argv) < 2:
        console.print("[yellow]Usage: transcribe <video_path>[/yellow]")
        console.print("[dim]Example: transcribe meeting.webm[/dim]")
        sys.exit(1)
    
    transcribe_video(sys.argv[1])


if __name__ == "__main__":
    main()
