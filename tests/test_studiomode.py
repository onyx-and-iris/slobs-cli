"""Test cases for the studio mode commands of the slobs_cli CLI application."""

import pytest
from asyncclick.testing import CliRunner

from slobs_cli import cli


@pytest.mark.anyio
async def test_studiomode_enable():
    """Test the enable studio mode command."""
    runner = CliRunner()

    result = await runner.invoke(cli, ['studiomode', 'status'])
    assert result.exit_code == 0
    active = 'Studio mode is currently enabled.' in result.output

    result = await runner.invoke(cli, ['studiomode', 'enable'])
    if active:
        assert result.exit_code != 0
        assert 'Studio mode is already enabled.' in result.output
    else:
        assert result.exit_code == 0
        assert 'Studio mode enabled successfully.' in result.output


@pytest.mark.anyio
async def test_studiomode_disable():
    """Test the disable studio mode command."""
    runner = CliRunner()

    result = await runner.invoke(cli, ['studiomode', 'status'])
    assert result.exit_code == 0
    active = 'Studio mode is currently enabled.' in result.output

    result = await runner.invoke(cli, ['studiomode', 'disable'])
    if not active:
        assert result.exit_code != 0
        assert 'Studio mode is already disabled.' in result.output
    else:
        assert result.exit_code == 0
        assert 'Studio mode disabled successfully.' in result.output


@pytest.mark.anyio
async def test_studiomode_toggle():
    """Test the toggle studio mode command."""
    runner = CliRunner()

    result = await runner.invoke(cli, ['studiomode', 'status'])
    assert result.exit_code == 0
    active = 'Studio mode is currently enabled.' in result.output

    result = await runner.invoke(cli, ['studiomode', 'toggle'])
    if active:
        assert result.exit_code == 0
        assert 'Studio mode disabled successfully.' in result.output
    else:
        assert result.exit_code == 0
        assert 'Studio mode enabled successfully.' in result.output
