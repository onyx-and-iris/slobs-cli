import anyio
import asyncclick as click
import pytest
from asyncclick.testing import CliRunner

from slobs_cli import cli


@pytest.mark.anyio
async def test_record_start():
    runner = CliRunner()
    result = await runner.invoke(cli, ["record", "status"])
    assert result.exit_code == 0
    active = "Recording is currently active." in result.output

    if not active:
        result = await runner.invoke(cli, ["record", "start"])
        assert result.exit_code == 0
        assert "Recording started" in result.output
        await anyio.sleep(1)  # Allow some time for the recording to start
    else:
        with pytest.raises(ExceptionGroup) as exc_info:
            result = await runner.invoke(
                cli, ["record", "start"], catch_exceptions=False
            )
        assert exc_info.group_contains(
            click.Abort, match="Recording is already active."
        )


@pytest.mark.anyio
async def test_record_stop():
    runner = CliRunner()
    result = await runner.invoke(cli, ["record", "status"])
    assert result.exit_code == 0
    active = "Recording is currently active." in result.output

    if active:
        result = await runner.invoke(cli, ["record", "stop"])
        assert result.exit_code == 0
        assert "Recording stopped" in result.output
        await anyio.sleep(1)  # Allow some time for the recording to stop
    else:
        with pytest.raises(ExceptionGroup) as exc_info:
            result = await runner.invoke(
                cli, ["record", "stop"], catch_exceptions=False
            )
        assert exc_info.group_contains(
            click.Abort, match="Recording is already inactive."
        )
