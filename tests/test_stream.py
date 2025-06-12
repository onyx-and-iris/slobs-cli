"""Tests for the stream commands in slobs_cli."""

import anyio
import pytest
from asyncclick.testing import CliRunner

from slobs_cli import cli


@pytest.mark.anyio
async def test_stream_start():
    """Test the start stream command."""
    runner = CliRunner()
    result = await runner.invoke(cli, ['stream', 'status'])
    assert result.exit_code == 0
    active = 'Stream is currently active.' in result.output

    result = await runner.invoke(cli, ['stream', 'start'])
    if not active:
        assert result.exit_code == 0
        assert 'Stream started' in result.output
        await anyio.sleep(0.2)  # Allow some time for the stream to start
    else:
        assert result.exit_code != 0
        assert 'Stream is already active.' in result.output


@pytest.mark.anyio
async def test_stream_stop():
    """Test the stop stream command."""
    runner = CliRunner()
    result = await runner.invoke(cli, ['stream', 'status'])
    assert result.exit_code == 0
    active = 'Stream is currently active.' in result.output

    result = await runner.invoke(cli, ['stream', 'stop'])
    if active:
        assert result.exit_code == 0
        assert 'Stream stopped' in result.output
        await anyio.sleep(0.2)  # Allow some time for the stream to stop
    else:
        assert result.exit_code != 0
        assert 'Stream is already inactive.' in result.output
