"""Test cases for audio commands in slobs_cli."""

import pytest
from asyncclick.testing import CliRunner

from slobs_cli import cli


@pytest.mark.anyio
async def test_audio_list():
    """Test the list audio sources command."""
    runner = CliRunner()
    result = await runner.invoke(cli, ['audio', 'list'])
    assert result.exit_code == 0
    assert 'Desktop Audio' in result.output
    assert 'Mic/Aux' in result.output


@pytest.mark.anyio
async def test_audio_mute():
    """Test the mute audio source command."""
    runner = CliRunner()
    result = await runner.invoke(cli, ['audio', 'mute', 'Mic/Aux'])
    assert result.exit_code == 0
    assert 'Mic/Aux muted successfully' in result.output


@pytest.mark.anyio
async def test_audio_unmute():
    """Test the unmute audio source command."""
    runner = CliRunner()
    result = await runner.invoke(cli, ['audio', 'unmute', 'Mic/Aux'])
    assert result.exit_code == 0
    assert 'Mic/Aux unmuted successfully' in result.output


@pytest.mark.anyio
async def test_audio_invalid_source():
    """Test handling of invalid audio source."""
    runner = CliRunner()
    result = await runner.invoke(cli, ['audio', 'mute', 'InvalidSource'])
    assert result.exit_code != 0
    assert 'Audio source "InvalidSource" not found' in result.output
