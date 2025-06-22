"""module for managing the replay buffer in Slobs CLI."""

import asyncclick as click
from anyio import create_task_group
from pyslobs import StreamingService

from . import console
from .cli import cli
from .errors import SlobsCliError


@cli.group()
def stream():
    """Manage streaming in Slobs CLI."""


@stream.command()
@click.pass_context
async def start(ctx: click.Context):
    """Start the stream."""
    conn = ctx.obj['connection']
    ss = StreamingService(conn)

    async def _run():
        model = await ss.get_model()
        active = model.streaming_status != 'offline'

        if active:
            conn.close()
            raise SlobsCliError('Stream is already active.')

        await ss.toggle_streaming()
        console.out.print('Stream started.')
        conn.close()

    try:
        async with create_task_group() as tg:
            tg.start_soon(conn.background_processing)
            tg.start_soon(_run)
    except* SlobsCliError as excgroup:
        raisable = next(iter(excgroup.exceptions))
        raise raisable


@stream.command()
@click.pass_context
async def stop(ctx: click.Context):
    """Stop the stream."""
    conn = ctx.obj['connection']
    ss = StreamingService(conn)

    async def _run():
        model = await ss.get_model()
        active = model.streaming_status != 'offline'

        if not active:
            conn.close()
            raise SlobsCliError('Stream is already inactive.')

        await ss.toggle_streaming()
        console.out.print('Stream stopped.')
        conn.close()

    try:
        async with create_task_group() as tg:
            tg.start_soon(conn.background_processing)
            tg.start_soon(_run)
    except* SlobsCliError as excgroup:
        raisable = next(iter(excgroup.exceptions))
        raise raisable


@stream.command()
@click.pass_context
async def status(ctx: click.Context):
    """Get the current stream status."""
    conn = ctx.obj['connection']
    ss = StreamingService(conn)

    async def _run():
        model = await ss.get_model()
        active = model.streaming_status != 'offline'

        if active:
            console.out.print('Stream is currently active.')
        else:
            console.out.print('Stream is currently inactive.')
        conn.close()

    async with create_task_group() as tg:
        tg.start_soon(conn.background_processing)
        tg.start_soon(_run)


@stream.command()
@click.pass_context
async def toggle(ctx: click.Context):
    """Toggle the stream status."""
    conn = ctx.obj['connection']
    ss = StreamingService(conn)

    async def _run():
        model = await ss.get_model()
        active = model.streaming_status != 'offline'

        await ss.toggle_streaming()
        if active:
            console.out.print('Stream stopped.')
        else:
            console.out.print('Stream started.')

        conn.close()

    async with create_task_group() as tg:
        tg.start_soon(conn.background_processing)
        tg.start_soon(_run)
