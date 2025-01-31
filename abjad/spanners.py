"""
Classes and functions for modeling spanners: beams, hairpins, slurs, etc.
"""
import typing
from abjad import enums
from abjad import typings
from abjad.core.Chord import Chord
from abjad.core.Component import Component
from abjad.core.Leaf import Leaf
from abjad.core.MultimeasureRest import MultimeasureRest
from abjad.core.Note import Note
from abjad.core.Rest import Rest
from abjad.core.Selection import Selection
from abjad.core.Skip import Skip
from abjad.core.Staff import Staff
from abjad.indicators.BeamCount import BeamCount
from abjad.indicators.BendAfter import BendAfter
from abjad.indicators.BowContactPoint import BowContactPoint
from abjad.indicators.BowMotionTechnique import BowMotionTechnique
from abjad.indicators.Dynamic import Dynamic
from abjad.indicators.GlissandoIndicator import GlissandoIndicator
from abjad.indicators.StartHairpin import StartHairpin
from abjad.indicators.LilyPondLiteral import LilyPondLiteral
from abjad.indicators.Ottava import Ottava
from abjad.indicators.RepeatTie import RepeatTie
from abjad.indicators.StartBeam import StartBeam
from abjad.indicators.StartGroup import StartGroup
from abjad.indicators.StartPhrasingSlur import StartPhrasingSlur
from abjad.indicators.StartPianoPedal import StartPianoPedal
from abjad.indicators.StartSlur import StartSlur
from abjad.indicators.StartTextSpan import StartTextSpan
from abjad.indicators.StartTrillSpan import StartTrillSpan
from abjad.indicators.StopBeam import StopBeam
from abjad.indicators.StopGroup import StopGroup
from abjad.indicators.StopHairpin import StopHairpin
from abjad.indicators.StopSlur import StopSlur
from abjad.indicators.StopPhrasingSlur import StopPhrasingSlur
from abjad.indicators.StopPianoPedal import StopPianoPedal
from abjad.indicators.StopTextSpan import StopTextSpan
from abjad.indicators.StopTrillSpan import StopTrillSpan
from abjad.indicators.Tie import Tie
from abjad.lilypondnames.LilyPondTweakManager import IndexedTweakManager
from abjad.lilypondnames.LilyPondTweakManager import LilyPondTweakManager
from abjad.scheme import SchemeSymbol
from abjad.system.Tag import Tag
from abjad.system.Tags import Tags
from abjad.top.attach import attach
from abjad.top.detach import detach
from abjad.top.inspect import inspect
from abjad.top.iterate import iterate
from abjad.top.new import new
from abjad.top.override import override
from abjad.top.select import select
from abjad.top.setting import setting
from abjad.top.tweak import tweak
from abjad.utilities.Duration import Duration
from abjad.utilities.DurationInequality import DurationInequality
from abjad.utilities.Expression import Expression
from abjad.utilities.Sequence import Sequence

abjad_tags = Tags()


def _apply_tweaks(argument, tweaks, i=None, total=None):
    if not tweaks:
        return
    manager = tweak(argument)
    for item in tweaks:
        if isinstance(item, tuple):
            assert len(item) == 2
            manager_, i_ = item
            if 0 <= i_ and i_ != i:
                continue
            if i_ < 0 and i_ != -(total - i):
                continue
        else:
            manager_ = item
        assert isinstance(manager_, LilyPondTweakManager)
        tuples = manager_._get_attribute_tuples()
        for attribute, value in tuples:
            setattr(manager, attribute, value)


def beam(
    argument: typing.Union[Component, Selection],
    *,
    beam_lone_notes: bool = None,
    # beam_rests: bool = None,
    beam_rests: typing.Optional[bool] = True,
    durations: typing.Sequence[Duration] = None,
    selector: typings.SelectorTyping = "abjad.select().leaves()",
    span_beam_count: int = None,
    start_beam: StartBeam = None,
    stemlet_length: typings.Number = None,
    stop_beam: StopBeam = None,
    tag: str = None,
) -> None:
    r"""
    Attaches beam indicators.

    ..  container:: example

        >>> staff = abjad.Staff("c'8 d' e' f'")
        >>> abjad.beam(staff[:])
        >>> abjad.show(staff) # doctest: +SKIP

        ..  docs::

            >>> abjad.f(staff)
            \new Staff
            {
                c'8
                [
                d'8
                e'8
                f'8
                ]
            }

    """
    # import allows eval statement
    import abjad

    if isinstance(selector, str):
        selector = eval(selector)
    assert isinstance(selector, Expression)
    argument = selector(argument)
    original_leaves = iterate(argument).leaves()
    original_leaves = list(original_leaves)

    silent_prototype = (MultimeasureRest, Rest, Skip)

    def _is_beamable(argument, beam_rests=False):
        if isinstance(argument, (Chord, Note)):
            if 0 < argument.written_duration.flag_count:
                return True
        if beam_rests and isinstance(argument, silent_prototype):
            return True
        return False

    leaves = []
    for leaf in original_leaves:
        if not _is_beamable(leaf, beam_rests=beam_rests):
            continue
        leaves.append(leaf)
    # print(leaves, 'LLL')
    runs = []
    run = []
    run.extend(leaves[:1])
    for leaf in leaves[1:]:
        this_index = original_leaves.index(run[-1])
        that_index = original_leaves.index(leaf)
        if this_index + 1 == that_index:
            run.append(leaf)
        else:
            selection = select(run)
            runs.append(selection)
            run = [leaf]
    if run:
        selection = select(run)
        runs.append(selection)
    runs_ = select(runs)
    # print(runs, 'RRR', len(runs))
    # print()
    if not beam_lone_notes:
        runs_ = runs_.nontrivial()
    for run in runs_:
        # print(run, 'RRR')
        if all(isinstance(_, silent_prototype) for _ in run):
            continue
        start_leaf = run[0]
        stop_leaf = run[-1]
        start_beam_ = start_beam or StartBeam()
        stop_beam_ = stop_beam or StopBeam()
        detach(StartBeam, start_leaf)
        attach(start_beam_, start_leaf, tag=tag)
        detach(StopBeam, stop_leaf)
        attach(stop_beam_, stop_leaf, tag=tag)

        # for leaf in run:
        #    print(leaf, inspect(leaf).indicators())

        if stemlet_length is None:
            continue
        staff = inspect(start_leaf).parentage().get(Staff)
        lilypond_type = getattr(staff, "lilypond_type", "Staff")
        string = r"\override {}.Stem.stemlet-length = {}"
        string = string.format(lilypond_type, stemlet_length)
        literal = LilyPondLiteral(string)
        for indicator in inspect(start_leaf).indicators():
            if indicator == literal:
                break
        else:
            attach(literal, start_leaf, tag=tag)
        staff = inspect(stop_leaf).parentage().get(Staff)
        lilypond_type = getattr(staff, "lilypond_type", "Staff")
        string = rf"\revert {lilypond_type}.Stem.stemlet-length"
        literal = LilyPondLiteral(string)
        for indicator in inspect(stop_leaf).indicators():
            if indicator == literal:
                break
        else:
            attach(literal, stop_leaf, tag=tag)

    if not durations:
        return

    if len(original_leaves) == 1:
        return

    def _leaf_neighbors(leaf, original_leaves):
        assert leaf is not original_leaves[0]
        assert leaf is not original_leaves[-1]
        this_index = original_leaves.index(leaf)
        previous_leaf = original_leaves[this_index - 1]
        previous = 0
        if _is_beamable(previous_leaf, beam_rests=beam_rests):
            previous = previous_leaf.written_duration.flag_count
        next_leaf = original_leaves[this_index + 1]
        next_ = 0
        if _is_beamable(next_leaf, beam_rests=beam_rests):
            next_ = next_leaf.written_duration.flag_count
        return previous, next_

    span_beam_count = span_beam_count or 1
    durations = [Duration(_) for _ in durations]
    leaf_durations = [inspect(_).duration() for _ in original_leaves]
    leaf_durations_ = Sequence(leaf_durations)
    parts = leaf_durations_.partition_by_weights(durations, overhang=True)
    part_counts = [len(_) for _ in parts]
    original_leaves = Sequence(original_leaves)
    parts = original_leaves.partition_by_counts(part_counts)
    total_parts = len(parts)
    for i, part in enumerate(parts):
        is_first_part = False
        if i == 0:
            is_first_part = True
        is_last_part = False
        if i == total_parts - 1:
            is_last_part = True
        first_leaf = part[0]
        flag_count = first_leaf.written_duration.flag_count
        if len(part) == 1:
            if not _is_beamable(first_leaf, beam_rests=False):
                continue
            left = flag_count
            right = flag_count
            beam_count = BeamCount(left, right)
            attach(beam_count, first_leaf, tag=tag)
            continue
        if _is_beamable(first_leaf, beam_rests=False):
            if is_first_part:
                left = 0
            else:
                left = span_beam_count
            beam_count = BeamCount(left, flag_count)
            attach(beam_count, first_leaf, tag=tag)
        last_leaf = part[-1]
        if _is_beamable(last_leaf, beam_rests=False):
            flag_count = last_leaf.written_duration.flag_count
            if is_last_part:
                left = flag_count
                right = 0
            else:
                previous, next_ = _leaf_neighbors(last_leaf, original_leaves)
                if previous == next_ == 0:
                    left = right = flag_count
                elif previous == 0:
                    left = 0
                    right = flag_count
                elif next_ == 0:
                    left = flag_count
                    right = 0
                elif previous == flag_count:
                    left = flag_count
                    right = min(span_beam_count, next_)
                elif flag_count == next_:
                    left = min(previous, flag_count)
                    right = flag_count
                else:
                    left = flag_count
                    right = min(previous, flag_count)
            beam_count = BeamCount(left, right)
            attach(beam_count, last_leaf, tag=tag)

        # TODO: eventually remove middle leaf beam counts?
        for middle_leaf in part[1:-1]:
            if not _is_beamable(middle_leaf, beam_rests=beam_rests):
                continue
            if isinstance(middle_leaf, silent_prototype):
                continue
            flag_count = middle_leaf.written_duration.flag_count
            previous, next_ = _leaf_neighbors(middle_leaf, original_leaves)
            if previous == next_ == 0:
                left = right = flag_count
            elif previous == 0:
                left = 0
                right = flag_count
            elif next_ == 0:
                left = flag_count
                right = 0
            elif previous == flag_count:
                left = flag_count
                right = min(flag_count, next_)
            elif flag_count == next_:
                left = min(previous, flag_count)
                right = flag_count
            else:
                left = min(previous, flag_count)
                right = flag_count
            beam_count = BeamCount(left, right)
            attach(beam_count, middle_leaf, tag=tag)


