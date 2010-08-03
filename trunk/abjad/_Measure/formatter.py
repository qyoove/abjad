from abjad.Container.formatter import _ContainerFormatter
from abjad.exceptions import OverfullMeasureError
from abjad.exceptions import UnderfullMeasureError
from abjad._Measure.number import _MeasureFormatterNumberInterface
from abjad._Measure.slots import _MeasureFormatterSlotsInterface
from abjad.Rational import Rational
from abjad._Tuplet import FixedMultiplierTuplet


class _MeasureFormatter(_ContainerFormatter):
   '''Encapsulate all
   :class:`~abjad._Measure.dynamic.measure.DynamicMeasure` and
   :class:`~abjad._Measure.anonymous.AnonymousMeasure.AnonymousMeasure` 
   format logic. ::

      abjad> measure = AnonymousMeasure(macros.scale(3))
      abjad> measure.formatter
      <_MeasureFormatter>

   ::

      abjad> measure = DynamicMeasure(macros.scale(3))
      abjad> measure.formatter
      <_MeasureFormatter>

   :class:`~abjad._Measure.rigid.measure.RigidMeasure` instances implement
   a special formatter which inherits from this base class. ::

      abjad> measure = RigidMeasure((3, 8), macros.scale(3))
      abjad> measure.formatter
      <_RigidMeasureFormatter>
   '''

   def __init__(self, client):
      _ContainerFormatter.__init__(self, client)
      self._number = _MeasureFormatterNumberInterface(self)
      self._slots = _MeasureFormatterSlotsInterface(self)

   ## PUBLIC ATTRIBUTES ##

   @property
   def slots(self):
      '''Read-only reference to 
      :class:`~abjad._Measure.slots._MeasureFormatterSlotsInterface`.'''

      return self._slots
