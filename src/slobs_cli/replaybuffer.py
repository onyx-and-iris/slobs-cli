import asyncclick as click
from anyio import create_task_group
from pyslobs import StreamingService

from .cli import cli
from .errors import SlobsCliError


@cli.group()
def replaybuffer():
    """Replay buffer management commands."""


@replaybuffer.command()
@click.pass_context
async def start(ctx: click.Context):
    """Start the replay buffer."""

    conn = ctx.obj["connection"]
    ss = StreamingService(conn)

    async def _run():
        model = await ss.get_model()
        active = model.replay_buffer_status != "offline"

        if active:
            conn.close()
            raise SlobsCliError("Replay buffer is already active.")

        await ss.start_replay_buffer()
        click.echo("Replay buffer started.")
        conn.close()

    try:
        async with create_task_group() as tg:
            tg.start_soon(conn.background_processing)
            tg.start_soon(_run)
    except* SlobsCliError as excgroup:
        for e in excgroup.exceptions:
            raise e


@replaybuffer.command()
@click.pass_context
async def stop(ctx: click.Context):
    """Stop the replay buffer."""

    conn = ctx.obj["connection"]
    ss = StreamingService(conn)

    async def _run():
        model = await ss.get_model()
        active = model.replay_buffer_status != "offline"

        if not active:
            conn.close()
            raise SlobsCliError("Replay buffer is already inactive.")

        await ss.stop_replay_buffer()
        click.echo("Replay buffer stopped.")
        conn.close()

    try:
        async with create_task_group() as tg:
            tg.start_soon(conn.background_processing)
            tg.start_soon(_run)
    except* SlobsCliError as excgroup:
        for e in excgroup.exceptions:
            raise e


@replaybuffer.command()
@click.pass_context
async def status(ctx: click.Context):
    """Get the current status of the replay buffer."""

    conn = ctx.obj["connection"]
    ss = StreamingService(conn)

    async def _run():
        model = await ss.get_model()
        active = model.replay_buffer_status != "offline"
        if active:
            click.echo("Replay buffer is currently active.")
        else:
            click.echo("Replay buffer is currently inactive.")
        conn.close()

    async with create_task_group() as tg:
        tg.start_soon(conn.background_processing)
        tg.start_soon(_run)


@replaybuffer.command()
@click.pass_context
async def save(ctx: click.Context):
    """Save the current replay buffer."""

    conn = ctx.obj["connection"]
    ss = StreamingService(conn)

    async def _run():
        await ss.save_replay()
        click.echo("Replay buffer saved.")
        conn.close()

    async with create_task_group() as tg:
        tg.start_soon(conn.background_processing)
        tg.start_soon(_run)