def bow_contact_spanner(
    argument, *, omit_bow_changes: bool = None, tag: str = None
) -> None:
    r"""
    Attaches bow contact format indicators.

    ..  container:: example

        >>> staff = abjad.Staff()
        >>> staff.extend(r"c'4. c'8 \times 2/3 { c'4 c'4 c'4 }")

        >>> leaves = abjad.select(staff).leaves()
        >>> abjad.attach(abjad.BowMotionTechnique('jete'), leaves[0])
        >>> abjad.attach(abjad.BowContactPoint((1, 4)), leaves[0])
        >>> abjad.attach(abjad.BowContactPoint((3, 4)), leaves[1])
        >>> abjad.attach(abjad.BowContactPoint((1, 2)), leaves[2])
        >>> abjad.attach(abjad.BowMotionTechnique('circular'), leaves[3])
        >>> abjad.attach(abjad.BowContactPoint((1, 1)), leaves[3])
        >>> abjad.attach(abjad.BowContactPoint((0, 1)), leaves[4])

        >>> abjad.attach(abjad.Clef('percussion'), leaves[0])
        >>> abjad.override(staff).bar_line.transparent = True
        >>> abjad.override(staff).dots.staff_position = -8
        >>> abjad.override(staff).flag.Y_offset = -8.5
        >>> abjad.override(staff).glissando.bound_details__left__padding = 1.5
        >>> abjad.override(staff).glissando.bound_details__right__padding = 1.5
        >>> abjad.override(staff).glissando.thickness = 2
        >>> abjad.override(staff).script.staff_padding = 3
        >>> abjad.override(staff).staff_symbol.transparent = True
        >>> abjad.override(staff).stem.direction = abjad.Down
        >>> abjad.override(staff).stem.length = 8
        >>> abjad.override(staff).stem.stem_begin_position = -9
        >>> abjad.override(staff).time_signature.stencil = False

        >>> abjad.bow_contact_spanner(leaves)
        >>> abjad.show(staff) # doctest: +SKIP

        ..  docs::

            >>> abjad.f(staff)
            \new Staff
            \with
            {
                \override BarLine.transparent = ##t
                \override Dots.staff-position = #-8
                \override Flag.Y-offset = #-8.5
                \override Glissando.bound-details.left.padding = #1.5
                \override Glissando.bound-details.right.padding = #1.5
                \override Glissando.thickness = #2
                \override Script.staff-padding = #3
                \override StaffSymbol.transparent = ##t
                \override Stem.direction = #down
                \override Stem.length = #8
                \override Stem.stem-begin-position = #-9
                \override TimeSignature.stencil = ##f
            }
            {
                \clef "percussion"
                \tweak Y-offset #-1.0
                \tweak stencil #ly:text-interface::print
                \tweak text \markup {
                    \center-align
                        \vcenter
                            \fraction
                                1
                                4
                    }
                c'4.
                - \tweak style #'dotted-line
                \glissando
                ^ \downbow
                \tweak Y-offset #1.0
                \tweak stencil #ly:text-interface::print
                \tweak text \markup {
                    \center-align
                        \vcenter
                            \fraction
                                3
                                4
                    }
                c'8
                \glissando
                ^ \upbow
                \times 2/3 {
                    \tweak Y-offset #0.0
                    \tweak stencil #ly:text-interface::print
                    \tweak text \markup {
                        \center-align
                            \vcenter
                                \fraction
                                    1
                                    2
                        }
                    c'4
                    \glissando
                    ^ \downbow
                    \tweak Y-offset #2.0
                    \tweak stencil #ly:text-interface::print
                    \tweak text \markup {
                        \center-align
                            \vcenter
                                \fraction
                                    1
                                    1
                        }
                    c'4
                    - \tweak style #'zigzag
                    \glissando
                    ^ \upbow
                    \tweak Y-offset #-2.0
                    \tweak stencil #ly:text-interface::print
                    \tweak text \markup {
                        \center-align
                            \vcenter
                                \fraction
                                    0
                                    1
                        }
                    c'4
                }
            }

    ..  container:: example

        Set ``omit_bow_changes`` to true to suppress up-bow and down-bown
        indicators:

        >>> staff = abjad.Staff()
        >>> staff.extend(r"c'4. c'8 \times 2/3 { c'4 c'4 c'4 }")

        >>> leaves = abjad.select(staff).leaves()
        >>> abjad.attach(abjad.BowMotionTechnique('jete'), leaves[0])
        >>> abjad.attach(abjad.BowContactPoint((1, 4)), leaves[0])
        >>> abjad.attach(abjad.BowContactPoint((3, 4)), leaves[1])
        >>> abjad.attach(abjad.BowContactPoint((1, 2)), leaves[2])
        >>> abjad.attach(abjad.BowMotionTechnique('circular'), leaves[3])
        >>> abjad.attach(abjad.BowContactPoint((1, 1)), leaves[3])
        >>> abjad.attach(abjad.BowContactPoint((0, 1)), leaves[4])

        >>> abjad.attach(abjad.Clef('percussion'), leaves[0])
        >>> abjad.override(staff).bar_line.transparent = True
        >>> abjad.override(staff).dots.staff_position = -8
        >>> abjad.override(staff).flag.Y_offset = -8.5
        >>> abjad.override(staff).glissando.bound_details__left__padding = 1.5
        >>> abjad.override(staff).glissando.bound_details__right__padding = 1.5
        >>> abjad.override(staff).glissando.thickness = 2
        >>> abjad.override(staff).script.staff_padding = 3
        >>> abjad.override(staff).staff_symbol.transparent = True
        >>> abjad.override(staff).stem.direction = abjad.Down
        >>> abjad.override(staff).stem.length = 8
        >>> abjad.override(staff).stem.stem_begin_position = -9
        >>> abjad.override(staff).time_signature.stencil = False

        >>> abjad.bow_contact_spanner(leaves, omit_bow_changes=True)
        >>> abjad.show(staff) # doctest: +SKIP

        ..  docs::

            >>> abjad.f(staff)
            \new Staff
            \with
            {
                \override BarLine.transparent = ##t
                \override Dots.staff-position = #-8
                \override Flag.Y-offset = #-8.5
                \override Glissando.bound-details.left.padding = #1.5
                \override Glissando.bound-details.right.padding = #1.5
                \override Glissando.thickness = #2
                \override Script.staff-padding = #3
                \override StaffSymbol.transparent = ##t
                \override Stem.direction = #down
                \override Stem.length = #8
                \override Stem.stem-begin-position = #-9
                \override TimeSignature.stencil = ##f
            }
            {
                \clef "percussion"
                \tweak Y-offset #-1.0
                \tweak stencil #ly:text-interface::print
                \tweak text \markup {
                    \center-align
                        \vcenter
                            \fraction
                                1
                                4
                    }
                c'4.
                - \tweak style #'dotted-line
                \glissando
                \tweak Y-offset #1.0
                \tweak stencil #ly:text-interface::print
                \tweak text \markup {
                    \center-align
                        \vcenter
                            \fraction
                                3
                                4
                    }
                c'8
                \glissando
                \times 2/3 {
                    \tweak Y-offset #0.0
                    \tweak stencil #ly:text-interface::print
                    \tweak text \markup {
                        \center-align
                            \vcenter
                                \fraction
                                    1
                                    2
                        }
                    c'4
                    \glissando
                    \tweak Y-offset #2.0
                    \tweak stencil #ly:text-interface::print
                    \tweak text \markup {
                        \center-align
                            \vcenter
                                \fraction
                                    1
                                    1
                        }
                    c'4
                    - \tweak style #'zigzag
                    \glissando
                    \tweak Y-offset #-2.0
                    \tweak stencil #ly:text-interface::print
                    \tweak text \markup {
                        \center-align
                            \vcenter
                                \fraction
                                    0
                                    1
                        }
                    c'4
                }
            }

    ..  container:: example

        Use ``BowContactPoint(None)`` to indicate unbowed actions, such as
        pizzicato:

        >>> staff = abjad.Staff(r"c'4 c'4 c'4 c'4")

        >>> leaves = staff[:]
        >>> abjad.attach(abjad.BowContactPoint(None), leaves[0])
        >>> abjad.attach(abjad.BowContactPoint((3, 4)), leaves[1])
        >>> abjad.attach(abjad.BowContactPoint((1, 2)), leaves[2])
        >>> abjad.attach(abjad.BowContactPoint(None), leaves[3])

        >>> abjad.attach(abjad.Clef('percussion'), staff[0])
        >>> abjad.override(staff).bar_line.transparent = True
        >>> abjad.override(staff).dots.staff_position = -8
        >>> abjad.override(staff).flag.Y_offset = -8.5
        >>> abjad.override(staff).glissando.bound_details__left__padding = 1.5
        >>> abjad.override(staff).glissando.bound_details__right__padding = 1.5
        >>> abjad.override(staff).glissando.thickness = 2
        >>> abjad.override(staff).script.staff_padding = 3
        >>> abjad.override(staff).staff_symbol.transparent = True
        >>> abjad.override(staff).stem.direction =abjad.Down
        >>> abjad.override(staff).stem.length = 8
        >>> abjad.override(staff).stem.stem_begin_position = -9
        >>> abjad.override(staff).time_signature.stencil = False

        >>> abjad.bow_contact_spanner(leaves)
        >>> abjad.show(staff) # doctest: +SKIP

        ..  docs::

            >>> abjad.f(staff)
            \new Staff
            \with
            {
                \override BarLine.transparent = ##t
                \override Dots.staff-position = #-8
                \override Flag.Y-offset = #-8.5
                \override Glissando.bound-details.left.padding = #1.5
                \override Glissando.bound-details.right.padding = #1.5
                \override Glissando.thickness = #2
                \override Script.staff-padding = #3
                \override StaffSymbol.transparent = ##t
                \override Stem.direction = #down
                \override Stem.length = #8
                \override Stem.stem-begin-position = #-9
                \override TimeSignature.stencil = ##f
            }
            {
                \clef "percussion"
                \tweak style #'cross
                c'4
                \tweak Y-offset #1.0
                \tweak stencil #ly:text-interface::print
                \tweak text \markup {
                    \center-align
                        \vcenter
                            \fraction
                                3
                                4
                    }
                c'4
                \glissando
                ^ \upbow
                \tweak Y-offset #0.0
                \tweak stencil #ly:text-interface::print
                \tweak text \markup {
                    \center-align
                        \vcenter
                            \fraction
                                1
                                2
                    }
                c'4
                \tweak style #'cross
                c'4
            }

    """

    def _get_indicators(leaf):
        inspector = inspect(leaf)
        bow_contact_point = None
        prototype = BowContactPoint
        if inspector.has_indicator(prototype):
            bow_contact_point = inspector.indicator(prototype)
        bow_motion_technique = None
        prototype = BowMotionTechnique
        if inspector.has_indicator(prototype):
            bow_motion_technique = inspector.indicator(prototype)
        return (bow_contact_point, bow_motion_technique)

    def _make_bow_contact_point_tweaks(leaf, bow_contact_point):
        if bow_contact_point is None:
            return
        tweak(leaf.note_head).stencil = "ly:text-interface::print"
        tweak(leaf.note_head).text = bow_contact_point.markup
        y_offset = float((4 * bow_contact_point.contact_point) - 2)
        tweak(leaf.note_head).Y_offset = y_offset

    def _make_bow_change_contributions(leaf, leaves, bow_contact_point):
        cautionary_change = False
        direction_change = None
        next_leaf = inspect(leaf).leaf(1)
        this_contact_point = bow_contact_point
        if this_contact_point is None:
            return
        next_contact_point = inspect(next_leaf).indicator(BowContactPoint)
        if next_contact_point is None:
            return
        previous_leaf = inspect(leaf).leaf(-1)
        previous_contact_point = None
        if previous_leaf is not None:
            previous_contact_points = inspect(previous_leaf).indicators(
                BowContactPoint
            )
            if previous_contact_points:
                previous_contact_point = previous_contact_points[0]
        if (
            leaf is leaves[0]
            or previous_contact_point is None
            or previous_contact_point.contact_point is None
        ):
            if this_contact_point < next_contact_point:
                direction_change = enums.Down
            elif next_contact_point < this_contact_point:
                direction_change = enums.Up
        else:
            previous_leaf = inspect(leaf).leaf(-1)
            previous_contact_point = inspect(previous_leaf).indicator(
                BowContactPoint
            )
            if (
                previous_contact_point < this_contact_point
                and next_contact_point < this_contact_point
            ):
                direction_change = enums.Up
            elif (
                this_contact_point < previous_contact_point
                and this_contact_point < next_contact_point
            ):
                direction_change = enums.Down
            elif this_contact_point == previous_contact_point:
                if this_contact_point < next_contact_point:
                    cautionary_change = True
                    direction_change = enums.Down
                elif next_contact_point < this_contact_point:
                    cautionary_change = True
                    direction_change = enums.Up
        if direction_change is None:
            return
        if direction_change == enums.Up:
            string = r"\upbow"
        else:
            string = r"\downbow"
        if cautionary_change:
            string = rf"\parenthesize {string}"
        string = "^ " + string
        literal = LilyPondLiteral(string, "after")
        attach(literal, leaf)

    def _next_leaf_is_bowed(leaf, leaves):
        if leaf is leaves[-1]:
            return False
        silent_prototype = (MultimeasureRest, Rest, Skip)
        next_leaf = inspect(leaf).leaf(1)
        if next_leaf is None or isinstance(next_leaf, silent_prototype):
            return False
        next_contact_point = inspect(next_leaf).indicator(BowContactPoint)
        if next_contact_point is None:
            return False
        elif next_contact_point.contact_point is None:
            return False
        return True

    def _format_leaf(leaf, leaves):
        indicators = _get_indicators(leaf)
        bow_contact_point = indicators[0]
        bow_motion_technique = indicators[1]
        if bow_contact_point is None:
            return
        if bow_contact_point.contact_point is None:
            tweak(leaf.note_head).style = "cross"
            return
        if len(leaves) == 1:
            return
        _make_bow_contact_point_tweaks(leaf, bow_contact_point)
        if not _next_leaf_is_bowed(leaf, leaves):
            return
        glissando = GlissandoIndicator()
        if bow_motion_technique is not None:
            style = SchemeSymbol(bow_motion_technique.glissando_style)
            tweak(glissando).style = style
        attach(glissando, leaf, tag=tag)
        if not omit_bow_changes:
            _make_bow_change_contributions(leaf, leaves, bow_contact_point)

    leaves = select(argument).leaves()
    for leaf in leaves:
        _format_leaf(leaf, leaves)


