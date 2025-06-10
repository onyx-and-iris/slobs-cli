import pytest
from asyncclick.testing import CliRunner

from slobs_cli import cli


@pytest.mark.anyio
async def test_scene_list():
    runner = CliRunner()
    result = await runner.invoke(cli, ["scene", "list"])
    assert result.exit_code == 0
    assert "slobs-test-scene-1" in result.output
    assert "slobs-test-scene-2" in result.output
    assert "slobs-test-scene-3" in result.output


@pytest.mark.anyio
async def test_scene_current():
    runner = CliRunner()
    result = await runner.invoke(cli, ["scene", "switch", "slobs-test-scene-2"])
    assert result.exit_code == 0

    result = await runner.invoke(cli, ["scene", "current"])
    assert result.exit_code == 0
    assert "Current active scene: slobs-test-scene-2" in result.output
