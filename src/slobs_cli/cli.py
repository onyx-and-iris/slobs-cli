"""module defining the entry point for the Streamlabs Desktop CLI application."""

import anyio
import asyncclick as click
from pyslobs import ConnectionConfig, SlobsConnection

from . import styles
from .__about__ import __version__ as version


def validate_style(ctx: click.Context, param: click.Parameter, value: str) -> str:
    """Validate the style option."""
    if value not in styles.registry:
        raise click.BadParameter(
            f"Invalid style '{value}'. Available styles: {', '.join(styles.registry.keys())}"
        )
    return value


CONTEXT_SETTINGS = dict(help_option_names=['-h', '--help'])


@click.group(
    context_settings=CONTEXT_SETTINGS,
)
@click.option(
    '-d',
    '--domain',
    default='localhost',
    envvar='SLOBS_DOMAIN',
    show_default=True,
    show_envvar=True,
    help='\b\nStreamlabs Desktop WebSocket domain or IP address.\t',
)
@click.option(
    '-p',
    '--port',
    default=59650,
    envvar='SLOBS_PORT',
    show_default=True,
    show_envvar=True,
    help='\b\nStreamlabs Desktop WebSocket port.\t\t\t',
)
@click.option(
    '-t',
    '--token',
    envvar='SLOBS_TOKEN',
    show_envvar=True,
    required=True,
    help='\b\nStreamlabs Desktop WebSocket authentication token.\t',
)
@click.option(
    '-s',
    '--style',
    default='disabled',
    envvar='SLOBS_STYLE',
    show_default=True,
    show_envvar=True,
    help='\b\nThe style to use for output.\t\t\t\t',
    callback=validate_style,
)
@click.option(
    '-b',
    '--no-border',
    is_flag=True,
    default=False,
    envvar='SLOBS_STYLE_NO_BORDER',
    show_default=True,
    show_envvar=True,
    help='\b\nDisable borders in the output.\t\t\t\t',
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