def glissando(
    argument,
    *tweaks: IndexedTweakManager,
    allow_repeats: bool = None,
    allow_ties: bool = None,
    hide_middle_note_heads: bool = None,
    hide_middle_stems: bool = None,
    left_broken: bool = None,
    parenthesize_repeats: bool = None,
    right_broken: bool = None,
    right_broken_show_next: bool = None,
    style: str = None,
    tag: str = None,
    zero_padding: bool = None,
):
    r"""
    Attaches glissando indicators.

    ..  container:: example

        >>> staff = abjad.Staff("c'8 d'8 e'8 f'8")
        >>> abjad.glissando(staff[:])
        >>> abjad.show(staff) # doctest: +SKIP

        ..  docs::

            >>> abjad.f(staff)
            \new Staff
            {
                c'8
                \glissando
                d'8
                \glissando
                e'8
                \glissando
                f'8
            }

    ..  container:: example

        Glissando avoids bend-after indicators:

        >>> staff = abjad.Staff("c'8 d'8 e'8 f'8")
        >>> bend_after = abjad.BendAfter()
        >>> abjad.attach(bend_after, staff[1])
        >>> abjad.glissando(staff[:])
        >>> abjad.show(staff) # doctest: +SKIP

        ..  docs::

            >>> abjad.f(staff)
            \new Staff
            {
                c'8
                \glissando
                d'8
                - \bendAfter #'-4
                e'8
                \glissando
                f'8
            }

    ..  container:: example

        Does not allow repeated pitches:

        >>> staff = abjad.Staff("a8 a8 b8 ~ b8 c'8 c'8 d'8 ~ d'8")
        >>> abjad.glissando(
        ...     staff[:],
        ...     allow_repeats=False,
        ...     )
        >>> abjad.show(staff) # doctest: +SKIP

        ..  docs::

            >>> abjad.f(staff)
            \new Staff
            {
                a8
                a8
                \glissando
                b8
                ~
                b8
                \glissando
                c'8
                c'8
                \glissando
                d'8
                ~
                d'8
            }

    ..  container:: example

        Allows repeated pitches (but not ties):

        >>> staff = abjad.Staff("a8 a8 b8 ~ b8 c'8 c'8 d'8 ~ d'8")
        >>> abjad.glissando(
        ...     staff[:],
        ...     allow_repeats=True,
        ...     )
        >>> abjad.show(staff) # doctest: +SKIP

        ..  docs::

            >>> abjad.f(staff)
            \new Staff
            {
                a8
                \glissando
                a8
                \glissando
                b8
                ~
                b8
                \glissando
                c'8
                \glissando
                c'8
                \glissando
                d'8
                ~
                d'8
            }

    ..  container:: example

        Allows both repeated pitches and ties:

        >>> staff = abjad.Staff("a8 a8 b8 ~ b8 c'8 c'8 d'8 ~ d'8")
        >>> abjad.glissando(
        ...     staff[:],
        ...     allow_repeats=True,
        ...     allow_ties=True,
        ...     )
        >>> abjad.show(staff) # doctest: +SKIP

        ..  docs::

            >>> abjad.f(staff)
            \new Staff
            {
                a8
                \glissando
                a8
                \glissando
                b8
                ~
                \glissando
                b8
                \glissando
                c'8
                \glissando
                c'8
                \glissando
                d'8
                ~
                \glissando
                d'8
            }

        Ties are excluded when repeated pitches are not allowed because all
        ties comprise repeated pitches.

    ..  container:: example

        Spans and parenthesizes repeated pitches:

        >>> staff = abjad.Staff("a8 a8 b8 ~ b8 c'8 c'8 d'8 ~ d'8")
        >>> abjad.glissando(
        ...     staff[:],
        ...     allow_repeats=True,
        ...     parenthesize_repeats=True,
        ...     )
        >>> abjad.show(staff) # doctest: +SKIP

        ..  docs::

            >>> abjad.f(staff)
            \new Staff
            {
                a8
                \glissando
                \parenthesize
                a8
                \glissando
                b8
                ~
                \parenthesize
                b8
                \glissando
                c'8
                \glissando
                \parenthesize
                c'8
                \glissando
                d'8
                ~
                \parenthesize
                d'8
            }

    ..  container:: example

        Parenthesizes (but does not span) repeated pitches:

        >>> staff = abjad.Staff("a8 a8 b8 ~ b8 c'8 c'8 d'8 ~ d'8")
        >>> abjad.glissando(
        ...     staff[:],
        ...     parenthesize_repeats=True,
        ...     )
        >>> abjad.show(staff) # doctest: +SKIP

        ..  docs::

            >>> abjad.f(staff)
            \new Staff
            {
                a8
                \parenthesize
                a8
                \glissando
                b8
                ~
                \parenthesize
                b8
                \glissando
                c'8
                \parenthesize
                c'8
                \glissando
                d'8
                ~
                \parenthesize
                d'8
            }

    ..  container:: example

        With ``hide_middle_note_heads`` set to true:

        >>> staff = abjad.Staff("c'8 d'8 e'8 f'8")
        >>> abjad.glissando(
        ...     staff[:],
        ...     hide_middle_note_heads=True,
        ...     )
        >>> abjad.show(staff) # doctest: +SKIP

        ..  docs::

            >>> abjad.f(staff)
            \new Staff
            {
                c'8
                \glissando
                \hide NoteHead
                \override Accidental.stencil = ##f
                \override NoteColumn.glissando-skip = ##t
                \override NoteHead.no-ledgers = ##t
                d'8
                e'8
                \revert Accidental.stencil
                \revert NoteColumn.glissando-skip
                \revert NoteHead.no-ledgers
                \undo \hide NoteHead
                f'8
            }

    ..  container:: example

        With ``hide_middle_note_heads`` and ``hide_middle_stems`` both set to
        true:

        >>> staff = abjad.Staff("c'8 d'8 e'8 f'8")
        >>> abjad.glissando(
        ...     staff[:],
        ...     hide_middle_note_heads=True,
        ...     hide_middle_stems=True,
        ...     )
        >>> abjad.show(staff) # doctest: +SKIP

        ..  docs::

            >>> abjad.f(staff)
            \new Staff
            {
                c'8
                \glissando
                \hide NoteHead
                \override Accidental.stencil = ##f
                \override NoteColumn.glissando-skip = ##t
                \override NoteHead.no-ledgers = ##t
                \override Dots.transparent = ##t
                \override Stem.transparent = ##t
                d'8
                e'8
                \revert Accidental.stencil
                \revert NoteColumn.glissando-skip
                \revert NoteHead.no-ledgers
                \undo \hide NoteHead
                \revert Dots.transparent
                \revert Stem.transparent
                f'8
            }

        ..  note:: Respects ``hide_middle_stems`` only when
            ``hide_middle_note_heads`` is set to true.

    ..  container:: example

        With right-broken set to true:

        >>> staff = abjad.Staff("c'8 d'8 e'8 f'8")
        >>> abjad.glissando(
        ...     staff[:],
        ...     right_broken=True,
        ...     )
        >>> abjad.show(staff) # doctest: +SKIP

        LilyPond output looks like this:

        >>> abjad.f(staff, strict=50)
        \new Staff
        {
            c'8
            \glissando
            d'8
            \glissando
            e'8
            \glissando
            f'8
        %@% \glissando                                    %! SHOW_TO_JOIN_BROKEN_SPANNERS
        }

    ..  container:: example

        With right-broken set to true and ``hide_middle_note_heads`` set to
        true:

        >>> staff = abjad.Staff("c'8 d'8 e'8 f'8")
        >>> abjad.glissando(
        ...     staff[:],
        ...     right_broken=True,
        ...     hide_middle_note_heads=True,
        ...     )
        >>> abjad.show(staff) # doctest: +SKIP

        LilyPond output looks like this:

        >>> abjad.f(staff, strict=50)
        \new Staff
        {
            c'8
            \glissando
            \hide NoteHead
            \override Accidental.stencil = ##f
            \override NoteColumn.glissando-skip = ##t
            \override NoteHead.no-ledgers = ##t
            d'8
            e'8
            \revert Accidental.stencil                    %! HIDE_TO_JOIN_BROKEN_SPANNERS
            \revert NoteColumn.glissando-skip             %! HIDE_TO_JOIN_BROKEN_SPANNERS
            \revert NoteHead.no-ledgers                   %! HIDE_TO_JOIN_BROKEN_SPANNERS
            \undo \hide NoteHead                          %! HIDE_TO_JOIN_BROKEN_SPANNERS
            f'8
        }

    ..  container:: example

        With ``right_broken``, ``hide_middle_note_heads`` and
        ``right_broken_show_next`` all set to true:

        >>> staff = abjad.Staff("c'8 d'8 e'8 f'8")
        >>> abjad.glissando(
        ...     staff[:],
        ...     hide_middle_note_heads=True,
        ...     right_broken=True,
        ...     right_broken_show_next=True,
        ...     )
        >>> abjad.show(staff) # doctest: +SKIP

        LilyPond output looks like this:

        >>> abjad.f(staff, strict=50)
        \new Staff
        {
            c'8
            \glissando
            \hide NoteHead
            \override Accidental.stencil = ##f
            \override NoteColumn.glissando-skip = ##t
            \override NoteHead.no-ledgers = ##t
            d'8
            e'8
            \revert Accidental.stencil                    %! HIDE_TO_JOIN_BROKEN_SPANNERS
            \revert NoteColumn.glissando-skip             %! HIDE_TO_JOIN_BROKEN_SPANNERS
            \revert NoteHead.no-ledgers                   %! HIDE_TO_JOIN_BROKEN_SPANNERS
            \undo \hide NoteHead                          %! HIDE_TO_JOIN_BROKEN_SPANNERS
            f'8
        %@% \revert Accidental.stencil                    %! SHOW_TO_JOIN_BROKEN_SPANNERS
        %@% \revert NoteColumn.glissando-skip             %! SHOW_TO_JOIN_BROKEN_SPANNERS
        %@% \revert NoteHead.no-ledgers                   %! SHOW_TO_JOIN_BROKEN_SPANNERS
        %@% \undo \hide NoteHead                          %! SHOW_TO_JOIN_BROKEN_SPANNERS
        }

    ..  container:: example

        With left-broken set to true (and ``hide_middle_note_heads`` set to
        true):

        >>> staff = abjad.Staff("c'8 d'8 e'8 f'8")
        >>> abjad.glissando(
        ...     staff[:],
        ...     left_broken=True,
        ...     hide_middle_note_heads=True,
        ...     )
        >>> abjad.show(staff) # doctest: +SKIP

        LilyPond output looks like this:

        >>> abjad.f(staff, strict=50)
        \new Staff
        {
            \hide NoteHead                                %! HIDE_TO_JOIN_BROKEN_SPANNERS
            \override Accidental.stencil = ##f            %! HIDE_TO_JOIN_BROKEN_SPANNERS
            \override NoteHead.no-ledgers = ##t           %! HIDE_TO_JOIN_BROKEN_SPANNERS
            c'8
            \glissando
            \override NoteColumn.glissando-skip = ##t     %! HIDE_TO_JOIN_BROKEN_SPANNERS
            d'8
            e'8
            \revert Accidental.stencil
            \revert NoteColumn.glissando-skip
            \revert NoteHead.no-ledgers
            \undo \hide NoteHead
            f'8
        }

        ..  note:: Respects left-broken only with ``hide_middle_note_heads``
            set to true.

    ..  container:: example

        With tweaks applied to every glissando command:

        >>> staff = abjad.Staff("c'8 d'8 e'8 f'8")
        >>> abjad.glissando(
        ...     staff[:],
        ...     abjad.tweak('trill').style,
        ...     )
        >>> abjad.show(staff) # doctest: +SKIP

        ..  docs::

            >>> abjad.f(staff)
            \new Staff
            {
                c'8
                - \tweak style #'trill
                \glissando
                d'8
                - \tweak style #'trill
                \glissando
                e'8
                - \tweak style #'trill
                \glissando
                f'8
            }

    ..  container:: example

        With zero padding on fixed pitch:

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

        With zero padding on moving pitch:

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

    ..  container:: example

        With indexed tweaks:

        >>> staff = abjad.Staff("d'4 d' d' d'")
        >>> abjad.glissando(
        ...     staff[:],
        ...     (abjad.tweak('red').color, 0),
        ...     (abjad.tweak('red').color, -1),
        ...     allow_repeats=True,
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
                d'4
                - \abjad-zero-padding-glissando
                - \tweak color #red
                \glissando
                \once \override NoteHead.X-extent = #'(0 . 0)
                \once \override NoteHead.transparent = ##t
                d'4
                - \abjad-zero-padding-glissando
                \glissando
                \once \override NoteHead.X-extent = #'(0 . 0)
                \once \override NoteHead.transparent = ##t
                d'4
                - \abjad-zero-padding-glissando
                - \tweak color #red
                \glissando
                d'4
            }

    """

    if right_broken_show_next and not right_broken:
        message = "set right_broken_show_next only when right_broken is true."
        raise Exception(message)

    if hide_middle_stems and not hide_middle_note_heads:
        message = "set hide_middle_stems only when"
        message += " hide_middle_note_heads is true."
        raise Exception(message)

    def _is_last_in_tie_chain(leaf):
        logical_tie = leaf._get_logical_tie()
        return leaf is logical_tie[-1]

    def _next_leaf_changes_current_pitch(leaf):
        next_leaf = inspect(leaf).leaf(n=1)
        if (
            isinstance(leaf, Note)
            and isinstance(next_leaf, Note)
            and leaf.written_pitch == next_leaf.written_pitch
        ):
            return False
        elif (
            isinstance(leaf, Chord)
            and isinstance(next_leaf, Chord)
            and leaf.written_pitches == next_leaf.written_pitches
        ):
            return False
        return True

    def _parenthesize_leaf(leaf):
        if isinstance(leaf, Note):
            leaf.note_head.is_parenthesized = True
        elif isinstance(leaf, Chord):
            for note_head in leaf.note_heads:
                note_head.is_parenthesized = True

    def _previous_leaf_changes_current_pitch(leaf):
        previous_leaf = inspect(leaf).leaf(n=-1)
        if (
            isinstance(leaf, Note)
            and isinstance(previous_leaf, Note)
            and leaf.written_pitch == previous_leaf.written_pitch
        ):
            return False
        elif (
            isinstance(leaf, Chord)
            and isinstance(previous_leaf, Chord)
            and leaf.written_pitches == previous_leaf.written_pitches
        ):
            return False
        return True

    leaves = select(argument).leaves()
    total = len(leaves) - 1
    for i, leaf in enumerate(leaves):
        if leaf is not leaves[0]:
            if parenthesize_repeats:
                if not _previous_leaf_changes_current_pitch(leaf):
                    _parenthesize_leaf(leaf)
        should_attach_glissando = False
        deactivate_glissando = None
        if inspect(leaf).has_indicator(BendAfter):
            pass
        elif leaf is leaves[-1]:
            if right_broken is True:
                should_attach_glissando = True
                deactivate_glissando = True
        elif not isinstance(leaf, (Chord, Note)):
            pass
        elif allow_repeats and allow_ties:
            should_attach_glissando = True
        elif allow_repeats and not allow_ties:
            should_attach_glissando = _is_last_in_tie_chain(leaf)
        elif not allow_repeats and allow_ties:
            if _next_leaf_changes_current_pitch(leaf):
                should_attach_glissando = True
        elif not allow_repeats and not allow_ties:
            if _next_leaf_changes_current_pitch(leaf):
                if _is_last_in_tie_chain(leaf):
                    should_attach_glissando = True
        if hide_middle_note_heads:
            if leaf is not leaves[0]:
                should_attach_glissando = False
            if not left_broken and leaf is leaves[1]:
                strings = [
                    r"\hide NoteHead",
                    r"\override Accidental.stencil = ##f",
                    r"\override NoteColumn.glissando-skip = ##t",
                    r"\override NoteHead.no-ledgers = ##t",
                ]
                if hide_middle_stems:
                    strings.extend(
                        [
                            r"\override Dots.transparent = ##t",
                            r"\override Stem.transparent = ##t",
                        ]
                    )
                literal = LilyPondLiteral(strings)
                attach(literal, leaf, tag=tag)
            elif left_broken and leaf is leaves[0]:
                strings = [
                    r"\hide NoteHead",
                    r"\override Accidental.stencil = ##f",
                    r"\override NoteHead.no-ledgers = ##t",
                ]
                if hide_middle_stems:
                    strings.extend(
                        [
                            r"\override Dots.transparent = ##t",
                            r"\override Stem.transparent = ##t",
                        ]
                    )
                literal = LilyPondLiteral(strings)
                attach(
                    literal, leaf, tag=abjad_tags.HIDE_TO_JOIN_BROKEN_SPANNERS
                )
            elif left_broken and leaf is leaves[1]:
                string = r"\override NoteColumn.glissando-skip = ##t"
                literal = LilyPondLiteral(string)
                attach(
                    literal, leaf, tag=abjad_tags.HIDE_TO_JOIN_BROKEN_SPANNERS
                )
            if leaf is leaves[-1]:
                strings = [
                    r"\revert Accidental.stencil",
                    r"\revert NoteColumn.glissando-skip",
                    r"\revert NoteHead.no-ledgers",
                    r"\undo \hide NoteHead",
                ]
                if hide_middle_stems:
                    strings.extend(
                        [
                            r"\revert Dots.transparent",
                            r"\revert Stem.transparent",
                        ]
                    )
                if right_broken:
                    deactivate_glissando = True
                    literal = LilyPondLiteral(strings)
                    attach(
                        literal,
                        leaf,
                        deactivate=False,
                        tag=abjad_tags.HIDE_TO_JOIN_BROKEN_SPANNERS,
                    )
                    if right_broken_show_next:
                        literal = LilyPondLiteral(strings, format_slot="after")
                        attach(
                            literal,
                            leaf,
                            deactivate=True,
                            tag=abjad_tags.SHOW_TO_JOIN_BROKEN_SPANNERS,
                        )
                else:
                    literal = LilyPondLiteral(strings)
                    attach(literal, leaf, tag=tag)
        if should_attach_glissando:
            glissando = GlissandoIndicator(zero_padding=zero_padding)
            _apply_tweaks(glissando, tweaks, i=i, total=total)
            tag_ = tag
            if deactivate_glissando:
                tag_ = abjad_tags.SHOW_TO_JOIN_BROKEN_SPANNERS
            attach(glissando, leaf, deactivate=deactivate_glissando, tag=tag_)


