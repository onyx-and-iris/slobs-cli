"""module defining the entry point for the Streamlabs Desktop CLI application."""

import anyio
import asyncclick as click
from pyslobs import ConnectionConfig, SlobsConnection

from .__about__ import __version__ as version


@click.group()
@click.option(
    '-d',
    '--domain',
    default='127.0.0.1',
    envvar='SLOBS_DOMAIN',
    show_default=True,
    show_envvar=True,
    help='The domain of the SLOBS server.',
)
@click.option(
    '-p',
    '--port',
    default=59650,
    envvar='SLOBS_PORT',
    show_default=True,
    show_envvar=True,
    help='The port of the SLOBS server.',
)
@click.option(
    '-t',
    '--token',
    envvar='SLOBS_TOKEN',
    show_envvar=True,
    required=True,
    help='The token for the SLOBS server.',
)
@click.version_option(
    version, '-v', '--version', message='%(prog)s version: %(version)s'
)
@click.pass_context
async def cli(ctx: click.Context, domain: str, port: int, token: str):
    """Command line interface for Streamlabs Desktop."""
    ctx.ensure_object(dict)
    config = ConnectionConfig(
        domain=domain,
        port=port,
        token=token,
    )
    ctx.obj['connection'] = SlobsConnection(config)


def run():
    """Run the CLI application."""
    anyio.run(cli.main)
