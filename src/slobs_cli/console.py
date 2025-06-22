"""module for console output handling."""

import asyncclick as click
from rich.console import Console

out = Console()
err = Console(stderr=True, style='bold red')


def highlight(ctx: click.Context, text: str) -> str:
    """Highlight text for console output."""
    if ctx.obj['style'].name == 'no_colour':
        return text
    return f'[{ctx.obj["style"].highlight}]{text}[/{ctx.obj["style"].highlight}]'


def warning(ctx: click.Context, text: str) -> str:
    """Format warning text for console output."""
    if ctx.obj['style'].name == 'no_colour':
        return text
    return f'[magenta]{text}[/magenta]'
