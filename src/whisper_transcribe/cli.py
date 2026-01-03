#!/usr/bin/env python3
"""
CLI for audio/video transcription using OpenAI Whisper.
"""

import argparse
import sys
import os

from rich.console import Console
from rich.progress import Progress, SpinnerColumn, TextColumn, BarColumn, TimeElapsedColumn

from .core import (
    AVAILABLE_MODELS,
    SUPPORTED_FORMATS,
    transcribe_file,
    save_transcript,
)

console = Console()


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
    
    # Validate file exists
    if not os.path.exists(args.file):
        console.print(f"[red]❌ File not found: {args.file}[/red]")
        sys.exit(1)
    
    # Validate format
    ext = os.path.splitext(args.file)[1].lower()
    if ext not in SUPPORTED_FORMATS:
        console.print(f"[yellow]⚠️ Unknown format {ext}, attempting anyway...[/yellow]")
    
    # Progress tracking
    progress_ctx = None
    task_id = None
    
    def on_progress(stage: str, message: str) -> None:
        nonlocal progress_ctx, task_id
        
        if stage == "device":
            if "mps" in message.lower():
                console.print("[green]🚀 Using MPS (Apple Silicon)[/green]")
            else:
                console.print("[yellow]⚠️ MPS unavailable, using CPU[/yellow]")
        elif stage == "loading":
            progress_ctx = Progress(
                SpinnerColumn(),
                TextColumn("[progress.description]{task.description}"),
                BarColumn(),
                TimeElapsedColumn(),
                console=console,
            )
            progress_ctx.start()
            task_id = progress_ctx.add_task(f"[cyan]{message}", total=None)
        elif stage == "loaded":
            if progress_ctx and task_id is not None:
                progress_ctx.update(task_id, completed=True, description=f"[green]✅ {message}")
        elif stage == "transcribing":
            if progress_ctx:
                task_id = progress_ctx.add_task(f"[cyan]{message}", total=None)
        elif stage == "complete":
            if progress_ctx and task_id is not None:
                progress_ctx.update(task_id, completed=True, description=f"[green]✅ {message}")
                progress_ctx.stop()
    
    try:
        result = transcribe_file(
            file_path=args.file,
            model_name=args.model,
            language=args.lang,
            prompt=args.prompt,
            on_progress=on_progress,
        )
        
        output_file = save_transcript(
            result=result,
            source_path=args.file,
            output_path=args.output,
        )
        
        console.print(f"\n[green]✅ Saved:[/green] {output_file}")
        console.print(f"[dim]Duration: {result.duration_min:.1f} min | Segments: {len(result.segments)} | Language: {result.language}[/dim]")
        
    except FileNotFoundError as e:
        console.print(f"[red]❌ {e}[/red]")
        sys.exit(1)
    except ValueError as e:
        console.print(f"[red]❌ {e}[/red]")
        sys.exit(1)
    except Exception as e:
        if progress_ctx:
            progress_ctx.stop()
        console.print(f"[red]❌ Error: {e}[/red]")
        sys.exit(1)


if __name__ == "__main__":
    main()
