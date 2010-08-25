#from abjad.interfaces._BacktrackingInterface import _BacktrackingInterface
from abjad.interfaces._ObserverInterface import _ObserverInterface


class KeySignatureInterface(_ObserverInterface):

   def __init__(self, _client, update_interface):
      _ObserverInterface.__init__(self, _client, update_interface)
      self._effective = None

   ## PRIVATE ATTRIBUTES ##

   def _get_effective(self):
      from abjad.tools.marktools.get_effective_mark import get_effective_mark
      from abjad.tools.marktools.KeySignatureMark import KeySignatureMark
      return get_effective_mark(self._client, KeySignatureMark)

   def _update_component(self):
      self._effective = self._get_effective( )

   ## PUBLIC ATTRIBUTES ##

   @property
   def effective(self):
      self._update_prolated_offset_values_of_all_score_components_if_necessary( )
      self._update_observer_interfaces_of_all_score_components_if_necessary( )
      return self._effective


#class KeySignatureInterface(_ObserverInterface, _BacktrackingInterface):
#   '''Publish information about effective and forced key_signature.
#   '''
#   
#   def __init__(self, _client, _update_interface):
#      from abjad.tools.tonalitytools import KeySignature
#      _ObserverInterface.__init__(self, _client, _update_interface)
#      _BacktrackingInterface.__init__(self, 'key_signature')
#      self._acceptableTypes = (KeySignature, )
#      #self._default = tonalitytools.KeySignature('c', 'major')
#      self._default = None
#      self._forced = None
#      #self._suppress = False
#      self._suppress = None
#
#   ## TODO: Generalize _self_should_contribute for both _Clef and _Meter ##
#
#   ## PRIVATE ATTRIBUTES ##
#
#   @property
#   def _self_can_contribute(self):
#      r'''True when self is able to contribute LilyPond stuff.'''
#      return not self.suppress and (self.forced or self.change)
#
#   @property
#   def _self_should_contribute(self):
#      r'''True when self should contribute LilyPond staff.'''
#      return self._self_can_contribute and not self._parent_can_contribute
#
#   @property
#   def _parent_can_contribute(self):
#      r'''True when any parent, other than self, can contribute LP \time.'''
#      for parent in self._client.parentage.proper_parentage:
#         try:
#            if parent.key_signature._self_can_contribute:
#               return True
#         except AttributeError:
#            pass
#      return False
#
#   ## PUBLIC ATTRIBUTES ##
#
#   @property
#   def default(self):
#      return self._default
#
#   @property
#   def _opening(self):
#      '''Format contributions at container opening or before leaf.'''
#      result = [ ]
#      if self._self_should_contribute:
#         result.append(self.effective.format)
#      return result
#
#   @apply
#   def suppress( ):
#      r'''Read / write attribute to suppress contribution
#      of LilyPond \key indication at format-time.'''
#      def fget(self):
#         return self._suppress
#      def fset(self, arg):
#         assert isinstance(arg, (bool, type(None)))
#         self._suppress = arg
#      return property(**locals( ))
