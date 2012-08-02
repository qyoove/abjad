from experimental.selectortools.BackgroundElementSliceSelector import BackgroundElementSliceSelector


class BackgroundMeasureSliceSelector(BackgroundElementSliceSelector):
    r'''.. versionadded:: 1.0

    Select all measures in score::

        >>> from experimental import *

    ::

        >>> selectortools.BackgroundMeasureSliceSelector()
        BackgroundMeasureSliceSelector()

    Select measures from ``3`` forward::

        >>> selectortools.BackgroundMeasureSliceSelector(start=3)
        BackgroundMeasureSliceSelector(start=3)

    Select measures up to but not including ``6``::

        >>> selectortools.BackgroundMeasureSliceSelector(stop=6)
        BackgroundMeasureSliceSelector(stop=6)

    Select measures from ``3`` up to but not including ``6``::

        >>> selectortools.BackgroundMeasureSliceSelector(start=3, stop=6)
        BackgroundMeasureSliceSelector(start=3, stop=6)

    Select all measures starting during segment ``'red'``::

        >>> timespan = selectortools.SegmentItemSelector(index='red')
        >>> inequality = timespantools.expr_starts_during_timespan(timespan=timespan)

    ::

        >>> selector = selectortools.BackgroundMeasureSliceSelector(inequality=inequality)

    ::

        >>> z(selector)
        selectortools.BackgroundMeasureSliceSelector(
            inequality=timespantools.TimespanInequality(
                timespantools.TimespanInequalityTemplate('t.start <= expr.start < t.stop'),
                timespantools.SingleSourceTimespan(
                    selector=selectortools.SegmentItemSelector(
                        index='red'
                        )
                    )
                )
            )

    Select the last two measures during segment ``'red'``::

        >>> selector = selectortools.BackgroundMeasureSliceSelector(inequality=inequality, start=-2)

    ::
    
        >>> z(selector)
        selectortools.BackgroundMeasureSliceSelector(
            inequality=timespantools.TimespanInequality(
                timespantools.TimespanInequalityTemplate('t.start <= expr.start < t.stop'),
                timespantools.SingleSourceTimespan(
                    selector=selectortools.SegmentItemSelector(
                        index='red'
                        )
                    )
                ),
            start=-2
            )

    Select all the measures that start during the three contiguous segments starting with ``'red'``::

        >>> expr = helpertools.SegmentIndexExpression("'red' + 3")
        >>> selector = selectortools.SegmentSliceSelector(start='red', stop=expr)
        >>> inequality = timespantools.expr_starts_during_timespan(timespan=selector)

    ::
    
        >>> selector = selectortools.BackgroundMeasureSliceSelector(inequality=inequality)

    ::

        >>> z(selector)
        selectortools.BackgroundMeasureSliceSelector(
            inequality=timespantools.TimespanInequality(
                timespantools.TimespanInequalityTemplate('t.start <= expr.start < t.stop'),
                timespantools.SingleSourceTimespan(
                    selector=selectortools.SegmentSliceSelector(
                        start='red',
                        stop=helpertools.SegmentIndexExpression("'red' + 3")
                        )
                    )
                )
            )

    Select the last two measures that start during the three contiguous segments starting with ``'red'``::

        >>> selector = selectortools.BackgroundMeasureSliceSelector(inequality=inequality, start=-2)

    ::

        >>> z(selector)
        selectortools.BackgroundMeasureSliceSelector(
            inequality=timespantools.TimespanInequality(
                timespantools.TimespanInequalityTemplate('t.start <= expr.start < t.stop'),
                timespantools.SingleSourceTimespan(
                    selector=selectortools.SegmentSliceSelector(
                        start='red',
                        stop=helpertools.SegmentIndexExpression("'red' + 3")
                        )
                    )
                ),
            start=-2
            )

    Measure slice selectors are immutable.
    '''

    ### INITIALIZER ###

    def __init__(self, inequality=None, start=None, stop=None):
        from abjad.tools import measuretools
        BackgroundElementSliceSelector.__init__(self, measuretools.Measure,
            inequality=inequality, start=start, stop=stop)

    ### READ-ONLY PUBLIC PROPERTIES ###

    @property
    def context_name(self):
        '''Return none.
        '''
        return

    @property
    def context_names(self):
        '''Return empty list.
        '''
        return []
