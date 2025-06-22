"""module containing utility functions for Slobs CLI."""

import os

import asyncclick as click


def check_mark(ctx: click.Context, value: bool, empty_if_false: bool = False) -> str:
    """Return a check mark or cross mark based on the boolean value."""
    if empty_if_false and not value:
        return ''

    # rich gracefully handles the absence of colour throughout the rest of the application,
    # but here we must handle it manually.
    # If NO_COLOR is set, we return plain text symbols.
    # Otherwise, we return coloured symbols.
    if os.getenv('NO_COLOR', '') != '':
        return '✓' if value else '✗'
    return '✅' if value else '❌'
