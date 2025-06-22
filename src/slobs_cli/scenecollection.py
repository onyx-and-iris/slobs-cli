"""module for scene collection management in SLOBS CLI."""

import asyncclick as click
from anyio import create_task_group
from pyslobs import ISceneCollectionCreateOptions, SceneCollectionsService
from rich.table import Table
from rich.text import Text

from . import console, util
from .cli import cli
from .errors import SlobsCliError


@cli.group()
def scenecollection():
    """Manage scene collections in Slobs CLI."""


@scenecollection.command()
@click.option('--id', is_flag=True, help='Include scene collection IDs in the output.')
@click.pass_context
async def list(ctx: click.Context, id: bool):
    """List all scene collections."""
    conn = ctx.obj['connection']
    scs = SceneCollectionsService(conn)

    async def _run():
        collections = await scs.collections()
        if not collections:
            console.out.print('No scene collections found.')
            conn.close()
            return

        active_collection = await scs.active_collection()

        style = ctx.obj['style']
        table = Table(
            show_header=True,
            header_style=style.header,
            border_style=style.border,
        )

        if id:
            columns = [
                ('Scene Collection Name', 'left'),
                ('Active', 'center'),
                ('ID', 'left'),
            ]
        else:
            columns = [
                ('Scene Collection Name', 'left'),
                ('Active', 'center'),
            ]

        for col_name, col_justify in columns:
            table.add_column(Text(col_name, justify='center'), justify=col_justify)

        for collection in collections:
            to_append = [Text(collection.name, style=style.cell)]
            to_append.append(
                util.check_mark(
                    ctx, collection.id == active_collection.id, empty_if_false=True
                )
            )
            if id:
                to_append.append(Text(collection.id, style=style.cell))
            table.add_row(*to_append)

        console.out.print(table)

        conn.close()

    async with create_task_group() as tg:
        tg.start_soon(conn.background_processing)
        tg.start_soon(_run)


@scenecollection.command()
@click.argument('scenecollection_name')
@click.pass_context
async def load(ctx: click.Context, scenecollection_name: str):
    """Load a scene collection by name."""
    conn = ctx.obj['connection']
    scs = SceneCollectionsService(conn)

    async def _run():
        collections = await scs.collections()
        for collection in collections:
            if collection.name == scenecollection_name:
                break
        else:  # If no collection by the given name was found
            conn.close()
            raise SlobsCliError(f'Scene collection "{scenecollection_name}" not found.')

        await scs.load(collection.id)
        console.out.print(
            f'Scene collection {console.highlight(scenecollection_name)} loaded successfully.'
        )
        conn.close()

    try:
        async with create_task_group() as tg:
            tg.start_soon(conn.background_processing)
            tg.start_soon(_run)
    except* SlobsCliError as excgroup:
        raisable = next(iter(excgroup.exceptions))
        raise raisable


@scenecollection.command()
@click.argument('scenecollection_name')
@click.pass_context
async def create(ctx: click.Context, scenecollection_name: str):
    """Create a new scene collection."""
    conn = ctx.obj['connection']
    scs = SceneCollectionsService(conn)

    async def _run():
        await scs.create(ISceneCollectionCreateOptions(scenecollection_name))
        console.out.print(
            f'Scene collection {console.highlight(scenecollection_name)} created successfully.'
        )
        conn.close()

    async with create_task_group() as tg:
        tg.start_soon(conn.background_processing)
        tg.start_soon(_run)


@scenecollection.command()
@click.argument('scenecollection_name')
@click.pass_context
async def delete(ctx: click.Context, scenecollection_name: str):
    """Delete a scene collection by name."""
    conn = ctx.obj['connection']
    scs = SceneCollectionsService(conn)

    async def _run():
        collections = await scs.collections()
        for collection in collections:
            if collection.name == scenecollection_name:
                break
        else:  # If no collection by the given name was found
            conn.close()
            raise SlobsCliError(f'Scene collection "{scenecollection_name}" not found.')

        await scs.delete(collection.id)
        console.out.print(
            f'Scene collection {console.highlight(scenecollection_name)} deleted successfully.'
        )
        conn.close()

    try:
        async with create_task_group() as tg:
            tg.start_soon(conn.background_processing)
            tg.start_soon(_run)
    except* SlobsCliError as excgroup:
        raisable = next(iter(excgroup.exceptions))
        raise raisable


@scenecollection.command()
@click.argument('scenecollection_name')
@click.argument('new_name')
@click.pass_context
async def rename(ctx: click.Context, scenecollection_name: str, new_name: str):
    """Rename a scene collection."""
    conn = ctx.obj['connection']
    scs = SceneCollectionsService(conn)

    async def _run():
        collections = await scs.collections()
        for collection in collections:
            if collection.name == scenecollection_name:
                break
        else:  # If no collection by the given name was found
            conn.close()
            raise SlobsCliError(f'Scene collection "{scenecollection_name}" not found.')

        await scs.rename(new_name, collection.id)
        console.out.print(
            f'Scene collection {console.highlight(scenecollection_name)} renamed to {console.highlight(new_name)}.'
        )
        conn.close()

    try:
        async with create_task_group() as tg:
            tg.start_soon(conn.background_processing)
            tg.start_soon(_run)
    except* SlobsCliError as excgroup:
        raisable = next(iter(excgroup.exceptions))
        raise raisable
