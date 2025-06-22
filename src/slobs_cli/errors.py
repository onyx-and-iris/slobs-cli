"""module for custom exceptions in Slobs CLI."""

import json

import asyncclick as click

from . import console


class SlobsCliError(click.ClickException):
    """Base class for all Slobs CLI errors."""

    def __init__(self, message: str):
        """Initialize the SlobsCliError with a message."""
        super().__init__(message)
        self.exit_code = 1

    def show(self):
        """Display the error message in red and write to stderr."""
        console.err.print(f'Error: {self.message}')


class SlobsCliProtocolError(SlobsCliError):
    """Converts pyslobs ProtocolError to a SlobsCliProtocolError."""

    def __init__(self, message: str):
        """Initialize the SlobsCliProtocolError with a message."""
        protocol_message_to_dict = json.loads(
            str(message).replace('"', '\\"').replace("'", '"')
        )
        super().__init__(
            protocol_message_to_dict.get('message', 'Unable to parse error message')
        )
        self.exit_code = 2
        self.protocol_code = protocol_message_to_dict.get('code', 'Unknown error code')

    def show(self):
        """Display the protocol error message in red."""
        match self.protocol_code:
            case -32600:
                console.err.print(
                    'Oops! Looks like we hit a rate limit for this command. Please try again later.'
                )
            case _:
                # Fall back to the base error display for unknown protocol codes
                super().show()
