"""Test cases for scene commands in slobs_cli."""

import anyio
import pytest
from asyncclick.testing import CliRunner

from slobs_cli import cli


@pytest.mark.anyio
async def test_scene_list():
    """Test the list scenes command."""
    runner = CliRunner()
    result = await runner.invoke(cli, ['scene', 'list'])
    assert result.exit_code == 0
    assert 'slobs-test-scene-1' in result.output
    assert 'slobs-test-scene-2' in result.output
    assert 'slobs-test-scene-3' in result.output
    await anyio.sleep(0.2)  # Avoid rate limiting issues


@pytest.mark.anyio
async def test_scene_current():
    """Test the current scene command."""
    runner = CliRunner()
    result = await runner.invoke(cli, ['scene', 'switch', 'slobs-test-scene-2'])
    assert result.exit_code == 0
    await anyio.sleep(0.2)  # Avoid rate limiting issues

    result = await runner.invoke(cli, ['scene', 'current'])
    assert result.exit_code == 0
    assert 'Current active scene: slobs-test-scene-2' in result.output
    await anyio.sleep(0.2)  # Avoid rate limiting issues


@pytest.mark.anyio
async def test_scene_invalid_switch():
    """Test switching to an invalid scene."""
    runner = CliRunner()
    result = await runner.invoke(cli, ['scene', 'switch', 'invalid-scene'])
    assert result.exit_code != 0
    assert 'Scene "invalid-scene" not found' in result.output
    await anyio.sleep(0.2)  # Avoid rate limiting issues
