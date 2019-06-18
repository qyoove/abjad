"""
Tools for modeling "timespans".
"""

from .Timespan import Timespan
from .AnnotatedTimespan import AnnotatedTimespan
from .CompoundInequality import CompoundInequality
from .TimeRelation import TimeRelation
from .OffsetTimespanTimeRelation import OffsetTimespanTimeRelation
from .TimespanInequality import TimespanInequality
from .TimespanList import TimespanList
from .TimespanTimespanTimeRelation import TimespanTimespanTimeRelation
from .offset_happens_after_timespan_starts import (
    offset_happens_after_timespan_starts,
)
from .offset_happens_after_timespan_stops import (
    offset_happens_after_timespan_stops,
)
from .offset_happens_before_timespan_starts import (
    offset_happens_before_timespan_starts,
)
from .offset_happens_before_timespan_stops import (
    offset_happens_before_timespan_stops,
)
from .offset_happens_during_timespan import offset_happens_during_timespan
from .offset_happens_when_timespan_starts import (
    offset_happens_when_timespan_starts,
)
from .offset_happens_when_timespan_stops import (
    offset_happens_when_timespan_stops,
)
from .timespan_2_contains_timespan_1_improperly import (
    timespan_2_contains_timespan_1_improperly,
)
from .timespan_2_curtails_timespan_1 import timespan_2_curtails_timespan_1
from .timespan_2_delays_timespan_1 import timespan_2_delays_timespan_1
from .timespan_2_happens_during_timespan_1 import (
    timespan_2_happens_during_timespan_1,
)
from .timespan_2_intersects_timespan_1 import timespan_2_intersects_timespan_1
from .timespan_2_is_congruent_to_timespan_1 import (
    timespan_2_is_congruent_to_timespan_1,
)
from .timespan_2_overlaps_all_of_timespan_1 import (
    timespan_2_overlaps_all_of_timespan_1,
)
from .timespan_2_overlaps_only_start_of_timespan_1 import (
    timespan_2_overlaps_only_start_of_timespan_1,
)
from .timespan_2_overlaps_only_stop_of_timespan_1 import (
    timespan_2_overlaps_only_stop_of_timespan_1,
)
from .timespan_2_overlaps_start_of_timespan_1 import (
    timespan_2_overlaps_start_of_timespan_1,
)
from .timespan_2_overlaps_stop_of_timespan_1 import (
    timespan_2_overlaps_stop_of_timespan_1,
)
from .timespan_2_starts_after_timespan_1_starts import (
    timespan_2_starts_after_timespan_1_starts,
)
from .timespan_2_starts_after_timespan_1_stops import (
    timespan_2_starts_after_timespan_1_stops,
)
from .timespan_2_starts_before_timespan_1_starts import (
    timespan_2_starts_before_timespan_1_starts,
)
from .timespan_2_starts_before_timespan_1_stops import (
    timespan_2_starts_before_timespan_1_stops,
)
from .timespan_2_starts_during_timespan_1 import (
    timespan_2_starts_during_timespan_1,
)
from .timespan_2_starts_when_timespan_1_starts import (
    timespan_2_starts_when_timespan_1_starts,
)
from .timespan_2_starts_when_timespan_1_stops import (
    timespan_2_starts_when_timespan_1_stops,
)
from .timespan_2_stops_after_timespan_1_starts import (
    timespan_2_stops_after_timespan_1_starts,
)
from .timespan_2_stops_after_timespan_1_stops import (
    timespan_2_stops_after_timespan_1_stops,
)
from .timespan_2_stops_before_timespan_1_starts import (
    timespan_2_stops_before_timespan_1_starts,
)
from .timespan_2_stops_before_timespan_1_stops import (
    timespan_2_stops_before_timespan_1_stops,
)
from .timespan_2_stops_during_timespan_1 import (
    timespan_2_stops_during_timespan_1,
)
from .timespan_2_stops_when_timespan_1_starts import (
    timespan_2_stops_when_timespan_1_starts,
)
from .timespan_2_stops_when_timespan_1_stops import (
    timespan_2_stops_when_timespan_1_stops,
)
from .timespan_2_trisects_timespan_1 import timespan_2_trisects_timespan_1
