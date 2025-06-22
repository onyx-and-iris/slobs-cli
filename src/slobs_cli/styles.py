"""module containing style management for Slobs CLI."""

import os
from dataclasses import dataclass

_registry = {}


def register_style(cls):
    """Register a style class."""
    key = cls.__name__.lower()
    if key in _registry:
        raise ValueError(f'Style {key} is already registered.')
    _registry[key] = cls
    return cls


@dataclass
class Style:
    """Base class for styles."""

    name: str = 'no_colour'
    border: str = 'none'
    header: str = 'none'
    cell: str = 'none'
    highlight: str = 'none'
    warning: str = 'none'
    no_border: bool = False

    def __post_init__(self):
        """Post-initialization to set default values and normalize the name."""
        self.name = self.name.lower()
        if self.no_border:
            self.border = None


@register_style
@dataclass
class Red(Style):
    """Red style."""

    name: str = 'red'
    header: str = ''
    border: str = 'dark_red'
    cell: str = 'red'
    highlight: str = 'red3'
    warning: str = 'magenta'


@register_style
@dataclass
class Magenta(Style):
    """Magenta style."""

    name: str = 'magenta'
    header: str = ''
    border: str = 'dark_magenta'
    cell: str = 'magenta'
    highlight: str = 'magenta3'
    warning: str = 'magenta'


@register_style
@dataclass
class Purple(Style):
    """Purple style."""

    name: str = 'purple'
    header: str = ''
    border: str = 'purple'
    cell: str = 'medium_orchid'
    highlight: str = 'medium_orchid'
    warning: str = 'magenta'


@register_style
@dataclass
class Blue(Style):
    """Blue style."""

    name: str = 'blue'
    header: str = ''
    border: str = 'dark_blue'
    cell: str = 'blue'
    highlight: str = 'blue3'
    warning: str = 'magenta'


@register_style
@dataclass
class Cyan(Style):
    """Cyan style."""

    name: str = 'cyan'
    header: str = ''
    border: str = 'dark_cyan'
    cell: str = 'cyan'
    highlight: str = 'cyan3'
    warning: str = 'magenta'


@register_style
@dataclass
class Green(Style):
    """Green style."""

    name: str = 'green'
    header: str = ''
    border: str = 'dark_green'
    cell: str = 'green'
    highlight: str = 'green3'
    warning: str = 'magenta'


@register_style
@dataclass
class Yellow(Style):
    """Yellow style."""

    name: str = 'yellow'
    header: str = ''
    border: str = 'yellow3'
    cell: str = 'wheat1'
    highlight: str = 'yellow3'
    warning: str = 'magenta'


@register_style
@dataclass
class Orange(Style):
    """Orange style."""

    name: str = 'orange'
    header: str = ''
    border: str = 'dark_orange'
    cell: str = 'orange'
    highlight: str = 'orange3'
    warning: str = 'magenta'


@register_style
@dataclass
class White(Style):
    """White style."""

    name: str = 'white'
    header: str = ''
    border: str = 'white'
    cell: str = 'white'
    highlight: str = 'white'
    warning: str = 'magenta'


@register_style
@dataclass
class Grey(Style):
    """Grey style."""

    name: str = 'grey'
    header: str = ''
    border: str = 'grey50'
    cell: str = 'grey70'
    highlight: str = 'grey90'
    warning: str = 'magenta'


@register_style
@dataclass
class Navy(Style):
    """Navy style."""

    name: str = 'navy'
    header: str = ''
    border: str = 'deep_sky_blue4'
    cell: str = 'light_sky_blue3'
    highlight: str = 'light_sky_blue3'
    warning: str = 'magenta'


@register_style
@dataclass
class Black(Style):
    """Black style."""

    name: str = 'black'
    header: str = ''
    border: str = 'black'
    cell: str = 'grey30'
    highlight: str = 'grey30'
    warning: str = 'magenta'


def request_style_obj(style_name: str, no_border: bool) -> Style:
    """Request a style object by name."""
    key = style_name.lower()
    if key not in _registry:
        os.environ['NO_COLOR'] = '1'  # Disable colour output
        return Style(no_border=no_border)
    return _registry[key](no_border=no_border)
