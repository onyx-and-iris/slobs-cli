import asyncclick as click
from anyio import create_task_group
from pyslobs import TransitionsService

from .cli import cli
from .errors import SlobsCliError


@cli.group()
def studiomode():
    """Studio mode management commands."""


@studiomode.command()
@click.pass_context
async def enable(ctx: click.Context):
    """Enable studio mode."""

    conn = ctx.obj["connection"]
    ts = TransitionsService(conn)

    async def _run():
        model = await ts.get_model()
        if model.studio_mode:
            conn.close()
            raise SlobsCliError("Studio mode is already enabled.")

        await ts.enable_studio_mode()
        click.echo("Studio mode enabled successfully.")
        conn.close()

    try:
        async with create_task_group() as tg:
            tg.start_soon(conn.background_processing)
            tg.start_soon(_run)
    except* SlobsCliError as excgroup:
        for e in excgroup.exceptions:
            raise e


@studiomode.command()
@click.pass_context
async def disable(ctx: click.Context):
    """Disable studio mode."""

    conn = ctx.obj["connection"]
    ts = TransitionsService(conn)

    async def _run():
        model = await ts.get_model()
        if not model.studio_mode:
            conn.close()
            raise SlobsCliError("Studio mode is already disabled.")

        await ts.disable_studio_mode()
        click.echo("Studio mode disabled successfully.")
        conn.close()

    try:
        async with create_task_group() as tg:
            tg.start_soon(conn.background_processing)
            tg.start_soon(_run)
    except* SlobsCliError as excgroup:
        for e in excgroup.exceptions:
            raise e


@studiomode.command()
@click.pass_context
async def status(ctx: click.Context):
    """Check the status of studio mode."""

    conn = ctx.obj["connection"]
    ts = TransitionsService(conn)

    async def _run():
        model = await ts.get_model()
        if model.studio_mode:
            click.echo("Studio mode is currently enabled.")
        else:
            click.echo("Studio mode is currently disabled.")
        conn.close()

    async with create_task_group() as tg:
        tg.start_soon(conn.background_processing)
        tg.start_soon(_run)


@studiomode.command()
@click.pass_context
async def toggle(ctx: click.Context):
    """Toggle studio mode."""

    conn = ctx.obj["connection"]
    ts = TransitionsService(conn)

    async def _run():
        model = await ts.get_model()
        if model.studio_mode:
            await ts.disable_studio_mode()
            click.echo("Studio mode disabled successfully.")
        else:
            await ts.enable_studio_mode()
            click.echo("Studio mode enabled successfully.")
        conn.close()

    async with create_task_group() as tg:
        tg.start_soon(conn.background_processing)
        tg.start_soon(_run)


@studiomode.command()
@click.pass_context
async def force_transition(ctx: click.Context):
    """Force a transition in studio mode."""

    conn = ctx.obj["connection"]
    ts = TransitionsService(conn)

    async def _run():
        model = await ts.get_model()
        if not model.studio_mode:
            conn.close()
            raise SlobsCliError("Studio mode is not enabled.")

        await ts.execute_studio_mode_transition()
        click.echo("Forced studio mode transition.")
        conn.close()

    try:
        async with create_task_group() as tg:
            tg.start_soon(conn.background_processing)
            tg.start_soon(_run)
    except* SlobsCliError as excgroup:
        for e in excgroup.exceptions:
            raise e