def hairpin(
    descriptor: str,
    argument: typing.Union[Component, Selection],
    *,
    selector: typings.SelectorTyping = "abjad.select().leaves()",
    tag: str = None,
) -> None:
    r"""
    Attaches hairpin indicators.

    ..  container:: example

        With three-part string descriptor:

        >>> staff = abjad.Staff("c'4 d' e' f'")
        >>> abjad.hairpin('p < f', staff[:])
        >>> abjad.override(staff[0]).dynamic_line_spanner.staff_padding = 4
        >>> abjad.show(staff) # doctest: +SKIP

        ..  docs::

            >>> abjad.f(staff)
            \new Staff
            {
                \once \override DynamicLineSpanner.staff-padding = #4
                c'4
                \p
                \<
                d'4
                e'4
                f'4
                \f
            }

    ..  container:: example

        With two-part string descriptor:

        >>> staff = abjad.Staff("c'4 d' e' f'")
        >>> abjad.hairpin('< !', staff[:])
        >>> abjad.override(staff[0]).dynamic_line_spanner.staff_padding = 4
        >>> abjad.show(staff) # doctest: +SKIP

        ..  docs::

            >>> abjad.f(staff)
            \new Staff
            {
                \once \override DynamicLineSpanner.staff-padding = #4
                c'4
                \<
                d'4
                e'4
                f'4
                \!
            }

    ..  container:: example

        With dynamic objects:

        >>> staff = abjad.Staff("c'4 d' e' f'")
        >>> start_dynamic = abjad.Dynamic('niente', command=r'\!')
        >>> start_hairpin = abjad.StartHairpin('o<|')
        >>> abjad.tweak(start_hairpin).color = 'blue'
        >>> stop_dynamic = abjad.Dynamic('"f"')
        >>> abjad.hairpin([start_dynamic, start_hairpin, stop_dynamic], staff[:])
        >>> abjad.override(staff[0]).dynamic_line_spanner.staff_padding = 4
        >>> abjad.show(staff) # doctest: +SKIP

        ..  docs::

            >>> abjad.f(staff)
            \new Staff
            {
                \once \override DynamicLineSpanner.staff-padding = #4
                c'4
                \!
                - \tweak color #blue
                - \tweak circled-tip ##t
                - \tweak stencil #abjad-flared-hairpin
                \<
                d'4
                e'4
                f'4
                _ #(make-dynamic-script
                    (markup
                        #:whiteout
                        #:line (
                            #:general-align Y -2 #:normal-text #:larger "“"
                            #:hspace -0.4
                            #:dynamic "f"
                            #:hspace -0.2
                            #:general-align Y -2 #:normal-text #:larger "”"
                            )
                        )
                    )
            }

    """
    import abjad

    indicators: typing.List = []
    start_dynamic: typing.Optional[Dynamic]
    hairpin: typing.Optional[StartHairpin]
    stop_dynamic: typing.Optional[Dynamic]
    known_shapes = StartHairpin("<").known_shapes
    if isinstance(descriptor, str):
        for string in descriptor.split():
            if string in known_shapes:
                hairpin = StartHairpin(string)
                indicators.append(hairpin)
            elif string == "!":
                stop_hairpin = StopHairpin()
                indicators.append(stop_hairpin)
            else:
                dynamic = Dynamic(string)
                indicators.append(dynamic)
    else:
        assert isinstance(descriptor, list), repr(descriptor)
        indicators = descriptor

    start_dynamic, hairpin, stop_dynamic = None, None, None
    if len(indicators) == 1:
        if isinstance(indicators[0], Dynamic):
            start_dynamic = indicators[0]
        else:
            hairpin = indicators[0]
    elif len(indicators) == 2:
        if isinstance(indicators[0], Dynamic):
            start_dynamic = indicators[0]
            hairpin = indicators[1]
        else:
            hairpin = indicators[0]
            stop_dynamic = indicators[1]
    elif len(indicators) == 3:
        start_dynamic, hairpin, stop_dynamic = indicators
    else:
        raise Exception(indicators)

    if start_dynamic is not None:
        assert isinstance(start_dynamic, Dynamic), repr(start_dynamic)

    if isinstance(selector, str):
        selector = eval(selector)
    assert isinstance(selector, Expression)
    argument = selector(argument)
    leaves = select(argument).leaves()
    start_leaf = leaves[0]
    stop_leaf = leaves[-1]

    if start_dynamic is not None:
        attach(start_dynamic, start_leaf, tag=tag)
    if hairpin is not None:
        attach(hairpin, start_leaf, tag=tag)
    if stop_dynamic is not None:
        attach(stop_dynamic, stop_leaf, tag=tag)


