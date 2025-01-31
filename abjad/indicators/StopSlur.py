import typing
from abjad import enums
from abjad.system.LilyPondFormatBundle import LilyPondFormatBundle
from abjad.system.StorageFormatManager import StorageFormatManager


class StopSlur(object):
    r"""
    LilyPond ``)`` command.

    ..  container:: example

        >>> abjad.StopSlur()
        StopSlur() 

    """

    ### CLASS VARIABLES ###

    __slots__ = ("_leak",)

    _context = "Voice"

    _parameter = "SLUR"

    _persistent = True

    _publish_storage_format = True

    _time_orientation = enums.Right

    ### INITIALIZER ###

    def __init__(self, *, leak: bool = None) -> None:
        if leak is not None:
            leak = bool(leak)
        self._leak = leak

    ### SPECIAL METHODS ###

    def __repr__(self) -> str:
        """
        Gets interpreter representation.
        """
        return StorageFormatManager(self).get_repr_format()

    ### PRIVATE METHODS ###

    def _get_lilypond_format_bundle(self, component=None):
        bundle = LilyPondFormatBundle()
        string = ")"
        if self.leak:
            string = f"<> {string}"
            bundle.after.leaks.append(string)
        else:
            bundle.after.spanner_stops.append(string)
        return bundle

    ### PUBLIC PROPERTIES ###

    @property
    def context(self) -> str:
        """
        Returns (historically conventional) context ``'Voice'``.

        ..  container:: example

            >>> abjad.StopSlur().context
            'Voice'

        Class constant.

        Override with ``abjad.attach(..., context='...')``.
        """
        return self._context

    @property
    def leak(self) -> typing.Optional[bool]:
        r"""
        Is true when stop slur leaks LilyPond ``<>`` empty chord.

        ..  container:: example

            Without leak:

            >>> staff = abjad.Staff("c'4 d' e' r")
            >>> command = abjad.StartSlur()
            >>> abjad.tweak(command).color = 'blue'
            >>> abjad.attach(command, staff[0])
            >>> command = abjad.StopSlur()
            >>> abjad.attach(command, staff[-2])
            >>> abjad.show(staff) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(staff)
                \new Staff
                {
                    c'4
                    - \tweak color #blue
                    (
                    d'4
                    e'4
                    )
                    r4
                }

            With leak:

            >>> staff = abjad.Staff("c'4 d' e' r")
            >>> command = abjad.StartSlur()
            >>> abjad.tweak(command).color = 'blue'
            >>> abjad.attach(command, staff[0])
            >>> command = abjad.StopSlur(leak=True)
            >>> abjad.attach(command, staff[-2])
            >>> abjad.show(staff) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(staff)
                \new Staff
                {
                    c'4
                    - \tweak color #blue
                    (
                    d'4
                    e'4
                    <> )
                    r4
                }

        ..  container:: example

            REGRESSION. Leaked contributions appear last in postevent format
            slot:

            >>> staff = abjad.Staff("c'8 d' e' f' r2")
            >>> abjad.beam(staff[:4])
            >>> command = abjad.StartSlur()
            >>> abjad.tweak(command).color = 'blue'
            >>> abjad.attach(command, staff[0])
            >>> command = abjad.StopSlur(leak=True)
            >>> abjad.attach(command, staff[3])
            >>> abjad.show(staff) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(staff)
                \new Staff
                {
                    c'8
                    [
                    - \tweak color #blue
                    (
                    d'8
                    e'8
                    f'8
                    ]
                    <> )
                    r2
                }

            The leaked text spanner above does not inadvertantly leak the beam.

        """
        return self._leak

    @property
    def parameter(self) -> str:
        """
        Returns ``'SLUR'``.

        ..  container:: example

            >>> abjad.StopSlur().parameter
            'SLUR'

        Class constant.
        """
        return self._parameter

    @property
    def persistent(self) -> bool:
        """
        Is true.

        ..  container:: example

            >>> abjad.StopSlur().persistent
            True

        Class constant.
        """
        return self._persistent

    @property
    def spanner_stop(self) -> bool:
        """
        Is true.

        ..  container:: example

            >>> abjad.StopSlur().spanner_stop
            True

        """
        return True
