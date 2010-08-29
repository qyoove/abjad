from abjad.core import Rational
from abjad.tools import marktools


def is_bar_line_crossing_leaf(leaf):
   r'''.. versionadded:: 1.1.2

   True when `leaf` crosses bar line::

      abjad> t = Staff(macros.scale(4))
      abjad> t[2].duration.written *= 2
      abjad> marktools.TimeSignatureMark(2, 8, partial = Rational(1, 8))(t[2])
      abjad> f(t)
      \new Staff {
              \time 2/8
              \partial 8
              c'8
              d'8
              e'4
              f'8
      }
      abjad> leaftools.is_bar_line_crossing_leaf(t.leaves[2])
      True

   Otherwise false::

      abjad> leaftools.is_bar_line_crossing_leaf(t.leaves[3])
      False
   '''

   meter = marktools.get_effective_time_signature(leaf)
   partial = meter.partial
   if meter.partial is None:
      partial = Rational(0)

   shifted_start = (leaf.offset.start - partial) % meter.duration
   shifted_stop = (leaf.offset.stop - partial) % meter.duration

   if meter.duration < shifted_start + leaf.duration.prolated:
      return True

   return False
