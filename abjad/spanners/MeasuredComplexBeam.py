import typing
from abjad.enumerations import HorizontalAlignment, VerticalAlignment
from abjad.core.Measure import Measure
from abjad.top.inspect import inspect
from .ComplexBeam import ComplexBeam


class MeasuredComplexBeam(ComplexBeam):
    r"""
    Measured complex beam.

    ..  container:: example

        >>> staff = abjad.Staff()
        >>> staff.append(abjad.Measure((2, 16), "c'16 d'16"))
        >>> staff.append(abjad.Measure((2, 16), "e'16 f'16"))
        >>> abjad.setting(staff).auto_beaming = False
        >>> abjad.show(staff) # doctest: +SKIP

        >>> beam = abjad.MeasuredComplexBeam()
        >>> selector = abjad.select().leaves()
        >>> leaves = selector(staff)
        >>> abjad.attach(beam, leaves)
        >>> abjad.show(staff) # doctest: +SKIP

        ..  docs::

            >>> abjad.f(staff)
            \new Staff
            \with
            {
                autoBeaming = ##f
            }
            {
                {   % measure
                    \time 2/16
                    \set stemLeftBeamCount = 0
                    \set stemRightBeamCount = 2
                    c'16
                    [
                    \set stemLeftBeamCount = 2
                    \set stemRightBeamCount = 1
                    d'16
                }   % measure
                {   % measure
                    \set stemLeftBeamCount = 1
                    \set stemRightBeamCount = 2
                    e'16
                    \set stemLeftBeamCount = 2
                    \set stemRightBeamCount = 0
                    f'16
                    ]
                }   % measure
            }

    Beams leaves in spanner explicitly.

    Groups leaves by measures.

    Formats top-level ``span_beam_count`` beam between measures.
    """

    ### CLASS VARIABLES ###

    __slots__ = (
        '_span_beam_count',
        )

    ### INITIALIZER ###

    def __init__(
        self,
        *,
        direction: VerticalAlignment = None,
        isolated_nib_direction: typing.Union[bool, HorizontalAlignment] = False,
        span_beam_count: int = 1,
        ) -> None:
        ComplexBeam.__init__(
            self,
            direction=direction,
            isolated_nib_direction=isolated_nib_direction,
            )
        if span_beam_count is not None:
            assert isinstance(span_beam_count, int)
        self._span_beam_count = span_beam_count

    ### PRIVATE METHODS ###

    def _add_beam_counts(self, leaf, bundle):
        left, right = None, None
        #if leaf.beam.beamable:
        if self._is_beamable(leaf):
            if self._is_exterior_leaf(leaf):
                left, right = self._get_left_right_for_exterior_leaf(leaf)
            elif inspect(leaf).get_parentage(
                include_self=False).get_first(Measure) is not None:
                measure = inspect(leaf).get_parentage(
                    include_self=False).get_first(Measure)
                # leaf at beginning of measure
                if measure._is_one_of_my_first_leaves(leaf):
                    assert isinstance(self.span_beam_count, int)
                    left = self.span_beam_count
                    right = leaf.written_duration.flag_count
                # leaf at end of measure
                elif measure._is_one_of_my_last_leaves(leaf):
                    assert isinstance(self.span_beam_count, int)
                    left = leaf.written_duration.flag_count
                    right = self.span_beam_count
            else:
                left, right = self._get_left_right_for_interior_leaf(leaf)
            if left is not None:
                string = rf'\set stemLeftBeamCount = {left}'
                bundle.before.commands.append(string)
            if right is not None:
                string = rf'\set stemRightBeamCount = {right}'
                bundle.before.commands.append(string)

    def _copy_keywords(self, new):
        ComplexBeam._copy_keywords(self, new)
        new._span_beam_count = self.span_beam_count

    ### PUBLIC PROPERTIES ###

    @property
    def span_beam_count(self) -> int:
        r"""
        Gets number of span beams between adjacent measures.

        ..  container:: example

            Use one span beam between measures:

            >>> staff = abjad.Staff()
            >>> staff.append(abjad.Measure((2, 32), "c'32 d'32"))
            >>> staff.append(abjad.Measure((2, 32), "e'32 f'32"))
            >>> selector = abjad.select().leaves()
            >>> leaves = selector(staff)
            >>> beam = abjad.MeasuredComplexBeam(span_beam_count=1)
            >>> abjad.attach(beam, leaves)
            >>> abjad.show(staff) # doctest: +SKIP

            >>> beam.span_beam_count
            1

        ..  container:: example

            Use two span beams between measures:

            >>> staff = abjad.Staff()
            >>> staff.append(abjad.Measure((2, 32), "c'32 d'32"))
            >>> staff.append(abjad.Measure((2, 32), "e'32 f'32"))
            >>> beam = abjad.MeasuredComplexBeam(span_beam_count=2)
            >>> selector = abjad.select().leaves()
            >>> leaves = selector(staff)
            >>> abjad.attach(beam, leaves)
            >>> abjad.show(staff) # doctest: +SKIP

            >>> beam.span_beam_count
            2

        """
        return self._span_beam_count

    ### PUBLIC METHODS ###

    def start_command(self) -> typing.List[str]:
        """
        Gets start command.

        ..  container:: example

            >>> abjad.MeasuredComplexBeam().start_command()
            ['[']

        """
        return super(MeasuredComplexBeam, self).start_command()

    def stop_command(self) -> typing.Optional[str]:
        """
        Gets stop command.

        ..  container:: example

            >>> abjad.MeasuredComplexBeam().stop_command()
            ']'

        """
        return super(MeasuredComplexBeam, self).stop_command()
