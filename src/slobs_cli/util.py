"""module containing utility functions for Slobs CLI."""

import os

import asyncclick as click


def check_mark(ctx: click.Context, value: bool, empty_if_false: bool = False) -> str:
    """Return a check mark or cross mark based on the boolean value."""
    if empty_if_false and not value:
        return ''

    if os.getenv('NO_COLOR', '') != '' or ctx.obj['style'].name == 'no_colour':
        return '✓' if value else '✗'
    return '✅' if value else '❌'
