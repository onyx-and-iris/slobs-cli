"""Create test scenes in Streamlabs.

Usage:
    Run this script as a standalone program to setup the test environment.
    Requires 'SLOBS_DOMAIN' and 'SLOBS_TOKEN' environment variables to be set.
"""

import os

import anyio
from anyio import create_task_group
from pyslobs import ConnectionConfig, ScenesService, SlobsConnection


async def setup(conn: SlobsConnection):
    """Set up test scenes in Streamlabs OBS."""
    ss = ScenesService(conn)
    await ss.create_scene('slobs-test-scene-1')
    await ss.create_scene('slobs-test-scene-2')
    await ss.create_scene('slobs-test-scene-3')

    conn.close()


async def main():
    """Establish connection and set up scenes."""
    conn = SlobsConnection(
        ConnectionConfig(
            domain=os.environ['SLOBS_DOMAIN'],
            port=59650,
            token=os.environ['SLOBS_TOKEN'],
        )
    )

    async with create_task_group() as tg:
        tg.start_soon(conn.background_processing)
        tg.start_soon(setup, conn)


if __name__ == '__main__':
    anyio.run(main)
