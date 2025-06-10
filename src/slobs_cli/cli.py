import anyio
import asyncclick as click
from pyslobs import ConnectionConfig, SlobsConnection


@click.group()
@click.option(
    "-d",
    "--domain",
    default="127.0.0.1",
    show_default=True,
    show_envvar=True,
    help="The domain of the SLOBS server.",
    envvar="SLOBS_DOMAIN",
)
@click.option(
    "-p",
    "--port",
    default=59650,
    show_default=True,
    show_envvar=True,
    help="The port of the SLOBS server.",
    envvar="SLOBS_PORT",
)
@click.option(
    "-t",
    "--token",
    help="The token for the SLOBS server.",
    envvar="SLOBS_TOKEN",
    show_envvar=True,
)
@click.pass_context
async def cli(ctx: click.Context, domain: str, port: int, token: str | None):
    """
    Command line interface for SLOBS.
    """
    ctx.ensure_object(dict)
    config = ConnectionConfig(
        domain=domain,
        port=port,
        token=token,
    )
    ctx.obj["connection"] = SlobsConnection(config)


def run():
    """Run the CLI application."""
    anyio.run(cli.main)
