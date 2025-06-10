import os

import anyio
from anyio import create_task_group
from pyslobs import ConnectionConfig, SlobsConnection, StreamingService


async def cleanup(conn: SlobsConnection):
    ss = StreamingService(conn)
    current_state = await ss.get_model()
    if current_state.streaming_status != "offline":
        await ss.toggle_streaming()
    if current_state.replay_buffer_status != "offline":
        await ss.stop_replay_buffer()
    if current_state.recording_status != "offline":
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
