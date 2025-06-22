"""module defining the entry point for the Streamlabs Desktop CLI application."""

import anyio
import asyncclick as click
from pyslobs import ConnectionConfig, SlobsConnection

from . import styles
from .__about__ import __version__ as version


@click.group()
@click.option(
    '-d',
    '--domain',
    default='localhost',
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
@click.option(
    '-s',
    '--style',
    default='disabled',
    envvar='SLOBS_STYLE',
    show_default=True,
    show_envvar=True,
    help='The style to use for output.',
)
@click.option(
    '-b',
    '--no-border',
    is_flag=True,
    default=False,
    envvar='SLOBS_STYLE_NO_BORDER',
    show_default=True,
    show_envvar=True,
    help='Disable borders in the output.',
)
@click.version_option(
    version, '-v', '--version', message='%(prog)s version: %(version)s'
)
@click.pass_context
async def cli(
    ctx: click.Context, domain: str, port: int, token: str, style: str, no_border: bool
):
    """Command line interface for Streamlabs Desktop."""
    ctx.ensure_object(dict)
    config = ConnectionConfig(
        domain=domain,
        port=port,
        token=token,
    )
    ctx.obj['connection'] = SlobsConnection(config)
    ctx.obj['style'] = styles.request_style_obj(style, no_border)


def run():
    """Run the CLI application."""
    anyio.run(cli.main)
