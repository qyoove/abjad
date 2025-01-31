import collections
import typing
from abjad import enums
from abjad import typings
from abjad.markups import Markup
from abjad.mathtools import Ratio
from abjad.system.LilyPondFormatBundle import LilyPondFormatBundle
from abjad.system.StorageFormatManager import StorageFormatManager
from abjad.top.inspect import inspect
from abjad.top.new import new
from abjad.top.select import select
from abjad.utilities.Duration import Duration


class MetricModulation(object):
    r"""
    Metric modulation.

    ..  container:: example

        With notes:

        >>> metric_modulation = abjad.MetricModulation(
        ...     left_rhythm=abjad.Note("c'8."),
        ...     right_rhythm=abjad.Note("c'4."),
        ...     )

        >>> abjad.show(metric_modulation) # doctest: +SKIP

        ..  docs::

            >>> print(format(metric_modulation, 'lilypond'))
            \markup \abjad-metric-modulation #3 #1 #2 #1 #'(1 . 1)

    ..  container:: example

        With tuplets:

        >>> metric_modulation = abjad.MetricModulation(
        ...     left_rhythm=abjad.Tuplet((4, 5), "c'4"),
        ...     right_rhythm=abjad.Note("c'4"),
        ...     )

        >>> abjad.show(metric_modulation) # doctest: +SKIP

        ..  docs::

            >>> print(format(metric_modulation, 'lilypond'))
            \markup \abjad-metric-modulation-tuplet-lhs #2 #0 #4 #5 #2 #0 #'(1 . 1)

        >>> metric_modulation = abjad.MetricModulation(
        ...     left_rhythm=abjad.Note("c'4"),
        ...     right_rhythm=abjad.Tuplet((4, 5), "c'4"),
        ...     )

        >>> abjad.show(metric_modulation) # doctest: +SKIP

        ..  docs::

            >>> print(format(metric_modulation, 'lilypond'))
            \markup \abjad-metric-modulation-tuplet-rhs #2 #0 #2 #0 #4 #5 #'(1 . 1)

    ..  container:: example

        With tuplets again:

        >>> metric_modulation = abjad.MetricModulation(
        ...     left_rhythm=abjad.Note("c16."),
        ...     right_rhythm=abjad.Tuplet((2, 3), "c8"),
        ...     )

        >>> abjad.show(metric_modulation) # doctest: +SKIP

        ..  docs::

            >>> print(format(metric_modulation, 'lilypond'))
            \markup \abjad-metric-modulation-tuplet-rhs #4 #1 #3 #0 #2 #3 #'(1 . 1)

    ..  container:: example

        With ties:

        >>> maker = abjad.NoteMaker()
        >>> notes = maker([0], [(5, 16)])
        >>> metric_modulation = abjad.MetricModulation(
        ...     left_rhythm=abjad.Note("c'4"),
        ...     right_rhythm=notes,
        ...     )

        >>> abjad.show(metric_modulation) # doctest: +SKIP

        ..  docs::

            >>> print(format(metric_modulation, 'lilypond'))
            \markup {
                \score
                    {
                        \new Score
                        \with
                        {
                            \override SpacingSpanner.spacing-increment = #0.5
                            proportionalNotationDuration = ##f
                        }
                        <<
                            \new RhythmicStaff
                            \with
                            {
                                \remove Time_signature_engraver
                                \remove Staff_symbol_engraver
                                \override Stem.direction = #up
                                \override Stem.length = #5
                                \override TupletBracket.bracket-visibility = ##t
                                \override TupletBracket.direction = #up
                                \override TupletBracket.minimum-length = #4
                                \override TupletBracket.padding = #1.25
                                \override TupletBracket.shorten-pair = #'(-1 . -1.5)
                                \override TupletBracket.springs-and-rods = #ly:spanner::set-spacing-rods
                                \override TupletNumber.font-size = #0
                                \override TupletNumber.text = #tuplet-number::calc-fraction-text
                                tupletFullLength = ##t
                            }
                            {
                                c'4
                            }
                        >>
                        \layout {
                            indent = #0
                            ragged-right = ##t
                        }
                    }
                =
                \hspace
                    #-0.5
                \score
                    {
                        \new Score
                        \with
                        {
                            \override SpacingSpanner.spacing-increment = #0.5
                            proportionalNotationDuration = ##f
                        }
                        <<
                            \new RhythmicStaff
                            \with
                            {
                                \remove Time_signature_engraver
                                \remove Staff_symbol_engraver
                                \override Stem.direction = #up
                                \override Stem.length = #5
                                \override TupletBracket.bracket-visibility = ##t
                                \override TupletBracket.direction = #up
                                \override TupletBracket.minimum-length = #4
                                \override TupletBracket.padding = #1.25
                                \override TupletBracket.shorten-pair = #'(-1 . -1.5)
                                \override TupletBracket.springs-and-rods = #ly:spanner::set-spacing-rods
                                \override TupletNumber.font-size = #0
                                \override TupletNumber.text = #tuplet-number::calc-fraction-text
                                tupletFullLength = ##t
                            }
                            {
                                c'4
                                ~
                                c'16
                            }
                        >>
                        \layout {
                            indent = #0
                            ragged-right = ##t
                        }
                    }
                }

    ..  container:: example

        With ties and tuplets:

        >>> maker = abjad.NoteMaker()
        >>> notes = maker([0], [(5, 16)])
        >>> tuplet = abjad.Tuplet((2, 3), notes)
        >>> metric_modulation = abjad.MetricModulation(
        ...     left_rhythm=abjad.Note("c'4"),
        ...     right_rhythm=tuplet,
        ...     )

        >>> abjad.show(metric_modulation) # doctest: +SKIP

        ..  docs::

            >>> print(format(metric_modulation, 'lilypond'))
            \markup {
                \score
                    {
                        \new Score
                        \with
                        {
                            \override SpacingSpanner.spacing-increment = #0.5
                            proportionalNotationDuration = ##f
                        }
                        <<
                            \new RhythmicStaff
                            \with
                            {
                                \remove Time_signature_engraver
                                \remove Staff_symbol_engraver
                                \override Stem.direction = #up
                                \override Stem.length = #5
                                \override TupletBracket.bracket-visibility = ##t
                                \override TupletBracket.direction = #up
                                \override TupletBracket.minimum-length = #4
                                \override TupletBracket.padding = #1.25
                                \override TupletBracket.shorten-pair = #'(-1 . -1.5)
                                \override TupletBracket.springs-and-rods = #ly:spanner::set-spacing-rods
                                \override TupletNumber.font-size = #0
                                \override TupletNumber.text = #tuplet-number::calc-fraction-text
                                tupletFullLength = ##t
                            }
                            {
                                c'4
                            }
                        >>
                        \layout {
                            indent = #0
                            ragged-right = ##t
                        }
                    }
                =
                \hspace
                    #-0.5
                \score
                    {
                        \new Score
                        \with
                        {
                            \override SpacingSpanner.spacing-increment = #0.5
                            proportionalNotationDuration = ##f
                        }
                        <<
                            \new RhythmicStaff
                            \with
                            {
                                \remove Time_signature_engraver
                                \remove Staff_symbol_engraver
                                \override Stem.direction = #up
                                \override Stem.length = #5
                                \override TupletBracket.bracket-visibility = ##t
                                \override TupletBracket.direction = #up
                                \override TupletBracket.minimum-length = #4
                                \override TupletBracket.padding = #1.25
                                \override TupletBracket.shorten-pair = #'(-1 . -1.5)
                                \override TupletBracket.springs-and-rods = #ly:spanner::set-spacing-rods
                                \override TupletNumber.font-size = #0
                                \override TupletNumber.text = #tuplet-number::calc-fraction-text
                                tupletFullLength = ##t
                            }
                            {
                                \tweak edge-height #'(0.7 . 0)
                                \times 2/3 {
                                    c'4
                                    ~
                                    c'16
                                }
                            }
                        >>
                        \layout {
                            indent = #0
                            ragged-right = ##t
                        }
                    }
                }


    ..  container:: example

        Attach metric modulations to generate score output:

        >>> staff = abjad.Staff("c'4 d'4 e'4 f'4 e'4 d'4")
        >>> abjad.attach(abjad.TimeSignature((3, 4)), staff[0])
        >>> score = abjad.Score([staff])

        >>> metric_modulation = abjad.MetricModulation(
        ...     left_rhythm=abjad.Note("c4"),
        ...     right_rhythm=abjad.Note("c8."),
        ...     )
        >>> abjad.attach(metric_modulation, staff[3])
        >>> abjad.override(staff).text_script.staff_padding = 2.5

        >>> abjad.show(score) # doctest: +SKIP

        ..  docs::

            >>> abjad.f(score)
            \new Score
            <<
                \new Staff
                \with
                {
                    \override TextScript.staff-padding = #2.5
                }
                {
                    \time 3/4
                    c'4
                    d'4
                    e'4
                    f'4
                    ^ \markup \abjad-metric-modulation #2 #0 #3 #1 #'(1 . 1)
                    e'4
                    d'4
                }
            >>

    """

    ### CLASS VARIABLES ###

    __slots__ = (
        "_hide",
        "_left_markup",
        "_left_rhythm",
        "_right_markup",
        "_right_rhythm",
        "_scale",
    )

    _publish_storage_format = True

    ### INITIALIZER ###

    def __init__(
        self,
        left_rhythm=None,
        right_rhythm=None,
        *,
        hide: bool = None,
        left_markup: Markup = None,
        right_markup: Markup = None,
        scale: typing.Tuple[typings.Number, typings.Number] = (1, 1),
    ) -> None:
        from abjad.core.Note import Note

        if hide is not None:
            hide = bool(hide)
        self._hide = hide
        left_rhythm = left_rhythm or Note("c4")
        right_rhythm = right_rhythm or Note("c4")
        left_rhythm = self._initialize_rhythm(left_rhythm)
        self._left_rhythm = left_rhythm
        right_rhythm = self._initialize_rhythm(right_rhythm)
        self._right_rhythm = right_rhythm
        self._right_rhythm = right_rhythm
        if left_markup is not None:
            assert isinstance(left_markup, Markup)
        self._left_markup = left_markup
        if right_markup is not None:
            assert isinstance(right_markup, Markup)
        self._right_markup = right_markup
        assert isinstance(scale, tuple), repr(scale)
        self._scale = scale

    ### SPECIAL METHODS ###

    def __eq__(self, argument) -> bool:
        """
        Is true when ``argument`` is another metric modulation with the same
        ratio as this metric modulation.

        ..  container:: example

            >>> metric_modulation_1 = abjad.MetricModulation(
            ...     left_rhythm=abjad.Note("c'4"),
            ...     right_rhythm=abjad.Note("c'4."),
            ...     )
            >>> metric_modulation_2 = abjad.MetricModulation(
            ...     left_rhythm=abjad.Tuplet((2, 3), [abjad.Note("c'4")]),
            ...     right_rhythm=abjad.Note("c'4"),
            ...     )
            >>> maker = abjad.NoteMaker()
            >>> notes = maker([0], [(5, 16)])
            >>> metric_modulation_3 = abjad.MetricModulation(
            ...     left_rhythm=abjad.Note("c'4"),
            ...     right_rhythm=notes,
            ...     )

            >>> metric_modulation_1.ratio
            Ratio((2, 3))
            >>> metric_modulation_2.ratio
            Ratio((2, 3))
            >>> metric_modulation_3.ratio
            Ratio((4, 5))

            >>> metric_modulation_1 == metric_modulation_1
            True
            >>> metric_modulation_1 == metric_modulation_2
            True
            >>> metric_modulation_1 == metric_modulation_3
            False

            >>> metric_modulation_2 == metric_modulation_1
            True
            >>> metric_modulation_2 == metric_modulation_2
            True
            >>> metric_modulation_2 == metric_modulation_3
            False

            >>> metric_modulation_3 == metric_modulation_1
            False
            >>> metric_modulation_3 == metric_modulation_2
            False
            >>> metric_modulation_3 == metric_modulation_3
            True

        """
        # custom definition because input rhythms don't compare:
        if isinstance(argument, type(self)):
            if self.ratio == argument.ratio:
                return True
        return False

    def __format__(self, format_specification="") -> str:
        """
        Formats metric modulation.

        ..  container:: example

            >>> metric_modulation = abjad.MetricModulation(
            ...     left_rhythm=abjad.Note("c'4"),
            ...     right_rhythm=abjad.Note("c'4."),
            ...     )

            >>> abjad.f(metric_modulation)
            abjad.MetricModulation(
                left_rhythm=abjad.Selection(
                    [
                        abjad.Note("c'4"),
                        ]
                    ),
                right_rhythm=abjad.Selection(
                    [
                        abjad.Note("c'4."),
                        ]
                    ),
                scale=(1, 1),
                )

        """
        if format_specification in ("", "storage"):
            return StorageFormatManager(self).get_storage_format()
        return str(self)

    def __hash__(self) -> int:
        """
        Hashes metric modulation.

        Redefined in tandem with __eq__.
        """
        hash_values = StorageFormatManager(self).get_hash_values()
        try:
            result = hash(hash_values)
        except TypeError:
            raise TypeError(f"unhashable type: {self}")
        return result

    def __illustrate__(self):
        r"""
        Illustrates metric modulation.

        ..  container:: example

            >>> metric_modulation = abjad.MetricModulation(
            ...     left_rhythm=abjad.Tuplet((2, 3), "c'4"),
            ...     right_rhythm=abjad.Note("c'4."),
            ...     )
            >>> abjad.show(metric_modulation) # doctest: +SKIP

            ..  docs::

                >>> lilypond_file = metric_modulation.__illustrate__()
                >>> metric_modulation = lilypond_file.items[-1]
                >>> print(format(metric_modulation))
                \markup \abjad-metric-modulation-tuplet-lhs #2 #0 #2 #3 #2 #1 #'(1 . 1)

        Returns LilyPond file.
        """
        import abjad

        lilypond_file = abjad.LilyPondFile.new()
        lilypond_file.items.append(self._get_markup())
        return lilypond_file

    def __repr__(self) -> str:
        """
        Gets interpreter representation.
        """
        return StorageFormatManager(self).get_repr_format()

    def __str__(self) -> str:
        r"""
        Gets string representation of metric modulation.

        ..  container:: example

            >>> metric_modulation = abjad.MetricModulation(
            ...     left_rhythm=abjad.Tuplet((2, 3), [abjad.Note("c'4")]),
            ...     right_rhythm=abjad.Note("c'4"),
            ...     )

            >>> print(str(metric_modulation))
            \markup \abjad-metric-modulation-tuplet-lhs #2 #0 #2 #3 #2 #0 #'(1 . 1)

        """
        return str(self._get_markup())

    ### PRIVATE METHODS ###

    def _get_compact_output(self):
        import abjad

        if self._note_to_note():
            arguments = self._get_markup_arguments()
            left_exponent, left_dots, right_exponent, right_dots = arguments
            string = r"\abjad-metric-modulation"
            string += f" #{left_exponent} #{left_dots}"
            string += f" #{right_exponent} #{right_dots}"
        elif self._rhs_tuplet():
            arguments = self._get_markup_arguments()
            note_exponent, note_dots = arguments[:2]
            tuplet_exponent, tuplet_dots, tuplet_n, tuplet_d = arguments[2:]
            string = r"\abjad-metric-modulation-tuplet-rhs"
            string += f" #{note_exponent} #{note_dots}"
            string += f" #{tuplet_exponent} #{tuplet_dots}"
            string += f" #{tuplet_n} #{tuplet_d}"
        elif self._lhs_tuplet():
            arguments = self._get_markup_arguments()
            tuplet_exponent, tuplet_dots, tuplet_n, tuplet_d = arguments[:4]
            note_exponent, note_dots = arguments[4:]
            string = r"\abjad-metric-modulation-tuplet-lhs"
            string += f" #{tuplet_exponent} #{tuplet_dots}"
            string += f" #{tuplet_n} #{tuplet_d}"
            string += f" #{note_exponent} #{note_dots}"
        else:
            return None
        string += f" #'({self.scale[0]} . {self.scale[1]})"
        return string

    def _get_left_markup(self):
        if self.left_markup is not None:
            return self.left_markup
        markup = Duration._to_score_markup(self.left_rhythm)
        return markup

    def _get_lilypond_format(self):
        return str(self)

    def _get_lilypond_format_bundle(self, component=None):
        bundle = LilyPondFormatBundle()
        if not self.hide:
            markup = self._get_markup()
            markup = new(markup, direction=enums.Up)
            markup_format_pieces = markup._get_format_pieces()
            bundle.after.markup.extend(markup_format_pieces)
        return bundle

    def _get_markup(self):
        result = self._get_compact_output()
        if result is None:
            left_markup = self._get_left_markup()
            equal = Markup("=")
            right_space = Markup.hspace(-0.5)
            right_markup = self._get_right_markup()
            markup = left_markup + equal + right_space + right_markup
        else:
            markup = Markup(rf"\markup {result}", literal=True)
        return markup

    def _get_markup_arguments(self):
        if self._note_to_note():
            left_exponent = self.left_rhythm[0].written_duration.exponent
            left_dots = self.left_rhythm[0].written_duration.dot_count
            right_exponent = self.right_rhythm[0].written_duration.exponent
            right_dots = self.right_rhythm[0].written_duration.dot_count
            return (left_exponent, left_dots, right_exponent, right_dots)
        elif self._lhs_tuplet():
            tuplet_exponent = self.left_rhythm[0][0].written_duration.exponent
            tuplet_dots = self.left_rhythm[0][0].written_duration.dot_count
            tuplet_n = self.left_rhythm[0].multiplier.numerator
            tuplet_d = self.left_rhythm[0].multiplier.denominator
            note_exponent = self.right_rhythm[0].written_duration.exponent
            note_dots = self.right_rhythm[0].written_duration.dot_count
            return (
                tuplet_exponent,
                tuplet_dots,
                tuplet_n,
                tuplet_d,
                note_exponent,
                note_dots,
            )
        elif self._rhs_tuplet():
            note_exponent = self.left_rhythm[0].written_duration.exponent
            note_dots = self.left_rhythm[0].written_duration.dot_count
            tuplet_exponent = self.right_rhythm[0][0].written_duration.exponent
            tuplet_dots = self.right_rhythm[0][0].written_duration.dot_count
            tuplet_n = self.right_rhythm[0].multiplier.numerator
            tuplet_d = self.right_rhythm[0].multiplier.denominator
            return (
                note_exponent,
                note_dots,
                tuplet_exponent,
                tuplet_dots,
                tuplet_n,
                tuplet_d,
            )
        else:
            raise Exception("implement tied note values.")

    def _get_right_markup(self):
        if self.right_markup is not None:
            return self.right_markup
        markup = Duration._to_score_markup(self.right_rhythm)
        return markup

    def _initialize_rhythm(self, rhythm):
        import abjad

        if isinstance(rhythm, abjad.Component):
            selection = select([rhythm])
        elif isinstance(rhythm, abjad.Selection):
            selection = rhythm
        else:
            message = "rhythm must be duration, component or selection: {!r}."
            message = message.format(rhythm)
            raise TypeError(message)
        assert isinstance(selection, abjad.Selection)
        return selection

    def _lhs_tuplet(self):
        import abjad

        if (
            isinstance(self.left_rhythm[0], abjad.Tuplet)
            and len(self.left_rhythm[0]) == 1
            and isinstance(self.right_rhythm[0], abjad.Note)
            and len(self.right_rhythm) == 1
        ):
            return True
        return False

    def _note_to_note(self):
        import abjad

        if (
            isinstance(self.left_rhythm[0], abjad.Note)
            and len(self.left_rhythm) == 1
            and isinstance(self.right_rhythm[0], abjad.Note)
            and len(self.right_rhythm) == 1
        ):
            return True
        return False

    def _rhs_tuplet(self):
        import abjad

        if (
            isinstance(self.left_rhythm[0], abjad.Note)
            and len(self.left_rhythm) == 1
            and isinstance(self.right_rhythm[0], abjad.Tuplet)
            and len(self.right_rhythm[0]) == 1
        ):
            return True
        return False

    ### PUBLIC PROPERTIES ###

    @property
    def hide(self) -> typing.Optional[bool]:
        """
        Is true when metric modulation generates no LilyPond output.
        """
        return self._hide

    @property
    def left_markup(self) -> typing.Optional[Markup]:
        """
        Gets left markup of metric modulation.

        ..  container:: example

            >>> metric_modulation = abjad.MetricModulation(
            ...     left_rhythm=abjad.Note("c'4"),
            ...     right_rhythm=abjad.Note("c'4."),
            ...     )
            >>> metric_modulation.left_markup

        """
        return self._left_markup

    @property
    def left_rhythm(self):
        """
        Gets left rhythm of metric modulation.

        ..  container:: example

            >>> metric_modulation = abjad.MetricModulation(
            ...     left_rhythm=abjad.Note("c'4"),
            ...     right_rhythm=abjad.Note("c'4."),
            ...     )
            >>> metric_modulation.left_rhythm
            Selection([Note("c'4")])

        Returns selection.
        """
        return self._left_rhythm

    @property
    def ratio(self) -> Ratio:
        """
        Gets ratio of metric modulation.

        ..  container:: example

            >>> metric_modulation = abjad.MetricModulation(
            ...     left_rhythm=abjad.Tuplet((2, 3), [abjad.Note("c'4")]),
            ...     right_rhythm=abjad.Note("c'4"),
            ...     )
            >>> metric_modulation.ratio
            Ratio((2, 3))

        """
        left_duration = inspect(self.left_rhythm).duration()
        right_duration = inspect(self.right_rhythm).duration()
        duration = left_duration / right_duration
        ratio = Ratio(duration.pair)
        return ratio

    @property
    def right_markup(self) -> typing.Optional[Markup]:
        r"""Gets right markup of metric modulation.

        ..  container:: example

            >>> metric_modulation = abjad.MetricModulation(
            ...     left_rhythm=abjad.Note("c'4"),
            ...     right_rhythm=abjad.Note("c'4."),
            ...     )
            >>> metric_modulation.right_markup

        """
        return self._right_markup

    @property
    def right_rhythm(self):
        """
        Gets right tempo of metric modulation.

        ..  container:: example

            >>> metric_modulation = abjad.MetricModulation(
            ...     left_rhythm=abjad.Note("c'4"),
            ...     right_rhythm=abjad.Note("c'4."),
            ...     )
            >>> metric_modulation.right_rhythm
            Selection([Note("c'4.")])

        """
        return self._right_rhythm

    @property
    def scale(self) -> typing.Tuple[typings.Number, typings.Number]:
        r"""
        Gets scale of output markup.

        ..  container:: example

            >>> staff = abjad.Staff("c'4 d'4 e'4 f'4 e'4 d'4")
            >>> abjad.attach(abjad.TimeSignature((3, 4)), staff[0])
            >>> score = abjad.Score([staff])

            >>> metric_modulation = abjad.MetricModulation(
            ...     left_rhythm=abjad.Note("c4"),
            ...     right_rhythm=abjad.Note("c8."),
            ...     scale=(0.5, 0.5),
            ...     )
            >>> abjad.attach(metric_modulation, staff[3])
            >>> abjad.override(staff).text_script.staff_padding = 2.5

            >>> abjad.show(score) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(score)
                \new Score
                <<
                    \new Staff
                    \with
                    {
                        \override TextScript.staff-padding = #2.5
                    }
                    {
                        \time 3/4
                        c'4
                        d'4
                        e'4
                        f'4
                        ^ \markup \abjad-metric-modulation #2 #0 #3 #1 #'(0.5 . 0.5)
                        e'4
                        d'4
                    }
                >>

        """
        return self._scale

    @property
    def tweaks(self) -> None:
        """
        Are not implemented on metric modulation.
        """
        pass
