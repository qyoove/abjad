from abjad._Measure.duration import _MeasureDurationInterface


class _DynamicMeasureDurationInterface(_MeasureDurationInterface):

   ### PUBLIC ATTRIBUTES ###

   @property
   def preprolated(self):
      return self.contents
