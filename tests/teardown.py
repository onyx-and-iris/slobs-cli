"""Remove test scenes in Streamlabs, disable streaming, recording, and replay buffer.

Usage:
    Run this script as a standalone program to tear down the test environment.
    Requires 'SLOBS_DOMAIN' and 'SLOBS_TOKEN' environment variables to be set.
"""

import os

import anyio
from anyio import create_task_group
from pyslobs import (
    ConnectionConfig,
    ScenesService,
    SlobsConnection,
    StreamingService,
    TransitionsService,
)


async def cleanup(conn: SlobsConnection):
    """Clean up test scenes and ensure streaming, recording, and replay buffer are stopped."""
    ss = ScenesService(conn)
    scenes = await ss.get_scenes()
    for scene in scenes:
        if scene.name.startswith('slobs-test-scene-'):
            await ss.remove_scene(scene.id)

    ss = StreamingService(conn)
    model = await ss.get_model()
    if model.streaming_status != 'offline':
        await ss.toggle_streaming()
    if model.replay_buffer_status != 'offline':
        await ss.stop_replay_buffer()
    if model.recording_status != 'offline':
        await ss.toggle_recording()

    ts = TransitionsService(conn)
    model = await ts.get_model()
    if model.studio_mode:
        await ts.disable_studio_mode()

    conn.close()


async def main():
    """Establish connection and clean up test scenes."""
    conn = SlobsConnection(
        ConnectionConfig(
            domain=os.environ['SLOBS_DOMAIN'],
            port=59650,
            token=os.environ['SLOBS_TOKEN'],
        )
    )

    async with create_task_group() as tg:
        tg.start_soon(conn.background_processing)
        tg.start_soon(cleanup, conn)


if __name__ == '__main__':
    anyio.run(main)
