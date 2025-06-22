"""module for console output handling."""

import os

import asyncclick as click
from rich.console import Console

out = Console()
err = Console(
    stderr=True, style='bold red' if os.getenv('NO_COLOR', '') != '' else 'none'
)


def highlight(ctx: click.Context, text: str) -> str:
    """Highlight text for console output."""
    return f'[{ctx.obj["style"].highlight}]{text}[/{ctx.obj["style"].highlight}]'


def warning(ctx: click.Context, text: str) -> str:
    """Format warning text for console output."""
    return f'[{ctx.obj["style"].warning}]{text}[/{ctx.obj["style"].warning}]'
