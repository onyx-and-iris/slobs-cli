"""Test cases for the replay buffer commands in slobs_cli."""

import anyio
import pytest
from asyncclick.testing import CliRunner

from slobs_cli import cli


@pytest.mark.anyio
async def test_replaybuffer_start():
    """Test the start replay buffer command."""
    runner = CliRunner()
    result = await runner.invoke(cli, ['replaybuffer', 'status'])
    assert result.exit_code == 0
    active = 'Replay buffer is currently active.' in result.output

    result = await runner.invoke(cli, ['replaybuffer', 'start'])
    if not active:
        assert result.exit_code == 0
        assert 'Replay buffer started' in result.output
        await anyio.sleep(0.2)  # Allow some time for the replay buffer to start
    else:
        assert result.exit_code != 0
        assert 'Replay buffer is already active.' in result.output


@pytest.mark.anyio
async def test_replaybuffer_stop():
    """Test the stop replay buffer command."""
    runner = CliRunner()
    result = await runner.invoke(cli, ['replaybuffer', 'status'])
    assert result.exit_code == 0
    active = 'Replay buffer is currently active.' in result.output

    result = await runner.invoke(cli, ['replaybuffer', 'stop'])
    if active:
        assert result.exit_code == 0
        assert 'Replay buffer stopped' in result.output
        await anyio.sleep(0.2)  # Allow some time for the replay buffer to stop
    else:
        assert result.exit_code != 0
        assert 'Replay buffer is already inactive.' in result.output
