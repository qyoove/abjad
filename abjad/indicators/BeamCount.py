import typing
from abjad import enums
from abjad.system.LilyPondFormatBundle import LilyPondFormatBundle
from abjad.system.StorageFormatManager import StorageFormatManager


class BeamCount(object):
    r"""
    LilyPond ``\setLeftBeamCount``, ``\setRightBeamCount`` command.

    ..  container:: example

        >>> abjad.BeamCount()
        BeamCount(left=0, right=0) 

    """

    ### CLASS VARIABLES ###

    __slots__ = ("_left", "_right")

    _publish_storage_format = True

    ### INITIALIZER ###

    def __init__(self, left: int = 0, right: int = 0) -> None:
        assert isinstance(left, int), repr(left)
        self._left = left
        assert isinstance(right, int), repr(right)
        self._right = right

    ### SPECIAL METHODS ###

    def __repr__(self) -> str:
        """
        Gets interpreter representation.
        """
        return StorageFormatManager(self).get_repr_format()

    ### PRIVATE METHODS ###

    def _get_lilypond_format_bundle(self, component=None):
        bundle = LilyPondFormatBundle()
        string = rf"\set stemLeftBeamCount = {self.left}"
        bundle.before.commands.append(string)
        string = rf"\set stemRightBeamCount = {self.right}"
        bundle.before.commands.append(string)
        return bundle

    ### PUBLIC PROPERTIES ###

    @property
    def left(self) -> int:
        """
        Gets stem left beam count.
        """
        return self._left

    @property
    def right(self) -> int:
        """
        Gets stem right beam count.
        """
        return self._right
