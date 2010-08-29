from abjad.components.Note import Note
from abjad.core import Rational
from abjad.components.Skip import Skip
from abjad.tools import durtools
from abjad.tools import leaftools
from abjad.tools import mathtools


def _fill_measures_in_expr(expr, mode, iterctrl = lambda measure, i: True):
   '''Populate each measure in 'expr' according to 'mode'.

   With mode = 'big-endian':
      Populate with big-endian series of notes
      summing to duration of effective meter of measure.
   
   With mode = 'little-endian':
      Populate with little-endian series of notes
      summing to duration of effective meter of measure.
   
   With mode = 'meter series':
      Populate with n total 1/d notes, where
      n equals effective_meter.numerator, and
      d equals effective_meter.denominator.

   With mode = 'skip':
      Populate with exactly one skip, such that
      skip.duration.prolated == effective_meter.duration.
      Remove spanners attaching to measure.

   When mode is None:
      Empty the contents of each measure.

   .. versionchanged:: 1.1.2
      renamed ``measuretools.populate( )``
      to ``measuretools._fill_measures_in_expr( )``.
   '''

   if mode == 'big-endian':
      _measures_populate_big_endian(expr, iterctrl)
   elif mode == 'little-endian':
      _measures_populate_little_endian(expr, iterctrl)
   elif mode == 'meter series':
      _measures_populate_meter_series(expr, iterctrl)
   elif mode == 'skip':
      _measures_populate_skip(expr, iterctrl)
   elif durtools.is_duration_token(mode):
      _measures_populate_duration_train(expr, mode, iterctrl)
   elif mode is None:
      _measures_populate_none(expr, iterctrl)
   else:
      raise ValueError('unknown measure population mode "%s".' % mode)
