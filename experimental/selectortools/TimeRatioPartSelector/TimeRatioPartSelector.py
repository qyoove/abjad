from abjad.tools import durationtools
from abjad.tools import mathtools
from experimental.selectortools.RatioPartSelector import RatioPartSelector


class TimeRatioPartSelector(RatioPartSelector):
    r'''.. versionadded:: 1.0

    Partition `reference` by ratio of durations. Then select exactly one part.

        >>> from experimental import *

    Select all background measures starting during segment ``'red'`` in ``'Voice 1'``.
    Then partition these measures ``1:1`` by their duration.
    Then select part ``0`` of this partition::

        >>> segment_selector = selectortools.SegmentItemSelector(identifier='red')
        >>> inequality = timespantools.expr_starts_during_timespan(timespan=segment_selector.timespan)
        >>> background_measure_selector = selectortools.BackgroundMeasureSliceSelector(inequality=inequality)

    ::

        >>> time_ratio_part_selector = selectortools.TimeRatioPartSelector(
        ... background_measure_selector, (1, 1), 0)

    ::

        >>> z(time_ratio_part_selector)
        selectortools.TimeRatioPartSelector(
            selectortools.BackgroundMeasureSliceSelector(
                inequality=timespantools.TimespanInequality(
                    timespantools.TimespanInequalityTemplate('t.start <= expr.start < t.stop'),
                    timespantools.SingleSourceTimespan(
                        selector=selectortools.SegmentItemSelector(
                            identifier='red'
                            )
                        )
                    )
                ),
            mathtools.Ratio(1, 1),
            0
            )

    All duration ratio item selector properties are read-only.
    '''

    ### INITIALIZER ###

    def __init__(self, reference, ratio, part):
        RatioPartSelector.__init__(self, reference, ratio, part)

    ### PUBLIC METHODS ###

    def get_duration(self, score_specification):
        reference_duration = self.reference.get_duration(score_specification)
        parts = mathtools.divide_number_by_ratio(reference_duration, self.ratio)
        part = parts[self.part]
        return part

    def get_segment_start_offset(self, score_specification):
        reference_duration = self.reference.get_duration(score_specification)
        parts = mathtools.divide_number_by_ratio(reference_duration, self.ratio)
        parts_before = parts[:self.part]
        duration_before = sum(parts_before)
        return durationtools.Offset(duration_before) 

    def get_segment_stop_offset(self, score_specification):
        reference_duration = self.reference.get_duration(score_specification)
        parts = mathtools.divide_number_by_ratio(reference_duration, self.ratio)
        part = parts[self.part]
        duration = part
        parts_before = parts[:self.part]
        duration_before = sum(parts_before)
        stop_offset = duration_before + duration
        return durationtools.Offset(stop_offset)
