from abjad.Meter import Meter
from abjad.Rational import Rational
from abjad.tools import componenttools
from abjad.tools import iterate
from abjad.tools import mathtools
from abjad._Tuplet import _Tuplet


def subsume(expr):
   r'''Subsume all measures in expr containing only top-level tuplet.
   Measures usually become nonbinary as as result of subsumption.

   Return `None`.

   Example::

      abjad> t = RigidMeasure((2, 8), [
         FixedDurationTuplet((2, 8), macros.scale(3))])
      abjad> measuretools.subsume(t)
      abjad> print t.format

      \time 3/12
      \scaleDurations #'(2 . 3) {
         c'8
         d'8
         e'8
      }
   '''

   from abjad.tools import containertools
   for measure in iterate.measures_forward_in_expr(expr):
      if len(measure) == 1:
         if isinstance(measure[0], _Tuplet):
            tuplet = measure[0]
            tuplet_multiplier = tuplet.duration.multiplier
            tuplet_denominator = tuplet_multiplier._d
            reduced_denominator = mathtools.remove_powers_of_two(
               tuplet_denominator)
            meter = measure.meter.effective
            meter_rational = Rational(meter.numerator, meter.denominator)
            numerator = meter_rational._n * reduced_denominator
            denominator = meter_rational._d * reduced_denominator
            measure.meter.forced = Meter(numerator, denominator)
            meter_multiplier = measure.meter.effective.multiplier
            written_adjustment = tuplet_multiplier / meter_multiplier
            componenttools.move_parentage_and_spanners_from_components_to_components([tuplet], tuplet[:])
            containertools.scale_contents_of_container(measure, written_adjustment)
