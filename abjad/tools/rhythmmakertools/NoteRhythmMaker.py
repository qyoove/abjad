# -*- encoding: utf-8 -*-
from abjad.tools import durationtools
from abjad.tools import mathtools
from abjad.tools import metertools
from abjad.tools import scoretools
from abjad.tools import spannertools
from abjad.tools.rhythmmakertools.RhythmMaker import RhythmMaker
from abjad.tools.topleveltools import attach
from abjad.tools.topleveltools import detach
from abjad.tools.topleveltools import iterate
from abjad.tools.topleveltools import new


class NoteRhythmMaker(RhythmMaker):
    r'''Note rhythm-maker.

    ..  container:: example

        Makes notes equal to the duration of input divisions. Adds ties where
        necessary:

        ::

            >>> maker = rhythmmakertools.NoteRhythmMaker()

        ::

            >>> divisions = [(5, 8), (3, 8)]
            >>> music = maker(divisions)
            >>> lilypond_file = rhythmmakertools.make_lilypond_file(
            ...     music,
            ...     divisions,
            ...     )
            >>> show(lilypond_file) # doctest: +SKIP

        ..  doctest::

            >>> staff = maker._get_rhythmic_staff(lilypond_file)
            >>> f(staff)
            \new RhythmicStaff {
                {
                    \time 5/8
                    c'2 ~
                    c'8
                }
                {
                    \time 3/8
                    c'4.
                }
            }

    Usage follows the two-step configure-once / call-repeatedly pattern shown
    here.
    '''

    ### CLASS VARIABLES ###

    __slots__ = (
        '_burnish_specifier',
        )

    _class_name_abbreviation = 'N'

    _human_readable_class_name = 'note rhythm-maker'

    ### INITIALIZER ###

    def __init__(
        self,
        beam_specifier=None,
        burnish_specifier=None,
        duration_spelling_specifier=None,
        tie_specifier=None,
        tuplet_spelling_specifier=None,
        ):
        from abjad.tools import rhythmmakertools
        RhythmMaker.__init__(
            self,
            beam_specifier=beam_specifier,
            duration_spelling_specifier=duration_spelling_specifier,
            tie_specifier=tie_specifier,
            tuplet_spelling_specifier=tuplet_spelling_specifier,
            )
        if burnish_specifier is not None:
            prototype = rhythmmakertools.BurnishSpecifier
            assert isinstance(burnish_specifier, prototype)
        self._burnish_specifier = burnish_specifier

    ### SPECIAL METHODS ###

    def __call__(self, divisions, seeds=None):
        r'''Calls note rhythm-maker on `divisions`.

        ..  container:: example

            ::

                >>> maker = rhythmmakertools.NoteRhythmMaker()
                >>> divisions = [(5, 8), (3, 8)]
                >>> result = maker(divisions)
                >>> for x in result:
                ...     x
                Selection(Note("c'2"), Note("c'8"))
                Selection(Note("c'4."),)

        Returns list of selections. Each selection holds one or more notes.
        '''
        return RhythmMaker.__call__(
            self,
            divisions,
            seeds=seeds,
            )

    def __eq__(self, arg):
        r'''True when `arg` is a note rhythm-maker with values of
        `beam_specifier`, `duration_spelling_specifier` and `tie_specifier`
        equal to those of this note rhythm-maker. Otherwise false.

        ..  container:: example

            ::

                >>> maker_1 = rhythmmakertools.NoteRhythmMaker()
                >>> tie_specifier = rhythmmakertools.TieSpecifier(
                ...     tie_across_divisions=True,
                ...     )
                >>> maker_2 = rhythmmakertools.NoteRhythmMaker(
                ...     tie_specifier=tie_specifier,
                ...     )

            ::

                >>> maker_1 == maker_1
                True
                >>> maker_1 == maker_2
                False
                >>> maker_2 == maker_1
                False
                >>> maker_2 == maker_2
                True

        Returns boolean.
        '''
        return RhythmMaker.__eq__(self, arg)

    def __format__(self, format_specification=''):
        r'''Formats note rhythm-maker.

        Set `format_specification` to `''` or `'storage'`.

        ..  container:: example

            ::

                >>> maker = rhythmmakertools.NoteRhythmMaker()
                >>> print(format(maker))
                rhythmmakertools.NoteRhythmMaker()

        Returns string.
        '''
        superclass = super(NoteRhythmMaker, self)
        return superclass.__format__(format_specification=format_specification)

    def __hash__(self):
        r'''Hashes note rhythm-maker.

        Required to be explicitely re-defined on Python 3 if __eq__ changes.

        Returns integer.
        '''
        return super(NoteRhythmMaker, self).__hash__()

    def __repr__(self):
        r'''Gets interpreter representation of note rhythm-maker.

        ..  container:: example

            ::

                >>> rhythmmakertools.NoteRhythmMaker()
                NoteRhythmMaker()

        Returns string.
        '''
        return RhythmMaker.__repr__(self)

    ### PRIVATE PROPERTIES ###

    @property
    def _attribute_manifest(self):
        from abjad.tools import rhythmmakertools
        from abjad.tools import systemtools
        return systemtools.AttributeManifest(
            systemtools.AttributeDetail(
                name='beam_specifier',
                command='bs',
                editor=rhythmmakertools.BeamSpecifier,
                ),
            systemtools.AttributeDetail(
                name='duration_spelling_specifier',
                command='dss',
                editor=rhythmmakertools.DurationSpellingSpecifier,
                ),
            systemtools.AttributeDetail(
                name='tie_specifier',
                command='ts',
                editor=rhythmmakertools.TieSpecifier,
                ),
            )

    ### PRIVATE METHODS ###

    def _apply_burnish_specifier(self, selections):
        if self.burnish_specifier is None:
            return selections
        elif self.burnish_specifier.outer_divisions_only:
            selections = self._burnish_outer_divisions(selections)
        else:
            selections = self._burnish_each_division(selections)
        return selections

    def _burnish_each_division(self, selections):
        message = 'NoteRhythmMaker does not yet implement'
        message += ' burnishing each division.'
        raise NotImplementedError(message)

    def _burnish_outer_divisions(self, selections):
        lefts = self.burnish_specifier.lefts
        left_lengths = self.burnish_specifier.left_lengths
        rights = self.burnish_specifier.rights
        right_lengths = self.burnish_specifier.right_lengths
        raise Exception(selections)

    def _make_music(self, divisions, seeds):
        from abjad.tools import rhythmmakertools
        selections = []
        duration_specifier = self.duration_spelling_specifier
        if duration_specifier is None:
            duration_specifier = rhythmmakertools.DurationSpellingSpecifier()
        tuplet_specifier = self.tuplet_spelling_specifier
        if tuplet_specifier is None:
            tuplet_specifier = rhythmmakertools.TupletSpellingSpecifier()
        for division in divisions:
            if (duration_specifier.spell_metrically == True or
                (duration_specifier.spell_metrically == 'unassignable' and
                not mathtools.is_assignable_integer(division.numerator))):
                meter = metertools.Meter(division)
                rhythm_tree_container = meter.root_node
                durations = [_.duration for _ in rhythm_tree_container]
            else:
                durations = [division]
            selection = scoretools.make_leaves(
                pitches=0,
                durations=durations,
                decrease_durations_monotonically=\
                    duration_specifier.decrease_durations_monotonically,
                forbidden_written_duration=\
                    duration_specifier.forbidden_written_duration,
                is_diminution=tuplet_specifier.is_diminution,
                )
            selections.append(selection)
        selections = self._apply_burnish_specifier(selections)
        self._apply_beam_specifier(selections)
        return selections

    ### PUBLIC PROPERTIES ###

    @property
    def burnish_specifier(self):
        r'''Gets burnish specifier of note rhythm-maker.

        Returns burnish specifier or none.
        '''
        return self._burnish_specifier

    @property
    def duration_spelling_specifier(self):
        r'''Gets duration spelling specifier of note rhythm-maker.

        ..  container:: example

            **Example 1.** Spells durations with the fewest number of glyphs:

            ::

                >>> maker = rhythmmakertools.NoteRhythmMaker()

            ::

                >>> divisions = [(5, 8), (3, 8)]
                >>> music = maker(divisions)
                >>> lilypond_file = rhythmmakertools.make_lilypond_file(
                ...     music,
                ...     divisions,
                ...     )
                >>> show(lilypond_file) # doctest: +SKIP

            ..  doctest::

                >>> staff = maker._get_rhythmic_staff(lilypond_file)
                >>> f(staff)
                \new RhythmicStaff {
                    {
                        \time 5/8
                        c'2 ~
                        c'8
                    }
                    {
                        \time 3/8
                        c'4.
                    }
                }

        ..  container:: example

            **Example 2.** Forbids notes with written duration greater than or 
            equal to ``1/2``:

            ::

                >>> maker = rhythmmakertools.NoteRhythmMaker(
                ...     duration_spelling_specifier=rhythmmakertools.DurationSpellingSpecifier(
                ...     forbidden_written_duration=Duration(1, 2),
                ...         ),
                ...     )

            ::

                >>> divisions = [(5, 8), (3, 8)]
                >>> music = maker(divisions)
                >>> lilypond_file = rhythmmakertools.make_lilypond_file(
                ...     music,
                ...     divisions,
                ...     )
                >>> show(lilypond_file) # doctest: +SKIP

            ..  doctest::

                >>> staff = maker._get_rhythmic_staff(lilypond_file)
                >>> f(staff)
                \new RhythmicStaff {
                    {
                        \time 5/8
                        c'4 ~
                        c'4 ~
                        c'8
                    }
                    {
                        \time 3/8
                        c'4.
                    }
                }

        ..  container:: example

            **Example 3.** Spells metrically all divisions metrically
            when `spell_metrically` is true:

            ::

                >>> maker = rhythmmakertools.NoteRhythmMaker(
                ...     duration_spelling_specifier=rhythmmakertools.DurationSpellingSpecifier(
                ...         spell_metrically=True,
                ...         ),
                ...     )

            ::

                >>> divisions = [(3, 4), (6, 16), (9, 16)]
                >>> music = maker(divisions)
                >>> lilypond_file = rhythmmakertools.make_lilypond_file(
                ...     music,
                ...     divisions,
                ...     )
                >>> show(lilypond_file) # doctest: +SKIP

            ..  doctest::

                >>> staff = maker._get_rhythmic_staff(lilypond_file)
                >>> f(staff)
                \new RhythmicStaff {
                    {
                        \time 3/4
                        c'4
                        c'4
                        c'4
                    }
                    {
                        \time 6/16
                        c'8. [
                        c'8. ]
                    }
                    {
                        \time 9/16
                        c'8. [
                        c'8.
                        c'8. ]
                    }
                }

        ..  container:: example

            **Example 4.** Spells unassignable durations metrically when
            `spell_metrically` is ``'unassignable'``:

            ::

                >>> maker = rhythmmakertools.NoteRhythmMaker(
                ...     duration_spelling_specifier=rhythmmakertools.DurationSpellingSpecifier(
                ...         spell_metrically='unassignable',
                ...         ),
                ...     )

            ::

                >>> divisions = [(3, 4), (6, 16), (9, 16)]
                >>> music = maker(divisions)
                >>> lilypond_file = rhythmmakertools.make_lilypond_file(
                ...     music,
                ...     divisions,
                ...     )
                >>> show(lilypond_file) # doctest: +SKIP

            ..  doctest::

                >>> staff = maker._get_rhythmic_staff(lilypond_file)
                >>> f(staff)
                \new RhythmicStaff {
                    {
                        \time 3/4
                        c'2.
                    }
                    {
                        \time 6/16
                        c'4.
                    }
                    {
                        \time 9/16
                        c'8. [
                        c'8.
                        c'8. ]
                    }
                }

            ``9/16`` is spelled metrically because it is unassignable.
            The other durations are spelled with the fewest number of symbols
            possible.

        Returns duration spelling specifier or none.
        '''
        return RhythmMaker.duration_spelling_specifier.fget(self)

    @property
    def tuplet_spelling_specifier(self):
        r'''Gets tuplet spelling specifier of note rhythm-maker.

        ..  container:: example

            **Example 1.** Spells tuplets as diminutions:

            ::

                >>> maker = rhythmmakertools.NoteRhythmMaker()

            ::

                >>> divisions = [(5, 14), (3, 7)]
                >>> music = maker(divisions)
                >>> lilypond_file = rhythmmakertools.make_lilypond_file(
                ...     music,
                ...     divisions,
                ...     )
                >>> show(lilypond_file) # doctest: +SKIP

            ..  doctest::

                >>> staff = maker._get_rhythmic_staff(lilypond_file)
                >>> f(staff)
                \new RhythmicStaff {
                    {
                        \time 5/14
                        \tweak #'edge-height #'(0.7 . 0)
                        \times 4/7 {
                            c'2 ~
                            c'8
                        }
                    }
                    {
                        \time 3/7
                        \tweak #'edge-height #'(0.7 . 0)
                        \times 4/7 {
                            c'2.
                        }
                    }
                }

            This is the default behavior.

        ..  container:: example

            **Example 2.** Spells tuplets as augmentations:

            ::

                >>> maker = rhythmmakertools.NoteRhythmMaker(
                ...     tuplet_spelling_specifier=rhythmmakertools.TupletSpellingSpecifier(
                ...         is_diminution=False,
                ...         ),
                ...     )

            ::

                >>> divisions = [(5, 14), (3, 7)]
                >>> music = maker(divisions)
                >>> lilypond_file = rhythmmakertools.make_lilypond_file(
                ...     music,
                ...     divisions,
                ...     )
                >>> show(lilypond_file) # doctest: +SKIP

            ..  doctest::

                >>> staff = maker._get_rhythmic_staff(lilypond_file)
                >>> f(staff)
                \new RhythmicStaff {
                    {
                        \time 5/14
                        \tweak #'text #tuplet-number::calc-fraction-text
                        \tweak #'edge-height #'(0.7 . 0)
                        \times 8/7 {
                            c'4 ~
                            c'16
                        }
                    }
                    {
                        \time 3/7
                        \tweak #'text #tuplet-number::calc-fraction-text
                        \tweak #'edge-height #'(0.7 . 0)
                        \times 8/7 {
                            c'4.
                        }
                    }
                }

        Returns tuplet spelling specifier or none.
        '''
        superclass = super(NoteRhythmMaker, self)
        return superclass.tuplet_spelling_specifier

    ### PUBLIC METHODS ###

    def reverse(self):
        r'''Reverses note rhythm-maker.

        ..  container:: example

            ::

                >>> maker = rhythmmakertools.NoteRhythmMaker()
                >>> reversed_maker = maker.reverse()

            ::

                >>> print(format(reversed_maker))
                rhythmmakertools.NoteRhythmMaker(
                    duration_spelling_specifier=rhythmmakertools.DurationSpellingSpecifier(
                        decrease_durations_monotonically=False,
                        ),
                    )

            ::

                >>> divisions = [(5, 8), (3, 8)]
                >>> music = maker(divisions)
                >>> lilypond_file = rhythmmakertools.make_lilypond_file(
                ...     music,
                ...     divisions,
                ...     )
                >>> show(lilypond_file) # doctest: +SKIP

            ..  doctest::

                >>> staff = maker._get_rhythmic_staff(lilypond_file)
                >>> f(staff)
                \new RhythmicStaff {
                    {
                        \time 5/8
                        c'2 ~
                        c'8
                    }
                    {
                        \time 3/8
                        c'4.
                    }
                }

        Defined equal to copy of note rhythm-maker with
        `duration_spelling_specifier` reversed.

        Returns new note rhythm-maker.
        '''
        from abjad.tools import rhythmmakertools
        duration_spelling_specifier = self.duration_spelling_specifier
        if duration_spelling_specifier is None:
            default = rhythmmakertools.DurationSpellingSpecifier()
            duration_spelling_specifier = default
        duration_spelling_specifier = duration_spelling_specifier.reverse()
        arguments = {
            'duration_spelling_specifier': duration_spelling_specifier,
            }
        result = new(self, **arguments)
        return result