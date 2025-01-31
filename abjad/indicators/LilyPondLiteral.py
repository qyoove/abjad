import typing
from abjad.lilypondnames.LilyPondTweakManager import LilyPondTweakManager
from abjad.system.FormatSpecification import FormatSpecification
from abjad.system.LilyPondFormatBundle import LilyPondFormatBundle
from abjad.system.StorageFormatManager import StorageFormatManager


class LilyPondLiteral(object):
    r"""
    LilyPond literal.

    ..  container:: example

        Dotted slur:

        >>> staff = abjad.Staff("c'8 d'8 e'8 f'8")
        >>> abjad.slur(staff[:])
        >>> literal = abjad.LilyPondLiteral(r'\slurDotted')
        >>> abjad.attach(literal, staff[0])
        >>> abjad.show(staff) # doctest: +SKIP

        ..  docs::

            >>> abjad.f(staff)
            \new Staff
            {
                \slurDotted
                c'8
                (
                d'8
                e'8
                f'8
                )
            }

    ..  container:: example

        Use the absolute before and absolute after format slots like this:

        >>> staff = abjad.Staff("c'8 d'8 e'8 f'8")
        >>> abjad.slur(staff[:])
        >>> literal = abjad.LilyPondLiteral(r'\slurDotted')
        >>> abjad.attach(literal, staff[0])
        >>> literal = abjad.LilyPondLiteral('', format_slot='absolute_before')
        >>> abjad.attach(literal, staff[0])
        >>> literal = abjad.LilyPondLiteral(
        ...     '% before all formatting',
        ...     format_slot='absolute_before',
        ...     )
        >>> abjad.attach(literal, staff[0])
        >>> literal = abjad.LilyPondLiteral('', format_slot='absolute_after')
        >>> abjad.attach(literal, staff[-1])
        >>> abjad.show(staff) # doctest: +SKIP

        ..  docs::

            >>> abjad.f(staff)
            \new Staff
            {
            <BLANKLINE>
                % before all formatting
                \slurDotted
                c'8
                (
                d'8
                e'8
                f'8
                )
            <BLANKLINE>
            }

    ..  container:: example

        LilyPond literals can be tagged:

        >>> staff = abjad.Staff("c'8 d'8 e'8 f'8")
        >>> abjad.slur(staff[:])
        >>> literal = abjad.LilyPondLiteral(r'\slurDotted')
        >>> abjad.attach(literal, staff[0], tag='RED')
        >>> abjad.show(staff) # doctest: +SKIP

        >>> abjad.f(staff)
        \new Staff
        {
            \slurDotted %! RED
            c'8
            (
            d'8
            e'8
            f'8
            )
        }

    ..  container:: example

        Multiline input is allowed:

        >>> staff = abjad.Staff("c'8 d'8 e'8 f'8")
        >>> abjad.slur(staff[:])
        >>> lines = [
        ...     r'\stopStaff',
        ...     r'\startStaff',
        ...     r'\once \override Staff.StaffSymbol.color = #red',
        ...     ]
        >>> literal = abjad.LilyPondLiteral(lines)
        >>> abjad.attach(literal, staff[2], tag='RED')
        >>> abjad.show(staff) # doctest: +SKIP

        >>> abjad.f(staff)
        \new Staff
        {
            c'8
            (
            d'8
            \stopStaff %! RED
            \startStaff %! RED
            \once \override Staff.StaffSymbol.color = #red %! RED
            e'8
            f'8
            )
        }

    ..  container:: example

        REGRESSION. Duplicate literals are allowed:

        >>> staff = abjad.Staff("c'4 d' e' f'")
        >>> literal = abjad.LilyPondLiteral('% text')
        >>> abjad.attach(literal, staff[0])
        >>> literal = abjad.LilyPondLiteral('% text')
        >>> abjad.attach(literal, staff[0])

        >>> abjad.f(staff)
        \new Staff
        {
            % text
            % text
            c'4
            d'4
            e'4
            f'4
        }

    """

    ### CLASS VARIABLES ###

    __slots__ = ("_argument", "_directed", "_format_slot", "_tweaks")

    _allowable_format_slots = (
        "absolute_after",
        "absolute_before",
        "after",
        "before",
        "closing",
        "opening",
    )

    _can_attach_to_containers = True

    _format_leaf_children = False

    ### INITIALIZER ###

    def __init__(
        self,
        argument: typing.Union[str, typing.List[str]] = "",
        # TODO: probaby change default to "before"
        format_slot: str = "opening",
        *,
        directed: bool = None,
        tweaks: LilyPondTweakManager = None,
    ) -> None:
        self._argument = argument
        assert format_slot in self._allowable_format_slots, repr(format_slot)
        self._format_slot = format_slot
        if directed is not None:
            directed = bool(directed)
        self._directed = directed
        if tweaks is not None:
            assert isinstance(tweaks, LilyPondTweakManager), repr(tweaks)
        self._tweaks = LilyPondTweakManager.set_tweaks(self, tweaks)

    ### SPECIAL METHODS ###

    def __eq__(self, argument) -> bool:
        """
        Is true when all initialization values of Abjad value object equal
        the initialization values of ``argument``.
        """
        return StorageFormatManager.compare_objects(self, argument)

    def __format__(self, format_specification="") -> str:
        """
        Formats LilyPond literal.
        """
        if format_specification in ("", "storage"):
            return StorageFormatManager(self).get_storage_format()
        assert format_specification == "lilypond"
        return str(self.argument)

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

    # TODO: activate this:
    #    def _before_attach(self, component):
    #        if self.format_slot not in component._allowable_format_slots:
    #            message = f"{type(component).__name__} does not accept"
    #            message += f" format slot {repr(self.format_slot)}."
    #            raise Exception(message)

    def _get_format_pieces(self):
        if isinstance(self.argument, str):
            return [self.argument]
        assert isinstance(self.argument, list)
        return self.argument[:]

    def _get_format_specification(self):
        return FormatSpecification(
            client=self,
            storage_format_args_values=[self.argument],
            storage_format_is_indented=False,
        )

    def _get_lilypond_format_bundle(self, component=None):
        bundle = LilyPondFormatBundle()
        format_slot = bundle.get(self.format_slot)
        if self.tweaks:
            tweaks = self.tweaks._list_format_contributions(
                directed=self.directed
            )
            format_slot.commands.extend(tweaks)
        pieces = self._get_format_pieces()
        format_slot.commands.extend(pieces)
        return bundle

    ### PUBLIC PROPERTIES ###

    @property
    def argument(self) -> typing.Union[str, typing.List[str]]:
        r"""
        Gets argument of LilyPond literal.

        ..  container:: example

            >>> literal = abjad.LilyPondLiteral(r'\slurDotted')
            >>> literal.argument
            '\\slurDotted'

        """
        return self._argument

    @property
    def directed(self) -> typing.Optional[bool]:
        r"""
        Is true when literal is directed.

        ..  container:: example

            Directed literal:

            >>> staff = abjad.Staff("c'4 d' e' f'")
            >>> literal = abjad.LilyPondLiteral(r'\f', 'after', directed=True)
            >>> abjad.tweak(literal).color = 'blue'
            >>> abjad.tweak(literal).dynamic_line_spanner.staff_padding = 5
            >>> abjad.attach(literal, staff[0])
            >>> abjad.show(staff) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(staff)
                \new Staff
                {
                    c'4
                    - \tweak DynamicLineSpanner.staff-padding #5
                    - \tweak color #blue
                    \f
                    d'4
                    e'4
                    f'4
                }

        ..  container:: example

            Nondirected literal:

            >>> staff = abjad.Staff("c'4 d' e' f'")
            >>> literal = abjad.LilyPondLiteral(
            ...     r'\breathe',
            ...     'after',
            ...     directed=False,
            ...     )
            >>> abjad.tweak(literal).color = 'blue'
            >>> abjad.attach(literal, staff[0])
            >>> abjad.show(staff) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(staff)
                \new Staff
                {
                    c'4
                    \tweak color #blue
                    \breathe
                    d'4
                    e'4
                    f'4
                }

        Proper use of the ``directed`` property entails searching the LilyPond
        docs to understand whether LilyPond treats any particular command as
        directed or not. Most LilyPond commands are directed. LilyPond insists
        that a few commands (include ``\breathe``, ``\key``, ``\mark``) must
        not be directed.
        """
        return self._directed

    @property
    def format_slot(self) -> str:
        r"""
        Gets format slot of LilyPond literal.

        ..  container:: example

            >>> literal = abjad.LilyPondLiteral(r'\slurDotted')
            >>> literal.format_slot
            'opening'

        """
        return self._format_slot

    @property
    def tweaks(self) -> typing.Optional[LilyPondTweakManager]:
        r"""
        Gets tweaks.

        ..  container:: example

            >>> staff = abjad.Staff("c'4 d' e' f'")
            >>> literal = abjad.LilyPondLiteral(r'\f', 'after', directed=True)
            >>> abjad.tweak(literal).color = 'blue'
            >>> abjad.attach(literal, staff[0])
            >>> abjad.show(staff) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(staff)
                \new Staff
                {
                    c'4
                    - \tweak color #blue
                    \f
                    d'4
                    e'4
                    f'4
                }

        """
        return self._tweaks

    ### PUBLIC METHODS ###

    @staticmethod
    def list_allowable_format_slots() -> typing.Tuple[str, ...]:
        """
        Lists allowable format slots.

        ..  container:: example

            >>> for slot in abjad.LilyPondLiteral.list_allowable_format_slots():
            ...     slot
            ...
            'absolute_after'
            'absolute_before'
            'after'
            'before'
            'closing'
            'opening'

        """
        return LilyPondLiteral._allowable_format_slots
