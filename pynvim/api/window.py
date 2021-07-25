"""API for working with Nvim windows."""
import sys
from typing import TYPE_CHECKING, Tuple, Union, cast

from pynvim.api.buffer import Buffer
from pynvim.api.common import Remote

if sys.version_info < (3, 8):
    from typing_extensions import Literal, TypedDict
else:
    from typing import Literal, TypedDict

if TYPE_CHECKING:
    from pynvim.api.tabpage import Tabpage


__all__ = ['Window']

TWinChar = Union[str, Tuple[str, str]]
TWinManualBorder = Tuple[TWinChar, TWinChar, TWinChar, TWinChar,
                         TWinChar, TWinChar, TWinChar, TWinChar]
TWinBorder = Union[
    Literal['none'],
    Literal['single'],
    Literal['double'],
    Literal['rounded'],
    Literal['solid'],
    Literal['shadow'],
    TWinManualBorder,
]
TWinRelative = Union[Literal[''], Literal['editor'], Literal['win'], Literal['cursor']]
TWinAnchor = Union[Literal['NW'], Literal['NE'], Literal['SW'], Literal['SE']]


class WindowConfig(TypedDict, total=False):
    relative: TWinRelative
    focusable: bool
    external: bool
    win: 'Window'
    anchor: TWinAnchor
    width: int
    height: int
    bufpos: Tuple[int, int]
    row: Union[int, float]
    col: Union[int, float]
    zindex: int
    style: Literal['minimal']
    border: TWinBorder
    noautocmd: bool


class Window(Remote):

    """A remote Nvim window."""

    _api_prefix = "nvim_win_"

    @property
    def buffer(self) -> Buffer:
        """Get the `Buffer` currently being displayed by the window."""
        return self.request('nvim_win_get_buf')

    @buffer.setter
    def buffer(self, buffer: Union[int, Buffer]) -> None:
        """Set the `Buffer` to be displayed by the window."""
        return self.request('nvim_win_set_buf', buffer)

    @property
    def cursor(self) -> Tuple[int, int]:
        """Get the (row, col) tuple with the current cursor position."""
        return cast(Tuple[int, int], tuple(self.request('nvim_win_get_cursor')))

    @cursor.setter
    def cursor(self, pos: Tuple[int, int]) -> None:
        """Set the (row, col) tuple as the new cursor position."""
        return self.request('nvim_win_set_cursor', pos)

    @property
    def height(self) -> int:
        """Get the window height in rows."""
        return self.request('nvim_win_get_height')

    @height.setter
    def height(self, height: int) -> None:
        """Set the window height in rows."""
        return self.request('nvim_win_set_height', height)

    @property
    def width(self) -> int:
        """Get the window width in rows."""
        return self.request('nvim_win_get_width')

    @width.setter
    def width(self, width: int) -> None:
        """Set the window height in rows."""
        return self.request('nvim_win_set_width', width)

    @property
    def row(self) -> int:
        """0-indexed, on-screen window position(row) in display cells."""
        return self.request('nvim_win_get_position')[0]

    @property
    def col(self) -> int:
        """0-indexed, on-screen window position(col) in display cells."""
        return self.request('nvim_win_get_position')[1]

    @property
    def tabpage(self) -> 'Tabpage':
        """Get the `Tabpage` that contains the window."""
        return self.request('nvim_win_get_tabpage')

    @property
    def valid(self) -> bool:
        """Return True if the window still exists."""
        return self.request('nvim_win_is_valid')

    @property
    def number(self) -> int:
        """Get the window number."""
        return self.request('nvim_win_get_number')

    def close(self, force: bool) -> None:
        """Close the window."""
        return self.request('nvim_win_close', force)

    def hide(self) -> None:
        """Close the window and hide the buffer it contains."""
        return self.request('nvim_win_hide')

    @property
    def config(self) -> WindowConfig:
        """Gets the window configuration."""
        return self.request('nvim_win_get_config')

    @config.setter
    def config(self, config: WindowConfig) -> None:
        """Configures the window layout."""
        return self.request('nvim_win_set_config', config)
