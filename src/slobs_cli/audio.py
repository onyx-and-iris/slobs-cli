"""module for managing audio sources in Slobs CLI."""

import asyncclick as click
from anyio import create_task_group
from pyslobs import AudioService
from rich.table import Table
from rich.text import Text

from . import console, util
from .cli import cli
from .errors import SlobsCliError


@cli.group()
def audio():
    """Manage audio sources in Slobs CLI."""


@audio.command()
@click.option('--id', is_flag=True, help='Include audio source IDs in the output.')
@click.pass_context
async def list(ctx: click.Context, id: bool = False):
    """List all audio sources."""
    conn = ctx.obj['connection']
    as_ = AudioService(conn)

    async def _run():
        sources = await as_.get_sources()
        if not sources:
            console.out.print('No audio sources found.')
            conn.close()
            return

        style = ctx.obj['style']
        table = Table(
            show_header=True, header_style=style.header, border_style=style.border
        )

        if id:
            columns = [
                ('Audio Source Name', 'left'),
                ('Muted', 'center'),
                ('ID', 'left'),
            ]
        else:
            columns = [
                ('Audio Source Name', 'left'),
                ('Muted', 'center'),
            ]
        for col_name, col_justify in columns:
            table.add_column(Text(col_name, justify='center'), justify=col_justify)

        for source in sources:
            model = await source.get_model()

            to_append = [Text(model.name, style=style.cell)]
            to_append.append(util.check_mark(ctx, model.muted))
            if id:
                to_append.append(Text(model.source_id, style=style.cell))

            table.add_row(*to_append)

        console.out.print(table)

        conn.close()

    async with create_task_group() as tg:
        tg.start_soon(conn.background_processing)
        tg.start_soon(_run)


@audio.command()
@click.argument('source_name')
@click.pass_context
async def mute(ctx: click.Context, source_name: str):
    """Mute an audio source by name."""
    conn = ctx.obj['connection']
    as_ = AudioService(conn)

    async def _run():
        sources = await as_.get_sources()
        for source in sources:
            model = await source.get_model()
            if model.name.lower() == source_name.lower():
                break
        else:  # If no source by the given name was found
            conn.close()
            raise SlobsCliError(f'Audio source "{source_name}" not found.')

        await source.set_muted(True)
        console.out.print(f'{console.highlight(ctx, source_name)} muted successfully.')
        conn.close()

    try:
        async with create_task_group() as tg:
            tg.start_soon(conn.background_processing)
            tg.start_soon(_run)
    except* SlobsCliError as excgroup:
        raisable = next(iter(excgroup.exceptions))
        raise raisable


@audio.command()
@click.argument('source_name')
@click.pass_context
async def unmute(ctx: click.Context, source_name: str):
    """Unmute an audio source by name."""
    conn = ctx.obj['connection']
    as_ = AudioService(conn)

    async def _run():
        sources = await as_.get_sources()
        for source in sources:
            model = await source.get_model()
            if model.name.lower() == source_name.lower():
                break
        else:  # If no source by the given name was found
            conn.close()
            raise SlobsCliError(f'Audio source "{source_name}" not found.')

        await source.set_muted(False)
        console.out.print(
            f'{console.highlight(ctx, source_name)} unmuted successfully.'
        )
        conn.close()

    try:
        async with create_task_group() as tg:
            tg.start_soon(conn.background_processing)
            tg.start_soon(_run)
    except* SlobsCliError as excgroup:
        raisable = next(iter(excgroup.exceptions))
        raise raisable


@audio.command()
@click.argument('source_name')
@click.pass_context
async def toggle(ctx: click.Context, source_name: str):
    """Toggle mute state of an audio source by name."""
    conn = ctx.obj['connection']
    as_ = AudioService(conn)

    async def _run():
        sources = await as_.get_sources()
        for source in sources:
            model = await source.get_model()
            if model.name.lower() == source_name.lower():
                if model.muted:
                    await source.set_muted(False)
                    console.out.print(
                        f'{console.highlight(ctx, source_name)} unmuted successfully.'
                    )
                else:
                    await source.set_muted(True)
                    console.out.print(
                        f'{console.highlight(ctx, source_name)} muted successfully.'
                    )
                conn.close()
                break
        else:  # If no source by the given name was found
            conn.close()
            raise SlobsCliError(f'Audio source "{source_name}" not found.')

    try:
        async with create_task_group() as tg:
            tg.start_soon(conn.background_processing)
            tg.start_soon(_run)
    except* SlobsCliError as excgroup:
        raisable = next(iter(excgroup.exceptions))
        raise raisable


@audio.command()
@click.argument('source_name')
@click.pass_context
async def status(ctx: click.Context, source_name: str):
    """Get the mute status of an audio source by name."""
    conn = ctx.obj['connection']
    as_ = AudioService(conn)

    async def _run():
        sources = await as_.get_sources()
        for source in sources:
            model = await source.get_model()
            if model.name.lower() == source_name.lower():
                console.out.print(
                    f'{console.highlight(ctx, source_name)} is {"muted" if model.muted else "unmuted"}.'
                )
                conn.close()
                return
        else:  # If no source by the given name was found
            conn.close()
            raise SlobsCliError(f'Audio source "{source_name}" not found.')

    try:
        async with create_task_group() as tg:
            tg.start_soon(conn.background_processing)
            tg.start_soon(_run)
    except* SlobsCliError as excgroup:
        raisable = next(iter(excgroup.exceptions))
        raise raisable