def horizontal_bracket(
    argument: typing.Union[Component, Selection],
    *,
    selector: typings.SelectorTyping = "abjad.select().leaves()",
    start_group: StartGroup = None,
    stop_group: StopGroup = None,
    tag: str = None,
) -> None:
    r"""
    Attaches group indicators.

    ..  container:: example

        >>> staff = abjad.Staff("c'4 d' e' f'")
        >>> abjad.horizontal_bracket(staff[:])
        >>> abjad.show(staff) # doctest: +SKIP

        ..  docs::

            >>> abjad.f(staff)
            \new Staff
            {
                c'4
                \startGroup
                d'4
                e'4
                f'4
                \stopGroup
            }

    """
    # import allows eval statement
    import abjad

    start_group = start_group or StartGroup()
    stop_group = stop_group or StopGroup()
    if isinstance(selector, str):
        selector = eval(selector)
    assert isinstance(selector, Expression)
    argument = selector(argument)
    leaves = select(argument).leaves()
    start_leaf = leaves[0]
    stop_leaf = leaves[-1]
    attach(start_group, start_leaf, tag=tag)
    attach(stop_group, stop_leaf, tag=tag)


def ottava(
    argument: typing.Union[Component, Selection],
    *,
    selector: typings.SelectorTyping = "abjad.select().leaves()",
    start_ottava: Ottava = Ottava(n=1),
    stop_ottava: Ottava = Ottava(n=0, format_slot="after"),
    tag: str = None,
) -> None:
    r"""
    Attaches ottava indicators.

    ..  container:: example

        >>> staff = abjad.Staff("c'4 d' e' f'")
        >>> abjad.ottava(staff[:])
        >>> abjad.show(staff) # doctest: +SKIP

        ..  docs::

            >>> abjad.f(staff)
            \new Staff
            {
                \ottava 1
                c'4
                d'4
                e'4
                f'4
                \ottava 0
            }

    """
    # import allows eval statement
    import abjad

    assert isinstance(start_ottava, Ottava), repr(start_ottava)
    assert isinstance(stop_ottava, Ottava), repr(stop_ottava)
    if isinstance(selector, str):
        selector = eval(selector)
    assert isinstance(selector, Expression)
    argument = selector(argument)
    leaves = select(argument).leaves()
    start_leaf = leaves[0]
    stop_leaf = leaves[-1]
    attach(start_ottava, start_leaf, tag=tag)
    attach(stop_ottava, stop_leaf, tag=tag)


