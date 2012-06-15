from abjad.tools import componenttools
from abjad.tools import contexttools
from abjad.tools.abctools.AbjadObject import AbjadObject
from experimental.specificationtools.Callback import Callback
from experimental.specificationtools.Division import Division
from experimental.specificationtools.SegmentSpecification import SegmentSpecification
import types


class ScoreObjectIndicator(AbjadObject):
    r'''.. versionadded:: 1.0

    A frozen request to pick out an arbitrary object in score.

    (Oject-oriented delayed evaluation.)

    Score object indicator objects afford the identification of score
    objects that do not yet exist.

    Initialize with different combinations of optional `segment`, `context`, `klass`, `index` and `predicate`. 

    Pick out the entire score::

        >>> from experimental import specificationtools

    ::

        >>> specificationtools.ScoreObjectIndicator()
        ScoreObjectIndicator()

    Pick out the segment with name ``'red'``::

        >>> specificationtools.ScoreObjectIndicator(segment='red')
        ScoreObjectIndicator(segment='red')


    Pick context ``'Voice 1'`` out of the segment with name ``'red'``::

        >>> specificationtools.ScoreObjectIndicator(segment='red', context='Voice 1')
        ScoreObjectIndicator(segment='red', context='Voice 1')

    Pick the first measure in context ``'Voice 1'`` out of the segment with name ``'red'``::

        >>> specificationtools.ScoreObjectIndicator(segment='red', context='Voice 1', klass=Measure)
        ScoreObjectIndicator(segment='red', context='Voice 1', klass=measuretools.Measure)
    
    Pick the first division in context ``'Voice 1'`` out of the segment with name ``'red'``::

        >>> from experimental.specificationtools.Division import Division

    ::

        >>> specificationtools.ScoreObjectIndicator(segment='red', context='Voice 1', klass=Division)
        ScoreObjectIndicator(segment='red', context='Voice 1', klass=specificationtools.Division)

    Pick the first note in context ``'Voice 1'`` out of the segment with name ``'red'``::

        >>> specificationtools.ScoreObjectIndicator(segment='red', context='Voice 1', klass=Note)
        ScoreObjectIndicator(segment='red', context='Voice 1', klass=notetools.Note)

    Pick note ``20`` in context ``'Voice 1'`` out of the segment with name ``'red'``::

        >>> specificationtools.ScoreObjectIndicator(segment='red', context='Voice 1', klass=Note, index=20)
        ScoreObjectIndicator(segment='red', context='Voice 1', klass=notetools.Note, index=20)

    Pick the first chord with at least six pitches
    in context ``'Voice 1'`` out of the segment with name ``'red'``::

        >>> from experimental.specificationtools.Callback import Callback

    ::

        >>> command = 'lambda x: 6 <= len(x)'
        >>> predicate = Callback(eval(command), command)

    ::

        >>> specificationtools.ScoreObjectIndicator(segment='red', context='Voice 1', klass=Chord, predicate=predicate)
        ScoreObjectIndicator(segment='red', context='Voice 1', klass=chordtools.Chord, predicate=Callback('lambda x: 6 <= len(x)'))

    Pick chord ``20`` with at least six pitches
    in context ``'Voice 1'`` out of the segment with name ``'red'``::

        >>> specificationtools.ScoreObjectIndicator(segment='red', context='Voice 1', klass=Chord, predicate=predicate, index=20)
        ScoreObjectIndicator(segment='red', context='Voice 1', klass=chordtools.Chord, predicate=Callback('lambda x: 6 <= len(x)'), index=20)

    Examples below reference the score object indicator defined immediately above::

        >>> score_object_indicator = _

    Score object indicators are immutable.

    Limitations of the design:

    Score object indicators do not afford the specification of nested objects.
    So it is not possible to pick the first leaf of the last tuplet anywhere in score.

    When or if we decide we want such functionality it will be necessary to initialize score 
    object indicators with some type of nested object.
    '''

    ### INITIALIZER ###

    def __init__(self, segment=None, context=None, klass=None, predicate=None, index=None):
        if isinstance(segment, SegmentSpecification):
            segment = segment.name
        assert isinstance(segment, (str, type(None))), repr(segment)
        if isinstance(context, contexttools.Context):
            context = context.name
        assert isinstance(context, (str, type(None))), repr(context)
        if klass is not None:
            assert issubclass(klass, (componenttools.Component, Division)), repr(klass)
        assert isinstance(predicate, (Callback, type(None))), repr(predicate)
        assert isinstance(index, (int, type(None))), repr(index)
        self._segment = segment
        self._context = context
        self._klass = klass
        self._predicate = predicate
        self._index = index
    
    ### SPECIAL METHODS ###

    def __eq__(self, other):
        '''True when `other` is a score object indicator with `segment`,
        `context`, `klass`, `predicate` and `index` all equal to those of `self`.
        
        Otherwise false.
        
        Return boolean.
        '''
        if not isinstance(other, type(self)):
            return False
        elif not self.segment == other.segment:
            return False
        elif not self.context == other.context:
            return False
        elif not self.klass == other.klass:
            return False
        elif not self.predicate == other.predicate:
            return False
        elif not self.index == other.index:
            return False
        else:
            return True

    ### READ-ONLY PUBLIC PROPERTIES ###
    
    @property
    def context(self):
        '''Name of score object indicator context specified by user::

            >>> score_object_indicator.context
            'Voice 1'

        Return string or none.
        '''
        return self._context

    @property
    def index(self):
        '''Index of score object indicator specified by user::

            >>> score_object_indicator.index
            20

        Return integer or none.
        '''
        return self._index

    @property
    def is_context(self):
        '''True when `context` is not none but all other attributes are none.

        Otherwise false.
    
        Return boolean.
        '''
        if self.context is not None:
            other_attributes = (self.index, self.klass, self.predicate, self.segment)
            if all([x is None for x in other_attributes]):
                return True
        return False

    @property
    def is_klass(self):
        '''True when `klass` is not none but all other attributes are none.

        Otherwise false.
    
        Return boolean.
        '''
        if self.klass is not None:
            other_attributes = (self.context, self.index, self.predicate, self.segment)
            if all([x is None for x in other_attributes]):
                return True
        return False

    @property
    def is_score(self):
        '''True all attributes are none.

        Otherwise false.

        Return boolean.
        '''
        other_attributes = (self.context, self.index, self.klass, self.predicate, self.segment)
        if all([x is None for x in other_attributes]):
            return True
        return False

    @property
    def is_segment(self):
        '''True when `segment` is not none but all other attributes are none.

        Otherwise false.

        Return boolean.
        '''
        if self.segment is not None:
            other_attributes = (self.context, self.index, self.klass, self.predicate)
            if all([x is None for x in other_attributes]):
                return True
        return False

    @property
    def klass(self):
        '''Class of score object indicator specified by user::

            >>> score_object_indicator.klass is Chord
            True

        Return Abjad component class, division class or none.
        '''
        return self._klass

    @property
    def predicate(self):
        '''Predicate of score object indicator specified by user::

            >>> score_object_indicator.predicate
            Callback('lambda x: 6 <= len(x)')

        Return callback or none.
        '''
        return self._predicate

    @property
    def segment(self):
        '''Name of score object indicator segment specified by user::

            >>> score_object_indicator.segment
            'red'

        Return string or none.
        '''
        return self._segment
