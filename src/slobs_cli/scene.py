import asyncclick as click
from anyio import create_task_group
from pyslobs import ScenesService, TransitionsService

from .cli import cli
from .errors import SlobsCliError


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
            conn.close()
            return

        active_scene = await ss.active_scene()

        click.echo("Available scenes:")
        for scene in scenes:
            if scene.id == active_scene.id:
                click.echo(
                    f"- {click.style(scene.name, fg='green')} (ID: {scene.id}) [Active]"
                )
            else:
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
        click.echo(
            f"Current active scene: {click.style(active_scene.name, fg='green')} (ID: {active_scene.id})"
        )
        conn.close()

    async with create_task_group() as tg:
        tg.start_soon(conn.background_processing)
        tg.start_soon(_run)


@scene.command()
@click.argument("scene_name", type=str)
@click.option(
    "--preview",
    is_flag=True,
    help="Switch the preview scene only.",
)
@click.pass_context
async def switch(ctx: click.Context, scene_name: str, preview: bool = False):
    """Switch to a scene by its name."""

    conn = ctx.obj["connection"]
    ss = ScenesService(conn)
    ts = TransitionsService(conn)

    async def _run():
        scenes = await ss.get_scenes()
        for scene in scenes:
            if scene.name == scene_name:
                model = await ts.get_model()

                if model.studio_mode:
                    await ss.make_scene_active(scene.id)
                    if preview:
                        click.echo(
                            f"Switched to scene: {click.style(scene.name, fg='blue')} (ID: {scene.id}) in preview mode."
                        )
                    else:
                        await ts.execute_studio_mode_transition()
                        click.echo(
                            f"Switched to scene: {click.style(scene.name, fg='blue')} (ID: {scene.id}) in active mode."
                        )
                else:
                    if preview:
                        conn.close()
                        raise SlobsCliError(
                            "Cannot switch to preview scene in non-studio mode."
                        )

                    await ss.make_scene_active(scene.id)
                    click.echo(
                        f"Switched to scene: {click.style(scene.name, fg='blue')} (ID: {scene.id}) in active mode."
                    )

                conn.close()
                break
        else:  # If no scene by the given name was found
            raise SlobsCliError(f"Scene '{scene_name}' not found.")

    try:
        async with create_task_group() as tg:
            tg.start_soon(conn.background_processing)
            tg.start_soon(_run)
    except* SlobsCliError as excgroup:
        for e in excgroup.exceptions:
            raise e
