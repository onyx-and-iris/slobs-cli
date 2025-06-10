import asyncclick as click
from anyio import create_task_group
from pyslobs import AudioService

from .cli import cli


@cli.group()
def audio():
    """Audio management commands."""


@audio.command()
@click.pass_context
async def list(ctx: click.Context):
    """List all audio sources."""

    conn = ctx.obj["connection"]
    as_ = AudioService(conn)

    async def _run():
        sources = await as_.get_sources()
        if not sources:
            conn.close()
            click.Abort(click.style("No audio sources found.", fg="red"))

        for source in sources:
            model = await source.get_model()
            click.echo(
                f"Source ID: {source.source_id}, Name: {model.name}, Muted: {model.muted}"
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
        else:
            conn.close()
            raise click.Abort(
                click.style(f"Source '{source_name}' not found.", fg="red")
            )

        await source.set_muted(True)
        click.echo(f"Muted audio source: {source_name}")
        conn.close()

    async with create_task_group() as tg:
        tg.start_soon(conn.background_processing)
        tg.start_soon(_run)


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
        else:
            conn.close()
            raise click.Abort(
                click.style(f"Source '{source_name}' not found.", fg="red")
            )

        await source.set_muted(False)
        click.echo(f"Unmuted audio source: {source_name}")
        conn.close()

    async with create_task_group() as tg:
        tg.start_soon(conn.background_processing)
        tg.start_soon(_run)


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
        else:
            conn.close()
            raise click.Abort(
                click.style(f"Source '{source_name}' not found.", fg="red")
            )

    async with create_task_group() as tg:
        tg.start_soon(conn.background_processing)
        tg.start_soon(_run)
