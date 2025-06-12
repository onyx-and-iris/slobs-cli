"""Package slobs_cli provides a command-line interface for interacting with SLOBS (Streamlabs OBS)."""

from .audio import audio
from .cli import cli
from .record import record
from .replaybuffer import replaybuffer
from .scene import scene
from .scenecollection import scenecollection
from .stream import stream
from .studiomode import studiomode

__all__ = [
    'cli',
    'scene',
    'stream',
    'record',
    'audio',
    'replaybuffer',
    'studiomode',
    'scenecollection',
]
