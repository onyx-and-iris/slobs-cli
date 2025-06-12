"""module for scene collection management in SLOBS CLI."""

import asyncclick as click
from anyio import create_task_group
from pyslobs import ISceneCollectionCreateOptions, SceneCollectionsService
from terminaltables3 import AsciiTable

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
            click.echo('No scene collections found.')
            conn.close()
            return

        active_collection = await scs.active_collection()

        table_data = [
            ['Scene Collection Name', 'ID', 'Active']
            if id
            else ['Scene Collection Name', 'Active']
        ]
        for collection in collections:
            if collection.id == active_collection.id:
                to_append = [click.style(collection.name, fg='green')]
            else:
                to_append = [click.style(collection.name, fg='blue')]
            if id:
                to_append.append(collection.id)
            if collection.id == active_collection.id:
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


@scenecollection.command()
@click.argument('scenecollection_name', required=True)
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
        else:
            conn.close()
            raise SlobsCliError(f'Scene collection "{scenecollection_name}" not found.')

        await scs.load(collection.id)
        click.echo(f'Scene collection "{scenecollection_name}" loaded successfully.')
        conn.close()

    try:
        async with create_task_group() as tg:
            tg.start_soon(conn.background_processing)
            tg.start_soon(_run)
    except* SlobsCliError as excgroup:
        for e in excgroup.exceptions:
            raise e


@scenecollection.command()
@click.argument('scenecollection_name', required=True)
@click.pass_context
async def create(ctx: click.Context, scenecollection_name: str):
    """Create a new scene collection."""
    conn = ctx.obj['connection']
    scs = SceneCollectionsService(conn)

    async def _run():
        await scs.create(ISceneCollectionCreateOptions(scenecollection_name))
        click.echo(f'Scene collection "{scenecollection_name}" created successfully.')
        conn.close()

    async with create_task_group() as tg:
        tg.start_soon(conn.background_processing)
        tg.start_soon(_run)


@scenecollection.command()
@click.argument('scenecollection_name', required=True)
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
        else:
            conn.close()
            raise SlobsCliError(f'Scene collection "{scenecollection_name}" not found.')

        await scs.delete(collection.id)
        click.echo(f'Scene collection "{scenecollection_name}" deleted successfully.')
        conn.close()

    try:
        async with create_task_group() as tg:
            tg.start_soon(conn.background_processing)
            tg.start_soon(_run)
    except* SlobsCliError as excgroup:
        for e in excgroup.exceptions:
            raise e


@scenecollection.command()
@click.argument('scenecollection_name', required=True)
@click.argument('new_name', required=True)
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
        else:
            conn.close()
            raise SlobsCliError(f'Scene collection "{scenecollection_name}" not found.')

        await scs.rename(new_name, collection.id)
        click.echo(
            f'Scene collection "{scenecollection_name}" renamed to "{new_name}".'
        )
        conn.close()

    try:
        async with create_task_group() as tg:
            tg.start_soon(conn.background_processing)
            tg.start_soon(_run)
    except* SlobsCliError as excgroup:
        for e in excgroup.exceptions:
            raise e
