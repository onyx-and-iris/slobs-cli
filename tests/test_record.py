"""Test cases for the recording commands of the slobs_cli CLI application."""

import anyio
import pytest
from asyncclick.testing import CliRunner

from slobs_cli import cli


@pytest.mark.anyio
async def test_record_start():
    """Test the start recording command."""
    runner = CliRunner()
    result = await runner.invoke(cli, ['record', 'status'])
    assert result.exit_code == 0
    active = 'Recording is currently active.' in result.output

    result = await runner.invoke(cli, ['record', 'start'])
    if not active:
        assert result.exit_code == 0
        assert 'Recording started' in result.output
        await anyio.sleep(0.2)  # Allow some time for the recording to start
    else:
        assert result.exit_code != 0
        assert 'Recording is already active.' in result.output


@pytest.mark.anyio
async def test_record_stop():
    """Test the stop recording command."""
    runner = CliRunner()
    result = await runner.invoke(cli, ['record', 'status'])
    assert result.exit_code == 0
    active = 'Recording is currently active.' in result.output

    result = await runner.invoke(cli, ['record', 'stop'])
    if active:
        assert result.exit_code == 0
        assert 'Recording stopped' in result.output
        await anyio.sleep(0.2)  # Allow some time for the recording to stop
    else:
        assert result.exit_code != 0
        assert 'Recording is already inactive.' in result.output
