from abjad.core.interface import _Interface
from abjad.helpers.hasname import hasname
from abjad.helpers.iterate import iterate


class _ComponentSpannerAggregator(_Interface):

   def __init__(self, client):
      _Interface.__init__(self, client)
      self._spanners = set([ ])

   ### PRIVATE METHODS ###

   def _fractureContents(self):
      '''
      Left-fractures all spanners attaching to t and to any components
      attaching to t and starting at the same moment as t.
      Right-fractures all spanners attaching to t and to any components
      attaching to t and stopping at the same moment as t.

      Used by _Component.copy( ) only.
      '''

      result = [ ]
      client = self._client
      for component in client._navigator._contemporaneousStartComponents:
         for spanner in component.spanners.attached:
            result.append(spanner.fracture(spanner.index(component), 'left'))
      for component in client._navigator._contemporaneousStopComponents:
         for spanner in component.spanners.attached:
            result.append(spanner.fracture(spanner.index(component), 'right'))
      return result

   def _update(self, spanners):
      self._spanners.update(spanners)

   ### PUBLIC ATTRIBUTES ###
   
   @property
   def attached(self):
      '''
      Return an unordered set of all spanners attaching 
      directly to client.
      '''

      return self._spanners

   @property
   def contained(self):
      '''
      Return an unordered set of all spanners attaching to 
      any components in client, including client.
      '''

      result = set([ ])
      for component in iterate(self._client, '_Component'):
         result.update(set(component.spanners.attached))
      #return list(result)
      return result

   @property
   def spanned(self):
      '''
      Return True when any spanners attach to self, 
      False otherwise.
      '''
      
      return len(self.attached) > 0

   ### PUBLIC METHODS ###

   def clear(self):
      for spanner in list(self.attached):
         spanner.clear( )

   def detach(self):
      '''Remove client from all spanners attaching to client.'''
      client = self._client
      for spanner in list(self.attached):
         spanner.remove(client)

   def fracture(self, direction = 'both'):
      result = [ ]
      client = self._client
      for spanner in self.attached:
         result.append(spanner.fracture(spanner.index(client), direction))
      return result
