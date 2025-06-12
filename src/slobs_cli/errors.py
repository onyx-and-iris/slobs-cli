import asyncclick as click


class SlobsCliError(click.ClickException):
    """Base class for all Slobs CLI errors."""

    def __init__(self, message: str):
        super().__init__(message)
        self.exit_code = 1

    def show(self):
        """Display the error message in red."""
        click.secho(f"Error: {self.message}", fg="red", err=True)
