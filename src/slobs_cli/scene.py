"""module for managing scenes in Slobs CLI."""

import asyncclick as click
from anyio import create_task_group
from pyslobs import ScenesService, TransitionsService
from terminaltables3 import AsciiTable

from .cli import cli
from .errors import SlobsCliError


@cli.group()
def scene():
    """Manage scenes in Slobs CLI."""


@scene.command()
@click.option('--id', is_flag=True, help='Include scene IDs in the output.')
@click.pass_context
async def list(ctx: click.Context, id: bool = False):
    """List all available scenes."""
    conn = ctx.obj['connection']
    ss = ScenesService(conn)

    async def _run():
        scenes = await ss.get_scenes()
        if not scenes:
            click.echo('No scenes found.')
            conn.close()
            return

        active_scene = await ss.active_scene()

        table_data = [
            ['Scene Name', 'ID', 'Active'] if id else ['Scene Name', 'Active']
        ]
        for scene in scenes:
            if scene.id == active_scene.id:
                to_append = [click.style(scene.name, fg='green')]
            else:
                to_append = [click.style(scene.name, fg='blue')]
            if id:
                to_append.append(scene.id)
            if scene.id == active_scene.id:
                to_append.append('✅')

            table_data.append(to_append)

        table = AsciiTable(table_data)
        table.justify_columns = {
            0: 'left',
            1: 'left' if id else 'center',
            2: 'center' if id else None,
        }
        click.echo(table.table)

        conn.close()

    async with create_task_group() as tg:
        tg.start_soon(conn.background_processing)
        tg.start_soon(_run)


@scene.command()
@click.option('--id', is_flag=True, help='Include scene IDs in the output.')
@click.pass_context
async def current(ctx: click.Context, id: bool = False):
    """Show the currently active scene."""
    conn = ctx.obj['connection']
    ss = ScenesService(conn)

    async def _run():
        active_scene = await ss.active_scene()
        click.echo(
            f'Current active scene: {click.style(active_scene.name, fg="green")} '
            f'{f"(ID: {active_scene.id})" if id else ""}'
        )
        conn.close()

    async with create_task_group() as tg:
        tg.start_soon(conn.background_processing)
        tg.start_soon(_run)


@scene.command()
@click.option('--id', is_flag=True, help='Include scene IDs in the output.')
@click.argument('scene_name', type=str)
@click.option(
    '--preview',
    is_flag=True,
    help='Switch the preview scene only.',
)
@click.pass_context
async def switch(
    ctx: click.Context, scene_name: str, preview: bool = False, id: bool = False
):
    """Switch to a scene by its name."""
    conn = ctx.obj['connection']
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
                            f'Switched to preview scene: {click.style(scene.name, fg="blue")} '
                            f'{f"(ID: {scene.id})." if id else ""}'
                        )
                    else:
                        click.echo(
                            f'Switched to scene: {click.style(scene.name, fg="blue")} '
                            f'{f"(ID: {scene.id})." if id else ""}'
                        )
                        await ts.execute_studio_mode_transition()
                        click.echo(
                            'Executed studio mode transition to make the scene active.'
                        )
                else:
                    if preview:
                        conn.close()
                        raise SlobsCliError(
                            'Cannot switch the preview scene in non-studio mode.'
                        )

                    await ss.make_scene_active(scene.id)
                    click.echo(
                        f'Switched to scene: {click.style(scene.name, fg="blue")} '
                        f'{f"(ID: {scene.id})." if id else ""}'
                    )

                conn.close()
                break
        else:  # If no scene by the given name was found
            conn.close()
            raise SlobsCliError(f"Scene '{scene_name}' not found.")

    try:
        async with create_task_group() as tg:
            tg.start_soon(conn.background_processing)
            tg.start_soon(_run)
    except* SlobsCliError as excgroup:
        for e in excgroup.exceptions:
            raise e
