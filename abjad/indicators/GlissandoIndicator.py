import typing
from abjad import enums
from abjad import markups
from abjad import typings
from abjad.lilypondnames.LilyPondGrobOverride import LilyPondGrobOverride
from abjad.lilypondnames.LilyPondTweakManager import LilyPondTweakManager
from abjad.system.LilyPondFormatBundle import LilyPondFormatBundle
from abjad.system.StorageFormatManager import StorageFormatManager
from abjad.utilities.String import String


class GlissandoIndicator(object):
    r"""
    LilyPond ``\glissando`` command.

    ..  container:: example

        >>> staff = abjad.Staff("c'4 d' e' f'")
        >>> glissando = abjad.GlissandoIndicator()
        >>> abjad.tweak(glissando).color = 'blue'
        >>> abjad.attach(glissando, staff[0])
        >>> abjad.show(staff) # doctest: +SKIP

        ..  docs::

            >>> abjad.f(staff)
            \new Staff
            {
                c'4
                - \tweak color #blue
                \glissando
                d'4
                e'4
                f'4
            }

    ..  container:: example

        >>> abjad.GlissandoIndicator()
        GlissandoIndicator()

    """

    ### CLASS VARIABLES ###

    __slots__ = (
        "_allow_repeats",
        "_allow_ties",
        "_parenthesize_repeats",
        "_right_broken",
        "_stems",
        "_style",
        "_zero_padding",
        "_tweaks",
    )

    _context = "Voice"

    _persistent = True

    _publish_storage_format = True

    ### INITIALIZER ###

    def __init__(
        self,
        *,
        allow_repeats: bool = None,
        allow_ties: bool = None,
        parenthesize_repeats: bool = None,
        right_broken: bool = None,
        stems: bool = None,
        style: str = None,
        tweaks: LilyPondTweakManager = None,
        zero_padding: bool = None,
    ) -> None:
        if allow_repeats is not None:
            allow_repeats = bool(allow_repeats)
        self._allow_repeats = allow_repeats
        if allow_ties is not None:
            allow_ties = bool(allow_ties)
        self._allow_ties = allow_ties
        if parenthesize_repeats is not None:
            parenthesize_repeats = bool(parenthesize_repeats)
        self._parenthesize_repeats = parenthesize_repeats
        if right_broken is not None:
            right_broken = bool(right_broken)
        self._right_broken = right_broken
        if stems is not None:
            stems = bool(stems)
        self._stems = stems
        if style is not None:
            assert isinstance(style, str), repr(style)
        self._style = style
        if tweaks is not None:
            assert isinstance(tweaks, LilyPondTweakManager), repr(tweaks)
        self._tweaks = LilyPondTweakManager.set_tweaks(self, tweaks)
        if zero_padding is not None:
            zero_padding = bool(zero_padding)
        self._zero_padding = zero_padding

    ### SPECIAL METHODS ###

    def __eq__(self, argument) -> bool:
        """
        Is true when all initialization values of Abjad value object equal
        the initialization values of ``argument``.
        """
        return StorageFormatManager.compare_objects(self, argument)

    def __hash__(self) -> int:
        """
        Hashes Abjad value object.
        """
        hash_values = StorageFormatManager(self).get_hash_values()
        try:
            result = hash(hash_values)
        except TypeError:
            raise TypeError(f"unhashable type: {self}")
        return result

    def __repr__(self) -> str:
        """
        Gets interpreter representation.
        """
        return StorageFormatManager(self).get_repr_format()

    ### PRIVATE METHODS ###

    def _get_lilypond_format_bundle(self, component=None):
        bundle = LilyPondFormatBundle()
        strings = []
        if self.zero_padding:
            strings.append(r"- \abjad-zero-padding-glissando")
        if self.tweaks:
            tweaks = self.tweaks._list_format_contributions()
            strings.extend(tweaks)
        strings.append(r"\glissando")
        bundle.after.spanner_starts.extend(strings)
        return bundle

    ### PUBLIC PROPERTIES ###

    @property
    def context(self) -> str:
        """
        Returns (historically conventional) context ``'Voice'``.

        ..  container:: example

            >>> abjad.GlissandoIndicator().context
            'Voice'

        Class constant.

        Override with ``abjad.attach(..., context='...')``.
        """
        return self._context

    @property
    def persistent(self) -> bool:
        """
        Is true.

        ..  container:: example

            >>> abjad.GlissandoIndicator().persistent
            True

        Class constant.
        """
        return self._persistent

    @property
    def tweaks(self) -> typing.Optional[LilyPondTweakManager]:
        r"""
        Gets tweaks

        ..  container:: example

            >>> staff = abjad.Staff("c'4 d' e' f'")
            >>> glissando = abjad.GlissandoIndicator()
            >>> abjad.tweak(glissando).color = 'blue'
            >>> abjad.attach(glissando, staff[0])
            >>> abjad.show(staff) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(staff)
                \new Staff
                {
                    c'4
                    - \tweak color #blue
                    \glissando
                    d'4
                    e'4
                    f'4
                }

        """
        return self._tweaks

    @property
    def zero_padding(self) -> typing.Optional[bool]:
        r"""
        Is true when glissando formats with zero padding and no extra space for
        dots.

        ..  container:: example

            >>> staff = abjad.Staff("d'8 d'4. d'4. d'8")
            >>> abjad.glissando(
            ...     staff[:],
            ...     allow_repeats=True,
            ...     zero_padding=True,
            ...     )
            >>> for note in staff[1:]:
            ...     abjad.override(note).note_head.transparent = True
            ...     abjad.override(note).note_head.X_extent = (0, 0)
            ...
            >>> abjad.show(staff) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(staff)
                \new Staff
                {
                    d'8
                    - \abjad-zero-padding-glissando
                    \glissando
                    \once \override NoteHead.X-extent = #'(0 . 0)
                    \once \override NoteHead.transparent = ##t
                    d'4.
                    - \abjad-zero-padding-glissando
                    \glissando
                    \once \override NoteHead.X-extent = #'(0 . 0)
                    \once \override NoteHead.transparent = ##t
                    d'4.
                    - \abjad-zero-padding-glissando
                    \glissando
                    \once \override NoteHead.X-extent = #'(0 . 0)
                    \once \override NoteHead.transparent = ##t
                    d'8
                }

        ..  container:: example

            >>> staff = abjad.Staff("c'8. d'8. e'8. f'8.")
            >>> abjad.glissando(
            ...     staff[:],
            ...     zero_padding=True,
            ...     )
            >>> for note in staff[1:-1]:
            ...     abjad.override(note).note_head.transparent = True
            ...     abjad.override(note).note_head.X_extent = (0, 0)
            ...
            >>> abjad.show(staff) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(staff)
                \new Staff
                {
                    c'8.
                    - \abjad-zero-padding-glissando
                    \glissando
                    \once \override NoteHead.X-extent = #'(0 . 0)
                    \once \override NoteHead.transparent = ##t
                    d'8.
                    - \abjad-zero-padding-glissando
                    \glissando
                    \once \override NoteHead.X-extent = #'(0 . 0)
                    \once \override NoteHead.transparent = ##t
                    e'8.
                    - \abjad-zero-padding-glissando
                    \glissando
                    f'8.
                }

        """
        return self._zero_padding
