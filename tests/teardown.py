import os

import anyio
from anyio import create_task_group
from pyslobs import ConnectionConfig, ScenesService, SlobsConnection, StreamingService


async def cleanup(conn: SlobsConnection):
    ss = ScenesService(conn)
    scenes = await ss.get_scenes()
    for scene in scenes:
        if scene.name.startswith("slobs-test-scene-"):
            await ss.remove_scene(scene.id)

    ss = StreamingService(conn)
    model = await ss.get_model()
    if model.streaming_status != "offline":
        await ss.toggle_streaming()
    if model.replay_buffer_status != "offline":
        await ss.stop_replay_buffer()
    if model.recording_status != "offline":
        await ss.toggle_recording()

    conn.close()


async def main():
    conn = SlobsConnection(
        ConnectionConfig(
            domain=os.environ["SLOBS_DOMAIN"],
            port=59650,
            token=os.environ["SLOBS_TOKEN"],
        )
    )

    async with create_task_group() as tg:
        tg.start_soon(conn.background_processing)
        tg.start_soon(cleanup, conn)


if __name__ == "__main__":
    anyio.run(main)