def phrasing_slur(
    argument: typing.Union[Component, Selection],
    *,
    selector: typings.SelectorTyping = "abjad.select().leaves()",
    start_phrasing_slur: StartPhrasingSlur = None,
    stop_phrasing_slur: StopPhrasingSlur = None,
    tag: str = None,
) -> None:
    r"""
    Attaches phrasing slur indicators.

    ..  container:: example

        >>> staff = abjad.Staff("c'4 d' e' f'")
        >>> abjad.phrasing_slur(staff[:])
        >>> abjad.show(staff) # doctest: +SKIP

        ..  docs::

            >>> abjad.f(staff)
            \new Staff
            {
                c'4
                \(
                d'4
                e'4
                f'4
                \)
            }


    """
    # import allows eval statement
    import abjad

    start_phrasing_slur = StartPhrasingSlur()
    stop_phrasing_slur = StopPhrasingSlur()
    if isinstance(selector, str):
        selector = eval(selector)
    assert isinstance(selector, Expression)
    argument = selector(argument)
    leaves = select(argument).leaves()
    start_leaf = leaves[0]
    stop_leaf = leaves[-1]
    start_phrasing_slur = start_phrasing_slur or StartPhrasingSlur()
    stop_phrasing_slur = stop_phrasing_slur or StopPhrasingSlur()
    attach(start_phrasing_slur, start_leaf, tag=tag)
    attach(stop_phrasing_slur, stop_leaf, tag=tag)


