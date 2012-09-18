from abjad.tools import componenttools
from abjad.tools import containertools
from abjad.tools import durationtools
from abjad.tools.abctools.AbjadObject import AbjadObject


class OffsetPositionedRhythmExpression(AbjadObject):
    r'''.. versionadded:: 1.0

    Rhythm expression.

    One voice of counttime components: tuplets, notes, rests and chords.

    The interpretive process of building up the rhythm for a complete
    voice of music involves the generation of many different rhythm expressions.
    The rhythmic interpretation of a voice completes when enough    
    contiguous rhythm expressions exist to account for the entire
    duration of the voice.

    The many different rhythm expressions that together constitute the
    rhythm of a voice may not necessarily be constructed in
    chronological order during interpretation.

    Initializing ``start_offset=None`` will set `start_offset` to
    ``Offset(0)``.
    
    Composers do not create rhythm expression objects because 
    rhythm expressions arise as a byproduct of interpretation.
    '''

    ### INITIALIZER ###

    def __init__(self, music=None, start_offset=None, stop_offset=None):
        music = containertools.Container(music=music)
        self._music = music
        self._start_offset = start_offset or durationtools.Offset(0)

    ### SPECIAL METHODS ###

    def __copy__(self, *args):
        new = type(self)(start_offset=self.start_offset)
        new._music = componenttools.copy_components_and_covered_spanners([self.music])[0]
        return new

    __deepcopy__ = __copy__

    ### READ-ONLY PUBLIC PROPERTIES ###

    @property
    def music(self):
        '''Offset-positioned rhythm expression music.

        Return container.
        '''
        return self._music

    @property
    def start_offset(self):
        '''Rhythm expression start offset.

        Assigned at initialization during rhythm interpretation.

        Return offset.
        '''
        return self._start_offset

    @property
    def stop_offset(self):
        '''Rhythm expression stop offset.
        
        Defined equal to start offset plus 
        prolated duration of rhythm expression

        Return offset.
        '''
        return self.start_offset + self.music.prolated_duration
