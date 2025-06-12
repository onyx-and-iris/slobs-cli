import asyncclick as click
from anyio import create_task_group
from pyslobs import AudioService

from .cli import cli
from .errors import SlobsCliError


@cli.group()
def audio():
    """Audio management commands."""


@audio.command()
@click.option("--id", is_flag=True, help="Include audio source IDs in the output.")
@click.pass_context
async def list(ctx: click.Context, id: bool = False):
    """List all audio sources."""

    conn = ctx.obj["connection"]
    as_ = AudioService(conn)

    async def _run():
        sources = await as_.get_sources()
        if not sources:
            click.echo("No audio sources found.")
            conn.close()
            return

        click.echo("Available audio sources:")
        for source in sources:
            model = await source.get_model()
            click.echo(
                f"- {click.style(model.name, fg='blue')} "
                f"{f'ID: {model.source_id}, ' if id else ''}"
                f"Muted: {click.style('✅', fg='green') if model.muted else click.style('❌', fg='red')}"
            )
        conn.close()

    async with create_task_group() as tg:
        tg.start_soon(conn.background_processing)
        tg.start_soon(_run)


@audio.command()
@click.argument("source_name")
@click.pass_context
async def mute(ctx: click.Context, source_name: str):
    """Mute an audio source by name."""

    conn = ctx.obj["connection"]
    as_ = AudioService(conn)

    async def _run():
        sources = await as_.get_sources()
        for source in sources:
            model = await source.get_model()
            if model.name.lower() == source_name.lower():
                break
        else:  # If no source by the given name was found
            conn.close()
            raise SlobsCliError(f"Source '{source_name}' not found.")

        await source.set_muted(True)
        click.echo(f"Muted audio source: {source_name}")
        conn.close()

    try:
        async with create_task_group() as tg:
            tg.start_soon(conn.background_processing)
            tg.start_soon(_run)
    except* SlobsCliError as excgroup:
        for e in excgroup.exceptions:
            raise e


@audio.command()
@click.argument("source_name")
@click.pass_context
async def unmute(ctx: click.Context, source_name: str):
    """Unmute an audio source by name."""

    conn = ctx.obj["connection"]
    as_ = AudioService(conn)

    async def _run():
        sources = await as_.get_sources()
        for source in sources:
            model = await source.get_model()
            if model.name.lower() == source_name.lower():
                break
        else:  # If no source by the given name was found
            conn.close()
            raise SlobsCliError(f"Source '{source_name}' not found.")

        await source.set_muted(False)
        click.echo(f"Unmuted audio source: {source_name}")
        conn.close()

    try:
        async with create_task_group() as tg:
            tg.start_soon(conn.background_processing)
            tg.start_soon(_run)
    except* SlobsCliError as excgroup:
        for e in excgroup.exceptions:
            raise e


@audio.command()
@click.argument("source_name")
@click.pass_context
async def toggle(ctx: click.Context, source_name: str):
    """Toggle mute state of an audio source by name."""

    conn = ctx.obj["connection"]
    as_ = AudioService(conn)

    async def _run():
        sources = await as_.get_sources()
        for source in sources:
            model = await source.get_model()
            if model.name.lower() == source_name.lower():
                if model.muted:
                    await source.set_muted(False)
                    click.echo(f"Unmuted audio source: {source_name}")
                else:
                    await source.set_muted(True)
                    click.echo(f"Muted audio source: {source_name}")
                conn.close()
                break
        else:  # If no source by the given name was found
            conn.close()
            raise SlobsCliError(f"Source '{source_name}' not found.")

    try:
        async with create_task_group() as tg:
            tg.start_soon(conn.background_processing)
            tg.start_soon(_run)
    except* SlobsCliError as excgroup:
        for e in excgroup.exceptions:
            raise e
