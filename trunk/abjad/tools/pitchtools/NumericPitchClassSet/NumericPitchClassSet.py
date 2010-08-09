from abjad.tools import listtools
from abjad.tools.pitchtools.InversionEquivalentChromaticIntervalClassSet import InversionEquivalentChromaticIntervalClassSet
from abjad.tools.pitchtools.InversionEquivalentChromaticIntervalClassVector import InversionEquivalentChromaticIntervalClassVector
from abjad.tools.pitchtools.NumericPitchClass import NumericPitchClass
from abjad.tools.pitchtools.list_numeric_pitch_classes_in_expr import list_numeric_pitch_classes_in_expr


## TODO: Make NumericPitchClassSet and PitchSet both inherit ##
## from a shared base class. ##

class  NumericPitchClassSet(frozenset):
   '''.. versionadded:: 1.1.2

   12-ET pitch-class set from American pitch-class theory.
   '''

   def __new__(self, expr):
      pcs = [ ]
      ## assume expr is iterable
      try:
         for x in expr:
            try:
               pcs.append(NumericPitchClass(x))
            except TypeError:
               pcs.extend(get_pitch_classes(x))
      ## if expr is not iterable
      except TypeError:
         ## assume expr can be turned into a single pc
         try:
            pc = NumericPitchClass(expr)
            pcs.append(pc)
         ## expr is a Rest or non-PC type
         except TypeError:
            pcs = [ ]
      #return frozenset.__new__(PitchClassSet, pcs)
      return frozenset.__new__(self, pcs)

   ## OVERLOADS ##

   def __eq__(self, arg):
      if isinstance(arg, NumericPitchClassSet):
         for element in arg:
            if element not in self:
               return False
         else:
            return True
      return False

   def __hash__(self):
      return hash(repr(self))

   def __ne__(self, arg):
      return not self == arg

   def __repr__(self):
      return '%s(%s)' % (self.__class__.__name__, self._format_string)
   
   def __str__(self):
      return '{%s}' % self._format_string

   ## PRIVATE ATTRIBUTES ##

   @property
   def _format_string(self):
      return ', '.join([str(x) for x in sorted(self)])

   ## PUBLIC ATTRIBUTES ##

   @property
   def interval_class_set(self):
      interval_class_set = InversionEquivalentChromaticIntervalClassSet([ ])
      for first_pc, second_pc in listtools.get_unordered_pairs(self):
         interval_class = first_pc - second_pc
         interval_class_set.add(interval_class)
      return interval_class_set

   @property
   def interval_class_vector(self):
      interval_classes = [ ]
      for first_pc, second_pc in listtools.get_unordered_pairs(self):
         interval_class = first_pc - second_pc
         interval_classes.append(interval_class)
      return InversionEquivalentChromaticIntervalClassVector(interval_classes)

   @property
   def pitch_classes(self):
      return tuple(sorted(self))

   @property
   def prime_form(self):
      '''To be implemented.'''
      return None

   ## PUBLIC METHODS ##
   
   def invert(self):
      '''Invert all pcs in self.'''
      return NumericPitchClassSet([pc.invert( ) for pc in self])

   def is_transposed_subset(self, pcset):
      for n in range(12):
         if self.transpose(n).issubset(pcset):
            return True
      return False

   def is_transposed_superset(self, pcset):
      for n in range(12):
         if self.transpose(n).issuperset(pcset):
            return True
      return False

   def multiply(self, n):
      '''Transpose all pcs in self by n.'''
      return NumericPitchClassSet([pc.multiply(n) for pc in self])

   def transpose(self, n):
      '''Transpose all pcs in self by n.'''
      return NumericPitchClassSet([pc.transpose(n) for pc in self])
