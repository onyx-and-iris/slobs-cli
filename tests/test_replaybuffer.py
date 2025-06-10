import anyio
import asyncclick as click
import pytest
from asyncclick.testing import CliRunner

from slobs_cli import cli


@pytest.mark.anyio
async def test_replaybuffer_start():
    runner = CliRunner()
    result = await runner.invoke(cli, ["replaybuffer", "status"])
    assert result.exit_code == 0
    active = "Replay buffer is currently active." in result.output

    if not active:
        result = await runner.invoke(cli, ["replaybuffer", "start"])
        assert result.exit_code == 0
        assert "Replay buffer started" in result.output
        await anyio.sleep(1)
    else:
        with pytest.raises(ExceptionGroup) as exc_info:
            result = await runner.invoke(
                cli, ["replaybuffer", "start"], catch_exceptions=False
            )
        assert exc_info.group_contains(
            click.Abort, match="Replay buffer is already active."
        )


@pytest.mark.anyio
async def test_replaybuffer_stop():
    runner = CliRunner()
    result = await runner.invoke(cli, ["replaybuffer", "status"])
    assert result.exit_code == 0
    active = "Replay buffer is currently active." in result.output

    if active:
        result = await runner.invoke(cli, ["replaybuffer", "stop"])
        assert result.exit_code == 0
        assert "Replay buffer stopped" in result.output
        await anyio.sleep(1)
    else:
        with pytest.raises(ExceptionGroup) as exc_info:
            result = await runner.invoke(
                cli, ["replaybuffer", "stop"], catch_exceptions=False
            )
        assert exc_info.group_contains(
            click.Abort, match="Replay buffer is already inactive."
        )
