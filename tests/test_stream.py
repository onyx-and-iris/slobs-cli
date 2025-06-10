import anyio
import asyncclick as click
import pytest
from asyncclick.testing import CliRunner

from slobs_cli import cli


@pytest.mark.anyio
async def test_stream_start():
    runner = CliRunner()
    result = await runner.invoke(cli, ["stream", "status"])
    assert result.exit_code == 0
    active = "Stream is currently active." in result.output

    if not active:
        result = await runner.invoke(cli, ["stream", "start"])
        assert result.exit_code == 0
        assert "Stream started" in result.output
        await anyio.sleep(1)  # Allow some time for the stream to start
    else:
        with pytest.raises(ExceptionGroup) as exc_info:
            result = await runner.invoke(
                cli, ["stream", "start"], catch_exceptions=False
            )
        assert exc_info.group_contains(click.Abort, match="Stream is already active.")


@pytest.mark.anyio
async def test_stream_stop():
    runner = CliRunner()
    result = await runner.invoke(cli, ["stream", "status"])
    assert result.exit_code == 0
    active = "Stream is currently active." in result.output

    if active:
        result = await runner.invoke(cli, ["stream", "stop"])
        assert result.exit_code == 0
        assert "Stream stopped" in result.output
        await anyio.sleep(1)  # Allow some time for the stream to stop
    else:
        with pytest.raises(ExceptionGroup) as exc_info:
            result = await runner.invoke(
                cli, ["stream", "stop"], catch_exceptions=False
            )
        assert exc_info.group_contains(click.Abort, match="Stream is already inactive.")
