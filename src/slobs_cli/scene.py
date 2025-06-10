import asyncclick as click
from anyio import create_task_group
from pyslobs import ScenesService

from .cli import cli


@cli.group()
def scene():
    """Scene management commands."""


@scene.command()
@click.pass_context
async def list(ctx: click.Context):
    """List all available scenes."""

    conn = ctx.obj["connection"]
    ss = ScenesService(conn)

    async def _run():
        scenes = await ss.get_scenes()
        if not scenes:
            click.echo("No scenes found.")
            return

        click.echo("Available scenes:")
        for scene in scenes:
            click.echo(f"- {click.style(scene.name, fg='blue')} (ID: {scene.id})")

        conn.close()

    async with create_task_group() as tg:
        tg.start_soon(conn.background_processing)
        tg.start_soon(_run)


@scene.command()
@click.pass_context
async def current(ctx: click.Context):
    """Show the currently active scene."""

    conn = ctx.obj["connection"]
    ss = ScenesService(conn)

    async def _run():
        active_scene = await ss.active_scene()
        if active_scene:
            click.echo(
                f"Current active scene: {click.style(active_scene.name, fg='green')} (ID: {active_scene.id})"
            )
        else:
            click.echo("No active scene found.")
        conn.close()

    async with create_task_group() as tg:
        tg.start_soon(conn.background_processing)
        tg.start_soon(_run)


@scene.command()
@click.argument("scene_name", type=str)
@click.pass_context
async def switch(ctx: click.Context, scene_name: str):
    """Switch to a scene by its name."""

    conn = ctx.obj["connection"]
    ss = ScenesService(conn)

    async def _run():
        scenes = await ss.get_scenes()
        for scene in scenes:
            if scene.name == scene_name:
                await ss.make_scene_active(scene.id)
                click.echo(f"Switched to scene: {click.style(scene.name, fg='green')}")
                conn.close()
                break
        else:
            conn.close()
            raise click.ClickException(
                click.style(f"Scene '{scene_name}' not found.", fg="red")
            )

    async with create_task_group() as tg:
        tg.start_soon(conn.background_processing)
        tg.start_soon(_run)
