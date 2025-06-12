import asyncclick as click
from anyio import create_task_group
from pyslobs import StreamingService

from .cli import cli
from .errors import SlobsCliError


@cli.group()
def record():
    """Recording management commands."""


@record.command()
@click.pass_context
async def start(ctx: click.Context):
    """Start recording."""

    conn = ctx.obj["connection"]
    ss = StreamingService(conn)

    async def _run():
        model = await ss.get_model()
        active = model.recording_status != "offline"

        if active:
            conn.close()
            raise SlobsCliError("Recording is already active.")

        await ss.toggle_recording()
        click.echo("Recording started.")

        conn.close()

    try:
        async with create_task_group() as tg:
            tg.start_soon(conn.background_processing)
            tg.start_soon(_run)
    except* SlobsCliError as excgroup:
        for e in excgroup.exceptions:
            raise e


@record.command()
@click.pass_context
async def stop(ctx: click.Context):
    """Stop recording."""

    conn = ctx.obj["connection"]
    ss = StreamingService(conn)

    async def _run():
        model = await ss.get_model()
        active = model.recording_status != "offline"

        if not active:
            conn.close()
            raise SlobsCliError("Recording is already inactive.")

        await ss.toggle_recording()
        click.echo("Recording stopped.")

        conn.close()

    try:
        async with create_task_group() as tg:
            tg.start_soon(conn.background_processing)
            tg.start_soon(_run)
    except* SlobsCliError as excgroup:
        for e in excgroup.exceptions:
            raise e


@record.command()
@click.pass_context
async def status(ctx: click.Context):
    """Get recording status."""

    conn = ctx.obj["connection"]
    ss = StreamingService(conn)

    async def _run():
        model = await ss.get_model()
        active = model.recording_status != "offline"

        if active:
            click.echo("Recording is currently active.")
        else:
            click.echo("Recording is currently inactive.")

        conn.close()

    async with create_task_group() as tg:
        tg.start_soon(conn.background_processing)
        tg.start_soon(_run)


@record.command()
@click.pass_context
async def toggle(ctx: click.Context):
    """Toggle recording status."""

    conn = ctx.obj["connection"]
    ss = StreamingService(conn)

    async def _run():
        model = await ss.get_model()
        active = model.recording_status != "offline"

        if active:
            await ss.toggle_recording()
            click.echo("Recording stopped.")
        else:
            await ss.toggle_recording()
            click.echo("Recording started.")

        conn.close()

    async with create_task_group() as tg:
        tg.start_soon(conn.background_processing)
        tg.start_soon(_run)