def piano_pedal(
    argument: typing.Union[Component, Selection],
    *,
    selector: typings.SelectorTyping = "abjad.select().leaves()",
    start_piano_pedal: StartPianoPedal = None,
    stop_piano_pedal: StopPianoPedal = None,
    tag: str = None,
) -> None:
    r"""
    Attaches piano pedal indicators.

    ..  container:: example

        >>> staff = abjad.Staff("c'4 d' e' f'")
        >>> abjad.piano_pedal(staff[:])
        >>> abjad.setting(staff).pedal_sustain_style = "#'mixed"
        >>> abjad.override(staff).sustain_pedal_line_spanner.staff_padding = 5
        >>> abjad.show(staff) # doctest: +SKIP

        ..  docs::

            >>> abjad.f(staff)
            \new Staff
            \with
            {
                \override SustainPedalLineSpanner.staff-padding = #5
                pedalSustainStyle = #'mixed
            }
            {
                c'4
                \sustainOn
                d'4
                e'4
                f'4
                \sustainOff
            }

    """
    # import allows eval statement
    import abjad

    start_piano_pedal = start_piano_pedal or StartPianoPedal()
    stop_piano_pedal = stop_piano_pedal or StopPianoPedal()
    if isinstance(selector, str):
        selector = eval(selector)
    assert isinstance(selector, Expression)
    argument = selector(argument)
    leaves = select(argument).leaves()
    start_leaf = leaves[0]
    stop_leaf = leaves[-1]
    attach(start_piano_pedal, start_leaf, tag=tag)
    attach(stop_piano_pedal, stop_leaf, tag=tag)


def slur(
    argument: typing.Union[Component, Selection],
    *,
    selector: typings.SelectorTyping = "abjad.select().leaves()",
    start_slur: StartSlur = None,
    stop_slur: StopSlur = None,
    tag: str = None,
) -> None:
    r"""
    Attaches slur indicators.

    ..  container:: example

        >>> staff = abjad.Staff("c'4 d' e' f'")
        >>> abjad.slur(staff[:])
        >>> abjad.show(staff) # doctest: +SKIP

        ..  docs::

            >>> abjad.f(staff)
            \new Staff
            {
                c'4
                (
                d'4
                e'4
                f'4
                )
            }


    """
    # import allows eval statement
    import abjad

    start_slur = start_slur or StartSlur()
    stop_slur = stop_slur or StopSlur()
    if isinstance(selector, str):
        selector = eval(selector)
    assert isinstance(selector, Expression)
    argument = selector(argument)
    leaves = select(argument).leaves()
    start_leaf = leaves[0]
    stop_leaf = leaves[-1]
    attach(start_slur, start_leaf, tag=tag)
    attach(stop_slur, stop_leaf, tag=tag)


def text_spanner(
    argument: typing.Union[Component, Selection],
    *,
    selector: typings.SelectorTyping = "abjad.select().leaves()",
    start_text_span: StartTextSpan = None,
    stop_text_span: StopTextSpan = None,
    tag: str = None,
) -> None:
    r"""
    Attaches text span indicators.

    ..  container:: example

        Single spanner:

        >>> staff = abjad.Staff("c'4 d' e' f'")
        >>> start_text_span = abjad.StartTextSpan(
        ...     left_text=abjad.Markup('pont.').upright(),
        ...     right_text=abjad.Markup('tasto').upright(),
        ...     style='solid-line-with-arrow',
        ...     )
        >>> abjad.text_spanner(staff[:], start_text_span=start_text_span)
        >>> abjad.override(staff[0]).text_spanner.staff_padding = 4
        >>> abjad.show(staff) # doctest: +SKIP

        ..  docs::

            >>> abjad.f(staff)
            \new Staff
            {
                \once \override TextSpanner.staff-padding = #4
                c'4
                - \abjad-solid-line-with-arrow
                - \tweak bound-details.left.text \markup {
                    \concat
                        {
                            \upright
                                pont.
                            \hspace
                                #0.5
                        }
                    }
                - \tweak bound-details.right.text \markup {
                    \upright
                        tasto
                    }
                \startTextSpan
                d'4
                e'4
                f'4
                \stopTextSpan
            }

    ..  container:: example

        Enchained spanners:

        >>> staff = abjad.Staff("c'4 d' e' f' r")
        >>> start_text_span = abjad.StartTextSpan(
        ...     left_text=abjad.Markup('pont.').upright(),
        ...     style='dashed-line-with-arrow',
        ...     )
        >>> abjad.text_spanner(staff[:3], start_text_span=start_text_span)
        >>> start_text_span = abjad.StartTextSpan(
        ...     left_text=abjad.Markup('tasto').upright(),
        ...     right_text=abjad.Markup('pont.').upright(),
        ...     style='dashed-line-with-arrow',
        ...     )
        >>> abjad.text_spanner(staff[-3:], start_text_span=start_text_span)
        >>> abjad.override(staff).text_spanner.staff_padding = 4
        >>> abjad.show(staff) # doctest: +SKIP

        ..  docs::

            >>> abjad.f(staff)
            \new Staff
            \with
            {
                \override TextSpanner.staff-padding = #4
            }
            {
                c'4
                - \abjad-dashed-line-with-arrow
                - \tweak bound-details.left.text \markup {
                    \concat
                        {
                            \upright
                                pont.
                            \hspace
                                #0.5
                        }
                    }
                \startTextSpan
                d'4
                e'4
                \stopTextSpan
                - \abjad-dashed-line-with-arrow
                - \tweak bound-details.left.text \markup {
                    \concat
                        {
                            \upright
                                tasto
                            \hspace
                                #0.5
                        }
                    }
                - \tweak bound-details.right.text \markup {
                    \upright
                        pont.
                    }
                \startTextSpan
                f'4
                r4
                \stopTextSpan
            }

        >>> staff = abjad.Staff("c'4 d' e' f' r")
        >>> start_text_span = abjad.StartTextSpan(
        ...     left_text=abjad.Markup('pont.').upright(),
        ...     style='dashed-line-with-arrow',
        ...     )
        >>> abjad.text_spanner(staff[:3], start_text_span=start_text_span)
        >>> start_text_span = abjad.StartTextSpan(
        ...     left_text=abjad.Markup('tasto').upright(),
        ...     style='solid-line-with-hook',
        ...     )
        >>> abjad.text_spanner(staff[-3:], start_text_span=start_text_span)
        >>> abjad.override(staff).text_spanner.staff_padding = 4
        >>> abjad.show(staff) # doctest: +SKIP

        ..  docs::

            >>> abjad.f(staff)
            \new Staff
            \with
            {
                \override TextSpanner.staff-padding = #4
            }
            {
                c'4
                - \abjad-dashed-line-with-arrow
                - \tweak bound-details.left.text \markup {
                    \concat
                        {
                            \upright
                                pont.
                            \hspace
                                #0.5
                        }
                    }
                \startTextSpan
                d'4
                e'4
                \stopTextSpan
                - \abjad-solid-line-with-hook
                - \tweak bound-details.left.text \markup {
                    \concat
                        {
                            \upright
                                tasto
                            \hspace
                                #0.5
                        }
                    }
                \startTextSpan
                f'4
                r4
                \stopTextSpan
            }

    """
    import abjad

    start_text_span = start_text_span or StartTextSpan()
    stop_text_span = stop_text_span or StopTextSpan()
    if isinstance(selector, str):
        selector = eval(selector)
    assert isinstance(selector, Expression)
    argument = selector(argument)
    leaves = select(argument).leaves()
    start_leaf = leaves[0]
    stop_leaf = leaves[-1]
    attach(start_text_span, start_leaf, tag=tag)
    attach(stop_text_span, stop_leaf, tag=tag)


