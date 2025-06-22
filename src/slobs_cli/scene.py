"""module for managing scenes in Slobs CLI."""

import asyncclick as click
from anyio import create_task_group
from pyslobs import ProtocolError, ScenesService, TransitionsService
from rich.table import Table
from rich.text import Text

from . import console, util
from .cli import cli
from .errors import SlobsCliError, SlobsCliProtocolError


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
            console.out.print('No scenes found.')
            conn.close()
            return

        active_scene = await ss.active_scene()

        style = ctx.obj['style']
        table = Table(
            show_header=True,
            header_style=style.header,
            border_style=style.border,
        )

        if id:
            columns = [
                ('Scene Name', 'left'),
                ('Active', 'center'),
                ('ID', 'left'),
            ]
        else:
            columns = [
                ('Scene Name', 'left'),
                ('Active', 'center'),
            ]

        for col_name, col_justify in columns:
            table.add_column(Text(col_name, justify='center'), justify=col_justify)

        for scene in scenes:
            to_append = [Text(scene.name, style=style.cell)]
            to_append.append(
                util.check_mark(ctx, scene.id == active_scene.id, empty_if_false=True)
            )
            if id:
                to_append.append(Text(scene.id, style=style.cell))

            table.add_row(*to_append)

        console.out.print(table)

        conn.close()

    try:
        async with create_task_group() as tg:
            tg.start_soon(conn.background_processing)
            tg.start_soon(_run)
    except* ProtocolError as excgroup:
        p_error = next(iter(excgroup.exceptions))
        raisable = SlobsCliProtocolError(str(p_error))
        raise raisable


@scene.command()
@click.option('--id', is_flag=True, help='Include scene IDs in the output.')
@click.pass_context
async def current(ctx: click.Context, id: bool = False):
    """Show the currently active scene."""
    conn = ctx.obj['connection']
    ss = ScenesService(conn)

    async def _run():
        active_scene = await ss.active_scene()
        console.out.print(
            f'Current active scene: {console.highlight(ctx, active_scene.name)} '
            f'{f"(ID: {console.highlight(ctx, active_scene.id)})" if id else ""}'
        )
        conn.close()

    try:
        async with create_task_group() as tg:
            tg.start_soon(conn.background_processing)
            tg.start_soon(_run)
    except* ProtocolError as excgroup:
        p_error = next(iter(excgroup.exceptions))
        raisable = SlobsCliProtocolError(str(p_error))
        raise raisable


@scene.command()
@click.option('--id', is_flag=True, help='Include scene IDs in the output.')
@click.argument('scene_name')
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
                        console.out.print(
                            f'Switched to preview scene: {console.highlight(ctx, scene.name)} '
                            f'{f"(ID: {console.highlight(ctx, scene.id)})" if id else ""}'
                        )
                    else:
                        console.out.print(
                            f'Switched to scene: {console.highlight(ctx, scene.name)} '
                            f'{f"(ID: {console.highlight(ctx, scene.id)})" if id else ""}'
                        )
                        console.err.print(
                            console.warning(
                                ctx,
                                'Warning: You are in studio mode. The scene switch is not active yet.\n'
                                'use `slobs-cli studiomode force-transition` to activate the scene switch.',
                            )
                        )
                else:
                    if preview:
                        conn.close()
                        raise SlobsCliError(
                            'Cannot switch the preview scene in non-studio mode.'
                        )

                    await ss.make_scene_active(scene.id)
                    console.out.print(
                        f'Switched to scene: {console.highlight(ctx, scene.name)} '
                        f'{f"(ID: {console.highlight(ctx, scene.id)})" if id else ""}'
                    )

                conn.close()
                break
        else:  # If no scene by the given name was found
            conn.close()
            raise SlobsCliError(f'Scene "{scene_name}" not found.')

    try:
        async with create_task_group() as tg:
            tg.start_soon(conn.background_processing)
            tg.start_soon(_run)
    except* SlobsCliError as excgroup:
        raisable = next(iter(excgroup.exceptions))
        raise raisable
    except* ProtocolError as excgroup:
        p_error = next(iter(excgroup.exceptions))
        raisable = SlobsCliProtocolError(str(p_error))
        raise raisable
