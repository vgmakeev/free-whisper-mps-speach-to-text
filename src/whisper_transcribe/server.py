#!/usr/bin/env python3
"""
MCP server for audio/video transcription using MLX Whisper (Apple Silicon optimized).
"""

import os
import logging
from typing import Any

from mcp.server import Server
from mcp.server.stdio import stdio_server
from mcp.types import Tool, TextContent

from .core import (
    AVAILABLE_MODELS,
    SUPPORTED_FORMATS,
    transcribe_file,
    save_transcript,
    result_to_markdown,
)

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("whisper-transcribe")

# Create MCP server
server = Server("whisper-transcribe")


@server.list_tools()
async def list_tools() -> list[Tool]:
    """List available tools."""
    return [
        Tool(
            name="transcribe",
            description="""Transcribe audio/video file to text using MLX Whisper.

Supports formats: mp3, wav, m4a, flac, ogg, mp4, webm, mkv, avi, mov.
Optimized for Apple Silicon (MLX acceleration).

The transcript is saved as a Markdown file next to the source file (in ./Transcripts/ folder)
and the content is also returned directly.""",
            inputSchema={
                "type": "object",
                "properties": {
                    "file": {
                        "type": "string",
                        "description": "Absolute path to audio/video file",
                    },
                    "model": {
                        "type": "string",
                        "enum": list(AVAILABLE_MODELS.keys()),
                        "default": "medium",
                        "description": "Whisper model size (tiny/base/small/medium/large/turbo)",
                    },
                    "language": {
                        "type": "string",
                        "description": "Language code (e.g., 'ru', 'en'). Auto-detect if not specified.",
                    },
                    "prompt": {
                        "type": "string",
                        "description": "Initial prompt to guide transcription style/context",
                    },
                    "output": {
                        "type": "string",
                        "description": "Custom output file path. Default: ./Transcripts/<date> <name> Transcript.md",
                    },
                    "save_file": {
                        "type": "boolean",
                        "default": True,
                        "description": "Whether to save transcript to file (default: true)",
                    },
                },
                "required": ["file"],
            },
        ),
        Tool(
            name="transcribe_info",
            description="Get information about available models and supported formats.",
            inputSchema={
                "type": "object",
                "properties": {},
            },
        ),
    ]


@server.call_tool()
async def call_tool(name: str, arguments: dict[str, Any]) -> list[TextContent]:
    """Handle tool calls."""
    
    if name == "transcribe_info":
        info = f"""# Whisper Transcribe (MLX)

## Supported Formats
**Audio:** {', '.join(sorted(f for f in SUPPORTED_FORMATS if f in {'.mp3', '.wav', '.m4a', '.flac', '.ogg', '.wma', '.aac'}))}
**Video:** {', '.join(sorted(f for f in SUPPORTED_FORMATS if f in {'.mp4', '.webm', '.mkv', '.avi', '.mov'}))}

## Available Models
| Model | Speed | Quality |
|-------|-------|---------|
| tiny | ⚡⚡⚡ | Basic |
| base | ⚡⚡ | Good |
| small | ⚡ | Better |
| **medium** | 🐢 | Great (recommended) |
| large | 🐢🐢 | Best |
| **turbo** | ⚡⚡ | Great (fast) |

Models are downloaded automatically from Hugging Face on first use.
Optimized for Apple Silicon using MLX.
"""
        return [TextContent(type="text", text=info)]
    
    if name == "transcribe":
        file_path = arguments.get("file")
        model_name = arguments.get("model", "medium")
        language = arguments.get("language")
        prompt = arguments.get("prompt")
        output = arguments.get("output")
        save_file = arguments.get("save_file", True)
        
        if not file_path:
            return [TextContent(type="text", text="❌ Error: 'file' parameter is required")]
        
        # Expand path
        file_path = os.path.expanduser(file_path)
        
        if not os.path.exists(file_path):
            return [TextContent(type="text", text=f"❌ Error: File not found: {file_path}")]
        
        logger.info(f"Transcribing: {file_path} with model {model_name}")
        
        try:
            # Progress callback for logging
            def on_progress(stage: str, message: str) -> None:
                logger.info(f"[{stage}] {message}")
            
            result = transcribe_file(
                file_path=file_path,
                model_name=model_name,
                language=language,
                prompt=prompt,
                on_progress=on_progress,
            )
            
            # Generate markdown content
            source_filename = os.path.basename(file_path)
            markdown = result_to_markdown(result, source_filename)
            
            # Save file if requested
            output_info = ""
            if save_file:
                if output:
                    output = os.path.expanduser(output)
                output_file = save_transcript(
                    result=result,
                    source_path=file_path,
                    output_path=output,
                )
                output_info = f"\n\n---\n✅ Saved to: {output_file}"
            
            response = f"""{markdown}{output_info}

---
**Stats:** {result.duration_min:.1f} min | {len(result.segments)} segments | Language: {result.language} | Device: {result.device}"""
            
            return [TextContent(type="text", text=response)]
            
        except FileNotFoundError as e:
            return [TextContent(type="text", text=f"❌ Error: {e}")]
        except ValueError as e:
            return [TextContent(type="text", text=f"❌ Error: {e}")]
        except Exception as e:
            logger.exception("Transcription failed")
            return [TextContent(type="text", text=f"❌ Error: {e}")]
    
    return [TextContent(type="text", text=f"❌ Unknown tool: {name}")]


async def run_server():
    """Run the MCP server."""
    async with stdio_server() as (read_stream, write_stream):
        await server.run(
            read_stream,
            write_stream,
            server.create_initialization_options(),
        )


def main():
    """Entry point for MCP server."""
    import asyncio
    asyncio.run(run_server())


if __name__ == "__main__":
    main()