def tie(
    argument: typing.Union[Component, Selection],
    *,
    direction: enums.VerticalAlignment = None,
    repeat: typing.Union[bool, typings.IntegerPair, DurationInequality] = None,
    selector: typings.SelectorTyping = "abjad.select().leaves()",
    # tie: Tie = None,
    tag: str = None,
) -> None:
    r"""
    Attaches tie indicators.

    ..  container:: example

        >>> staff = abjad.Staff("c'4 c' c' c'")
        >>> abjad.tie(staff[:])
        >>> abjad.show(staff) # doctest: +SKIP

        ..  docs::

            >>> abjad.f(staff)
            \new Staff
            {
                c'4
                ~
                c'4
                ~
                c'4
                ~
                c'4
            }

    ..  container:: example

        With repeat ties:

        >>> staff = abjad.Staff("c'4 c' c' c'")
        >>> abjad.tie(staff[:], repeat=True)
        >>> abjad.show(staff) # doctest: +SKIP

        ..  docs::

            >>> abjad.f(staff)
            \new Staff
            {
                c'4
                c'4
                \repeatTie
                c'4
                \repeatTie
                c'4
                \repeatTie
            }

    ..  container:: example

        Removes any existing ties before attaching new tie:

        >>> staff = abjad.Staff("c'4 ~ c' ~ c' ~ c'")
        >>> abjad.tie(staff[:])
        >>> abjad.show(staff) # doctest: +SKIP

        ..  docs::

            >>> abjad.f(staff)
            \new Staff
            {
                c'4
                ~
                c'4
                ~
                c'4
                ~
                c'4
            }

    ..  container:: example

        Ties consecutive chords if all adjacent pairs have at least one pitch
        in common:

        >>> staff = abjad.Staff("<c'>4 <c' d'>4 <d'>4")
        >>> abjad.tie(staff[:])
        >>> abjad.show(staff) # doctest: +SKIP

        ..  docs::

            >>> abjad.f(staff)
            \new Staff
            {
                <c'>4
                ~
                <c' d'>4
                ~
                <d'>4
            }

    ..  container:: example

        Enharmonics are allowed:

        >>> staff = abjad.Staff("c'4 bs c' dff'")
        >>> abjad.tie(staff[:])
        >>> abjad.show(staff) # doctest: +SKIP

        ..  docs::

            >>> abjad.f(staff)
            \new Staff
            {
                c'4
                ~
                bs4
                ~
                c'4
                ~
                dff'4
            }

    ..  container:: example

        Repeat tie threshold works like this:

        >>> staff = abjad.Staff("d'4. d'2 d'4. d'2")
        >>> abjad.tie(staff[:], repeat=(4, 8))
        >>> abjad.show(staff) # doctest: +SKIP

        ..  docs::

            >>> abjad.f(staff)
            \new Staff
            {
                d'4.
                ~
                d'2
                d'4.
                \repeatTie
                ~
                d'2
            }

    ..  container:: example

        Detaches ties before attach:

        >>> staff = abjad.Staff("d'2 ~ d'8 ~ d'8 ~ d'8 ~ d'8")
        >>> abjad.show(staff) # doctest: +SKIP

        ..  docs::

            >>> abjad.f(staff)
            \new Staff
            {
                d'2
                ~
                d'8
                ~
                d'8
                ~
                d'8
                ~
                d'8
            }

        >>> abjad.tie(staff[:], repeat=(4, 8))
        >>> abjad.show(staff) # doctest: +SKIP

        ..  docs::

            >>> abjad.f(staff)
            \new Staff
            {
                d'2
                d'8
                \repeatTie
                ~
                d'8
                ~
                d'8
                ~
                d'8
            }

    """
    # import allows eval statement
    import abjad

    if repeat in (None, False):
        inequality = DurationInequality("<", 0)
    elif repeat is True:
        inequality = DurationInequality(">=", 0)
    elif isinstance(repeat, DurationInequality):
        inequality = repeat
    else:
        assert isinstance(repeat, tuple) and len(repeat) == 2, repr(repeat)
        inequality = DurationInequality(">=", repeat)
    assert isinstance(inequality, DurationInequality), repr(inequality)
    if isinstance(selector, str):
        selector = eval(selector)
    assert isinstance(selector, Expression)
    argument = selector(argument)
    leaves = select(argument).leaves()
    if len(leaves) < 2:
        raise Exception("must be two or more notes (not {leaves!r}).")
    for leaf in leaves:
        if not isinstance(leaf, (Note, Chord)):
            raise Exception(r"tie note or chord (not {leaf!r}).")
    for current_leaf, next_leaf in Sequence(leaves).nwise():
        duration = inspect(current_leaf).duration()
        if inequality(duration):
            detach(Tie, current_leaf)
            detach(RepeatTie, next_leaf)
            repeat_tie = RepeatTie(direction=direction)
            attach(repeat_tie, next_leaf, tag=tag)
        else:
            detach(Tie, current_leaf)
            detach(RepeatTie, next_leaf)
            tie = Tie(direction=direction)
            attach(tie, current_leaf, tag=tag)


def trill_spanner(
    argument: typing.Union[Component, Selection],
    *,
    selector: typings.SelectorTyping = "abjad.select().leaves()",
    start_trill_span: StartTrillSpan = None,
    stop_trill_span: StopTrillSpan = None,
    tag: str = None,
) -> None:
    r"""
    Attaches trill spanner indicators.

    ..  container:: example

        >>> staff = abjad.Staff("c'4 d' e' f'")
        >>> abjad.trill_spanner(staff[:])
        >>> abjad.show(staff) # doctest: +SKIP

        ..  docs::

            >>> abjad.f(staff)
            \new Staff
            {
                c'4
                \startTrillSpan
                d'4
                e'4
                f'4
                \stopTrillSpan
            }

    """
    # import allows eval statement
    import abjad

    start_trill_span = start_trill_span or StartTrillSpan()
    stop_trill_span = stop_trill_span or StopTrillSpan()
    if isinstance(selector, str):
        selector = eval(selector)
    assert isinstance(selector, Expression)
    argument = selector(argument)
    leaves = select(argument).leaves()
    start_leaf = leaves[0]
    stop_leaf = leaves[-1]
    attach(start_trill_span, start_leaf, tag=tag)
    attach(stop_trill_span, stop_leaf, tag=tag)
