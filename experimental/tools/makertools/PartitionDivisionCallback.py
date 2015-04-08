# -*- encoding: utf-8 -*-
from abjad.tools.abctools import AbjadValueObject
from abjad.tools import sequencetools


class PartitionDivisionCallback(AbjadValueObject):
    r'''Beat grouper.

    ..  container:: example

        Beat lists for examples:

        ::

            >>> beat_maker = makertools.SplitByBeatsDivisionCallback(
            ...     compound_beat_duration=Duration(3, 8),
            ...     simple_beat_duration=Duration(1, 4),
            ...     )
            >>> meters = [
            ...     metertools.Meter((4, 4)),
            ...     metertools.Meter((5, 4)),
            ...     metertools.Meter((6, 4)),
            ...     metertools.Meter((7, 4)),
            ...     ]
            >>> beat_lists = beat_maker(meters)
            >>> for beat_list in beat_lists:
            ...     beat_list
            [Duration(1, 4), Duration(1, 4), Duration(1, 4), Duration(1, 4)]
            [Duration(1, 4), Duration(1, 4), Duration(1, 4), Duration(1, 4), Duration(1, 4)]
            [Duration(3, 8), Duration(3, 8), Duration(3, 8), Duration(3, 8)]
            [Duration(1, 4), Duration(1, 4), Duration(1, 4), Duration(1, 4), Duration(1, 4), Duration(1, 4), Duration(1, 4)]

    ..  container:: example

        **Example 1a.** Beat lists grouped in pairs. Remainder at right:

        ::

            >>> grouper = makertools.PartitionDivisionCallback(
            ...     counts=[2],
            ...     fuse_remainder=False,
            ...     remainder_direction=Right,
            ...     )
            >>> grouped_beat_lists = grouper(beat_lists)
            >>> for grouped_beat_list in grouped_beat_lists:
            ...     grouped_beat_list
            [[Duration(1, 4), Duration(1, 4)], [Duration(1, 4), Duration(1, 4)]]
            [[Duration(1, 4), Duration(1, 4)], [Duration(1, 4), Duration(1, 4)], [Duration(1, 4)]]
            [[Duration(3, 8), Duration(3, 8)], [Duration(3, 8), Duration(3, 8)]]
            [[Duration(1, 4), Duration(1, 4)], [Duration(1, 4), Duration(1, 4)], [Duration(1, 4), Duration(1, 4)], [Duration(1, 4)]]

        **Example 1b.** Beat lists grouped in pairs. Remainder fused at right:

        ::

            >>> grouper = makertools.PartitionDivisionCallback(
            ...     counts=[2],
            ...     fuse_remainder=True,
            ...     remainder_direction=Right,
            ...     )
            >>> grouped_beat_lists = grouper(beat_lists)
            >>> for grouped_beat_list in grouped_beat_lists:
            ...     grouped_beat_list
            [[Duration(1, 4), Duration(1, 4)], [Duration(1, 4), Duration(1, 4)]]
            [[Duration(1, 4), Duration(1, 4)], [Duration(1, 4), Duration(1, 4), Duration(1, 4)]]
            [[Duration(3, 8), Duration(3, 8)], [Duration(3, 8), Duration(3, 8)]]
            [[Duration(1, 4), Duration(1, 4)], [Duration(1, 4), Duration(1, 4)], [Duration(1, 4), Duration(1, 4), Duration(1, 4)]]

    ..  container:: example

        **Example 2a.** Beat lists grouped in pairs. Remainder at left:

        ::

            >>> grouper = makertools.PartitionDivisionCallback(
            ...     counts=[2],
            ...     fuse_remainder=False,
            ...     remainder_direction=Left,
            ...     )
            >>> grouped_beat_lists = grouper(beat_lists)
            >>> for grouped_beat_list in grouped_beat_lists:
            ...     grouped_beat_list
            [[Duration(1, 4), Duration(1, 4)], [Duration(1, 4), Duration(1, 4)]]
            [[Duration(1, 4)], [Duration(1, 4), Duration(1, 4)], [Duration(1, 4), Duration(1, 4)]]
            [[Duration(3, 8), Duration(3, 8)], [Duration(3, 8), Duration(3, 8)]]
            [[Duration(1, 4)], [Duration(1, 4), Duration(1, 4)], [Duration(1, 4), Duration(1, 4)], [Duration(1, 4), Duration(1, 4)]]

        **Example 1b.** Beat lists grouped in pairs. Remainder fused at left:

        ::

            >>> grouper = makertools.PartitionDivisionCallback(
            ...     counts=[2],
            ...     fuse_remainder=True,
            ...     remainder_direction=Left,
            ...     )
            >>> grouped_beat_lists = grouper(beat_lists)
            >>> for grouped_beat_list in grouped_beat_lists:
            ...     grouped_beat_list
            [[Duration(1, 4), Duration(1, 4)], [Duration(1, 4), Duration(1, 4)]]
            [[Duration(1, 4), Duration(1, 4), Duration(1, 4)], [Duration(1, 4), Duration(1, 4)]]
            [[Duration(3, 8), Duration(3, 8)], [Duration(3, 8), Duration(3, 8)]]
            [[Duration(1, 4), Duration(1, 4), Duration(1, 4)], [Duration(1, 4), Duration(1, 4)], [Duration(1, 4), Duration(1, 4)]]

    Groups beats into conductors' groups.
    '''

    ### CLASS VARIABLES ###

    __slots__ = (
        '_counts',
        '_fuse_assignable_total_duration',
        '_fuse_remainder',
        '_remainder_direction',
        )

    ### INITIALIZER ###

    def __init__(
        self,
        counts=None,
        fuse_assignable_total_duration=False,
        fuse_remainder=False,
        remainder_direction=Right,
        ):
        self._counts = counts
        self._fuse_assignable_total_duration = fuse_assignable_total_duration
        self._fuse_remainder = fuse_remainder
        self._remainder_direction = remainder_direction

    ### SPECIAL METHODS ###

    def __call__(self, beat_lists):
        r'''Calls beat grouper on `beat_lists`.

        ..  container:: example

            **Example 1.** Groups beat list elements into pairs:

            ::

                >>> grouper = makertools.PartitionDivisionCallback(
                ...     counts=[2],
                ...     )
                >>> beat_list = 6 * [Duration(1, 4)]
                >>> grouped_beat_lists = grouper([beat_list])
                >>> grouped_beat_lists[0]
                [[Duration(1, 4), Duration(1, 4)], [Duration(1, 4), Duration(1, 4)], [Duration(1, 4), Duration(1, 4)]]
                >>> [len(beat_group) for beat_group in _]
                [2, 2, 2]

        ..  container:: example

            **Example 2.** Groups beat list elements into groups of three:

            ::

                >>> grouper = makertools.PartitionDivisionCallback(
                ...     counts=[3],
                ...     )
                >>> beat_list = 6 * [Duration(1, 4)]
                >>> grouped_beat_lists = grouper([beat_list])
                >>> grouped_beat_lists[0]
                [[Duration(1, 4), Duration(1, 4), Duration(1, 4)], [Duration(1, 4), Duration(1, 4), Duration(1, 4)]]
                >>> [len(beat_group) for beat_group in _]
                [3, 3]

        Returns list of beat lists.
        '''
        grouped_beat_lists = []
        for beat_list in beat_lists:
            grouped_beat_list = self._beat_list_to_grouped_beat_list(beat_list)
            grouped_beat_lists.append(grouped_beat_list)
        return grouped_beat_lists

    def _beat_list_to_grouped_beat_list(self, beat_list):
        assert isinstance(beat_list, (list, tuple)), repr(beat_list)
        total_duration = sum(beat_list)
        if (total_duration.is_assignable and 
            self.fuse_assignable_total_duration):
            return [[total_duration]]
        if self.counts is None:
            beat_group = list(beat_list)
            grouped_beat_list = [beat_group]
            return grouped_beat_list
        grouped_beat_list = sequencetools.partition_sequence_by_counts(
            beat_list,
            counts=self.counts,
            cyclic=True,
            overhang=False,
            )
        beats_included = sum([len(_) for _ in grouped_beat_list])
        if beats_included == len(beat_list):
            return grouped_beat_list
        remainder_length = len(beat_list) - beats_included
        if self.remainder_direction == Left:
            grouped_beat_list = sequencetools.partition_sequence_by_counts(
                beat_list[remainder_length:],
                counts=self.counts,
                cyclic=True,
                overhang=False
                )
            remainder = beat_list[:remainder_length]
            if self.fuse_remainder:
                grouped_beat_list[0] = remainder + grouped_beat_list[0]
            else:
                grouped_beat_list.insert(0, remainder)
        else:
            grouped_beat_list = sequencetools.partition_sequence_by_counts(
                beat_list[:-remainder_length],
                counts=self.counts,
                cyclic=True,
                overhang=False
                )
            remainder = beat_list[-remainder_length:]
            if self.fuse_remainder:
                grouped_beat_list[-1] = grouped_beat_list[-1] + remainder
            else:
                grouped_beat_list.append(remainder)
        return grouped_beat_list

    def __format__(self, format_specification=''):
        r'''Formats beat grouper.

        ..  container:: example

            ::

                >>> grouper = makertools.PartitionDivisionCallback()
                >>> print(format(grouper))
                makertools.PartitionDivisionCallback(
                    fuse_assignable_total_duration=False,
                    fuse_remainder=False,
                    remainder_direction=Right,
                    )

        Returns string.
        '''
        return AbjadValueObject.__format__(
            self,
            format_specification=format_specification,
            )

    def __repr__(self):
        r'''Gets interpreter representation of beat grouper.

        ..  container:: example

            ::

                >>> makertools.PartitionDivisionCallback()
                PartitionDivisionCallback(fuse_assignable_total_duration=False, fuse_remainder=False, remainder_direction=Right)

        Returns string.
        '''
        return AbjadValueObject.__repr__(self)

    ### PUBLIC PROPERTIES ###

    @property
    def counts(self):
        r'''Gets counts of beat grouper.

        ..  container:: example

            **Example 1.** Groups beats into a single group:

            ::

                >>> grouper = makertools.PartitionDivisionCallback(
                ...     counts=None,
                ...     )
                >>> beat_list = 6 * [Duration(1, 4)]
                >>> grouped_beat_lists = grouper([beat_list])
                >>> grouped_beat_lists[0]
                [[Duration(1, 4), Duration(1, 4), Duration(1, 4), Duration(1, 4), Duration(1, 4), Duration(1, 4)]]
                >>> [len(beat_group) for beat_group in _]
                [6]

        ..  container:: example

            **Example 1.** Groups beats into pairs:

            ::

                >>> grouper = makertools.PartitionDivisionCallback(
                ...     counts=[2],
                ...     )
                >>> beat_list = 6 * [Duration(1, 4)]
                >>> grouped_beat_lists = grouper([beat_list])
                >>> grouped_beat_lists[0]
                [[Duration(1, 4), Duration(1, 4)], [Duration(1, 4), Duration(1, 4)], [Duration(1, 4), Duration(1, 4)]]
                >>> [len(beat_group) for beat_group in _]
                [2, 2, 2]

        ..  container:: example

            **Example 2.** Groups beats into groups of three:

            ::

                >>> grouper = makertools.PartitionDivisionCallback(
                ...     counts=[3],
                ...     )
                >>> beat_list = 6 * [Duration(1, 4)]
                >>> grouped_beat_lists = grouper([beat_list])
                >>> grouped_beat_lists[0]
                [[Duration(1, 4), Duration(1, 4), Duration(1, 4)], [Duration(1, 4), Duration(1, 4), Duration(1, 4)]]
                >>> [len(beat_group) for beat_group in _]
                [3, 3]

        Defaults to none.

        Set to positive integers or none.
        '''
        return self._counts

    @property
    def fuse_assignable_total_duration(self):
        r'''Is true when assignable total duration of all input beats should
        be fused into a single duration. Otherwise false.

        ..  container:: example

            **Example 1.** Groups beats into pairs. Does not fuse assignable
            total durations:

            ::

                >>> grouper = makertools.PartitionDivisionCallback(
                ...     counts=[2],
                ...     fuse_assignable_total_duration=False,
                ...     )

            ::

                >>> beat_list = 5 * [Duration(1, 4)]
                >>> grouped_beat_lists = grouper([beat_list])
                >>> grouped_beat_lists[0]
                [[Duration(1, 4), Duration(1, 4)], [Duration(1, 4), Duration(1, 4)], [Duration(1, 4)]]
                >>> [len(beat_group) for beat_group in _]
                [2, 2, 1]

            ::

                >>> beat_list = 6 * [Duration(1, 4)]
                >>> grouped_beat_lists = grouper([beat_list])
                >>> grouped_beat_lists[0]
                [[Duration(1, 4), Duration(1, 4)], [Duration(1, 4), Duration(1, 4)], [Duration(1, 4), Duration(1, 4)]]
                >>> [len(beat_group) for beat_group in _]
                [2, 2, 2]

            ::

                >>> beat_list = 7 * [Duration(1, 4)]
                >>> grouped_beat_lists = grouper([beat_list])
                >>> grouped_beat_lists[0]
                [[Duration(1, 4), Duration(1, 4)], [Duration(1, 4), Duration(1, 4)], [Duration(1, 4), Duration(1, 4)], [Duration(1, 4)]]
                >>> [len(beat_group) for beat_group in _]
                [2, 2, 2, 1]

            ::

                >>> beat_list = 8 * [Duration(1, 4)]
                >>> grouped_beat_lists = grouper([beat_list])
                >>> grouped_beat_lists[0]
                [[Duration(1, 4), Duration(1, 4)], [Duration(1, 4), Duration(1, 4)], [Duration(1, 4), Duration(1, 4)], [Duration(1, 4), Duration(1, 4)]]
                >>> [len(beat_group) for beat_group in _]
                [2, 2, 2, 2]

            ::

                >>> beat_list = 9 * [Duration(1, 4)]
                >>> grouped_beat_lists = grouper([beat_list])
                >>> grouped_beat_lists[0]
                [[Duration(1, 4), Duration(1, 4)], [Duration(1, 4), Duration(1, 4)], [Duration(1, 4), Duration(1, 4)], [Duration(1, 4), Duration(1, 4)], [Duration(1, 4)]]
                >>> [len(beat_group) for beat_group in _]
                [2, 2, 2, 2, 1]

        ..  container:: example

            **Example 2.** Groups beats into pairs. Fuse assignable total
            durations:

            ::

                >>> grouper = makertools.PartitionDivisionCallback(
                ...     counts=[2],
                ...     fuse_assignable_total_duration=True,
                ...     )

            ::

                >>> beat_list = 5 * [Duration(1, 4)]
                >>> grouped_beat_lists = grouper([beat_list])
                >>> grouped_beat_lists[0]
                [[Duration(1, 4), Duration(1, 4)], [Duration(1, 4), Duration(1, 4)], [Duration(1, 4)]]
                >>> [len(beat_group) for beat_group in _]
                [2, 2, 1]

            ::

                >>> beat_list = 6 * [Duration(1, 4)]
                >>> grouped_beat_lists = grouper([beat_list])
                >>> grouped_beat_lists[0]
                [[Duration(3, 2)]]
                >>> [len(beat_group) for beat_group in _]
                [1]

            ::

                >>> beat_list = 7 * [Duration(1, 4)]
                >>> grouped_beat_lists = grouper([beat_list])
                >>> grouped_beat_lists[0]
                [[Duration(7, 4)]]
                >>> [len(beat_group) for beat_group in _]
                [1]

            ::

                >>> beat_list = 8 * [Duration(1, 4)]
                >>> grouped_beat_lists = grouper([beat_list])
                >>> grouped_beat_lists[0]
                [[Duration(2, 1)]]
                >>> [len(beat_group) for beat_group in _]
                [1]

            ::

                >>> beat_list = 9 * [Duration(1, 4)]
                >>> grouped_beat_lists = grouper([beat_list])
                >>> grouped_beat_lists[0]
                [[Duration(1, 4), Duration(1, 4)], [Duration(1, 4), Duration(1, 4)], [Duration(1, 4), Duration(1, 4)], [Duration(1, 4), Duration(1, 4)], [Duration(1, 4)]]
                >>> [len(beat_group) for beat_group in _]
                [2, 2, 2, 2, 1]

        Overrides all other settings when total duration is assignable.

        Defaults to false.

        Set to true or false.
        '''
        return self._fuse_assignable_total_duration

    @property
    def fuse_remainder(self):
        r'''Is true when remainder beat group should fuse to next closest beat
        group. Otherwise false.

        ..  container:: example

            **Example 1.** Groups beats into pairs. Remainder at right.
            Does not fuse remainder:

            ::

                >>> grouper = makertools.PartitionDivisionCallback(
                ...     counts=[2],
                ...     fuse_remainder=False,
                ...     remainder_direction=Right,
                ...     )

            ::

                >>> beat_list = 5 * [Duration(1, 4)]
                >>> grouped_beat_lists = grouper([beat_list])
                >>> grouped_beat_lists[0]
                [[Duration(1, 4), Duration(1, 4)], [Duration(1, 4), Duration(1, 4)], [Duration(1, 4)]]
                >>> [len(beat_group) for beat_group in _]
                [2, 2, 1]

            ::

                >>> beat_list = 6 * [Duration(1, 4)]
                >>> grouped_beat_lists = grouper([beat_list])
                >>> grouped_beat_lists[0]
                [[Duration(1, 4), Duration(1, 4)], [Duration(1, 4), Duration(1, 4)], [Duration(1, 4), Duration(1, 4)]]
                >>> [len(beat_group) for beat_group in _]
                [2, 2, 2]

            ::

                >>> beat_list = 7 * [Duration(1, 4)]
                >>> grouped_beat_lists = grouper([beat_list])
                >>> grouped_beat_lists[0]
                [[Duration(1, 4), Duration(1, 4)], [Duration(1, 4), Duration(1, 4)], [Duration(1, 4), Duration(1, 4)], [Duration(1, 4)]]
                >>> [len(beat_group) for beat_group in _]
                [2, 2, 2, 1]

            ::

                >>> beat_list = 8 * [Duration(1, 4)]
                >>> grouped_beat_lists = grouper([beat_list])
                >>> grouped_beat_lists[0]
                [[Duration(1, 4), Duration(1, 4)], [Duration(1, 4), Duration(1, 4)], [Duration(1, 4), Duration(1, 4)], [Duration(1, 4), Duration(1, 4)]]
                >>> [len(beat_group) for beat_group in _]
                [2, 2, 2, 2]

            ::

                >>> beat_list = 9 * [Duration(1, 4)]
                >>> grouped_beat_lists = grouper([beat_list])
                >>> grouped_beat_lists[0]
                [[Duration(1, 4), Duration(1, 4)], [Duration(1, 4), Duration(1, 4)], [Duration(1, 4), Duration(1, 4)], [Duration(1, 4), Duration(1, 4)], [Duration(1, 4)]]
                >>> [len(beat_group) for beat_group in _]
                [2, 2, 2, 2, 1]

        ..  container:: example

            **Example 2.** Groups beats into groups of two. Remainder at right.
            Fuses remainder to nearest group:

            ::

                >>> grouper = makertools.PartitionDivisionCallback(
                ...     counts=[2],
                ...     fuse_remainder=True,
                ...     remainder_direction=Right,
                ...     )

            ::

                >>> beat_list = 5 * [Duration(1, 4)]
                >>> grouped_beat_lists = grouper([beat_list])
                >>> grouped_beat_lists[0]
                [[Duration(1, 4), Duration(1, 4)], [Duration(1, 4), Duration(1, 4), Duration(1, 4)]]
                >>> [len(beat_group) for beat_group in _]
                [2, 3]

            ::

                >>> beat_list = 6 * [Duration(1, 4)]
                >>> grouped_beat_lists = grouper([beat_list])
                >>> grouped_beat_lists[0]
                [[Duration(1, 4), Duration(1, 4)], [Duration(1, 4), Duration(1, 4)], [Duration(1, 4), Duration(1, 4)]]
                >>> [len(beat_group) for beat_group in _]
                [2, 2, 2]

            ::

                >>> beat_list = 7 * [Duration(1, 4)]
                >>> grouped_beat_lists = grouper([beat_list])
                >>> grouped_beat_lists[0]
                [[Duration(1, 4), Duration(1, 4)], [Duration(1, 4), Duration(1, 4)], [Duration(1, 4), Duration(1, 4), Duration(1, 4)]]
                >>> [len(beat_group) for beat_group in _]
                [2, 2, 3]

            ::

                >>> beat_list = 8 * [Duration(1, 4)]
                >>> grouped_beat_lists = grouper([beat_list])
                >>> grouped_beat_lists[0]
                [[Duration(1, 4), Duration(1, 4)], [Duration(1, 4), Duration(1, 4)], [Duration(1, 4), Duration(1, 4)], [Duration(1, 4), Duration(1, 4)]]
                >>> [len(beat_group) for beat_group in _]
                [2, 2, 2, 2]

            ::

                >>> beat_list = 9 * [Duration(1, 4)]
                >>> grouped_beat_lists = grouper([beat_list])
                >>> grouped_beat_lists[0]
                [[Duration(1, 4), Duration(1, 4)], [Duration(1, 4), Duration(1, 4)], [Duration(1, 4), Duration(1, 4)], [Duration(1, 4), Duration(1, 4), Duration(1, 4)]]
                >>> [len(beat_group) for beat_group in _]
                [2, 2, 2, 3]

        Defaults to false.

        Set to true or false.
        '''
        return self._fuse_remainder

    @property
    def remainder_direction(self):
        r'''Gets remainder direction of beat grouper.

        ..  container:: example

            **Example 1a.** Groups beats into pairs. Remainder at right:

            ::

                >>> grouper = makertools.PartitionDivisionCallback(
                ...     counts=[2],
                ...     remainder_direction=Right,
                ...     )

            ::

                >>> beat_list = 4 * [Duration(1, 4)]
                >>> grouped_beat_lists = grouper([beat_list])
                >>> grouped_beat_lists[0]
                [[Duration(1, 4), Duration(1, 4)], [Duration(1, 4), Duration(1, 4)]]
                >>> [len(beat_group) for beat_group in _]
                [2, 2]

            ::

                >>> beat_list = 5 * [Duration(1, 4)]
                >>> grouped_beat_lists = grouper([beat_list])
                >>> grouped_beat_lists[0]
                [[Duration(1, 4), Duration(1, 4)], [Duration(1, 4), Duration(1, 4)], [Duration(1, 4)]]
                >>> [len(beat_group) for beat_group in _]
                [2, 2, 1]

            ::

                >>> beat_list = 6 * [Duration(1, 4)]
                >>> grouped_beat_lists = grouper([beat_list])
                >>> grouped_beat_lists[0]
                [[Duration(1, 4), Duration(1, 4)], [Duration(1, 4), Duration(1, 4)], [Duration(1, 4), Duration(1, 4)]]
                >>> [len(beat_group) for beat_group in _]
                [2, 2, 2]

            ::

                >>> beat_list = 7 * [Duration(1, 4)]
                >>> grouped_beat_lists = grouper([beat_list])
                >>> grouped_beat_lists[0]
                [[Duration(1, 4), Duration(1, 4)], [Duration(1, 4), Duration(1, 4)], [Duration(1, 4), Duration(1, 4)], [Duration(1, 4)]]
                >>> [len(beat_group) for beat_group in _]
                [2, 2, 2, 1]

        ..  container:: example

            **Example 1b.** Groups beats into pairs. Remainder at left:

            ::

                >>> grouper = makertools.PartitionDivisionCallback(
                ...     counts=[2],
                ...     remainder_direction=Left,
                ...     )

            ::

                >>> beat_list = 4 * [Duration(1, 4)]
                >>> grouped_beat_lists = grouper([beat_list])
                >>> grouped_beat_lists[0]
                [[Duration(1, 4), Duration(1, 4)], [Duration(1, 4), Duration(1, 4)]]
                >>> [len(beat_group) for beat_group in _]
                [2, 2]

            ::

                >>> beat_list = 5 * [Duration(1, 4)]
                >>> grouped_beat_lists = grouper([beat_list])
                >>> grouped_beat_lists[0]
                [[Duration(1, 4)], [Duration(1, 4), Duration(1, 4)], [Duration(1, 4), Duration(1, 4)]]
                >>> [len(beat_group) for beat_group in _]
                [1, 2, 2]

            ::

                >>> beat_list = 6 * [Duration(1, 4)]
                >>> grouped_beat_lists = grouper([beat_list])
                >>> grouped_beat_lists[0]
                [[Duration(1, 4), Duration(1, 4)], [Duration(1, 4), Duration(1, 4)], [Duration(1, 4), Duration(1, 4)]]
                >>> [len(beat_group) for beat_group in _]
                [2, 2, 2]

            ::

                >>> beat_list = 7 * [Duration(1, 4)]
                >>> grouped_beat_lists = grouper([beat_list])
                >>> grouped_beat_lists[0]
                [[Duration(1, 4)], [Duration(1, 4), Duration(1, 4)], [Duration(1, 4), Duration(1, 4)], [Duration(1, 4), Duration(1, 4)]]
                >>> [len(beat_group) for beat_group in _]
                [1, 2, 2, 2]

        Defaults to right.

        Set to right or left.
        '''
        return self._remainder_direction