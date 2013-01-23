from abjad.tools import mathtools
from abjad.tools import sequencetools
from experimental.tools.settingtools.AbsoluteExpression import AbsoluteExpression
from experimental.tools.settingtools.StartPositionedObject import StartPositionedObject


class StartPositionedAbsoluteExpression(AbsoluteExpression, StartPositionedObject):
    '''Start-positioned absolute expression.

        >>> expression = settingtools.StartPositionedAbsoluteExpression(
        ...     [(4, 16), (2, 16)], start_offset=Offset(40, 8))

    ::

        >>> expression = expression.repeat_to_length(6)

    ::

        >>> z(expression)
        settingtools.StartPositionedAbsoluteExpression(
            payload=((4, 16), (2, 16), (4, 16), (2, 16), (4, 16), (2, 16)),
            start_offset=durationtools.Offset(5, 1)
            )

    Start-positioned absolute expressions are assumed to evaluate
    to a list or other iterable.
    '''

    ### INITIALIZER ###

    def __init__(self, payload=None, start_offset=None):
        AbsoluteExpression.__init__(self, payload=payload)
        StartPositionedObject.__init__(self, start_offset=start_offset)

    ### READ-ONLY PUBLIC PROPERTIES ###

    @property
    def start_offset(self):
        '''Start-positioned absolute expression start offset:

        ::

            >>> expression.start_offset
            Offset(5, 1)

        Return offset.
        '''
        return StartPositionedObject.start_offset.fget(self)

    ### PUBLIC METHODS ###

    def partition_by_ratio(self, ratio):
        '''Partition payload by `ratio`:

        ::

            >>> payload = [(6, 8), (6, 8), (6, 8), (6, 8), (6, 4), (6, 4)]
            >>> expression = settingtools.StartPositionedAbsoluteExpression(payload, Offset(2))

        ::

            >>> result = expression.partition_by_ratio((1, 1)) # doctest: +SKIP


        Return newly constructed start-positioned absolute expression.
        '''
        raise NotImplementedError

    def partition_by_ratio_of_durations(self, ratio):
        '''Partition payload by `ratio` of durations:

        ::

            >>> payload = [(6, 8), (6, 8), (6, 8), (6, 8), (6, 4), (6, 4)]
            >>> expression = settingtools.StartPositionedAbsoluteExpression(payload, Offset(2))

        ::

            >>> result = expression.partition_by_ratio_of_durations((1, 1)) # doctest: +SKIP


        Return newly constructed start-positioned absolute expression.
        '''
        raise NotImplementedError

    def reflect(self):
        '''Reflect payload about axis:

        ::

            >>> payload = [(6, 8), (6, 8), (3, 4)]
            >>> expression = settingtools.StartPositionedAbsoluteExpression(payload, Offset(2))

        ::

            >>> result = expression.reflect()    

        ::

            >>> z(result)
            settingtools.StartPositionedAbsoluteExpression(
                payload=((3, 4), (6, 8), (6, 8)),
                start_offset=durationtools.Offset(2, 1)
                )

        Return newly constructed start-positioned absolute expression.
        '''
        expression = AbsoluteExpression.reflect(self)
        payload = expression.payload
        result = type(self)(payload=payload, start_offset=self.start_offset)
        return result

    def repeat_to_duration(self, duration):
        '''Repeat payload to `duration`:

            >>> payload = [(6, 8), (6, 8), (3, 4)]
            >>> expression = settingtools.StartPositionedAbsoluteExpression(payload, Offset(2))

        ::

            >>> result = expression.repeat_to_duration(Duration(17, 4))

        ::
    
            >>> z(result)
            settingtools.StartPositionedAbsoluteExpression(
                payload=(NonreducedFraction(6, 8), NonreducedFraction(6, 8), 
                    NonreducedFraction(3, 4), NonreducedFraction(6, 8), 
                    NonreducedFraction(6, 8), NonreducedFraction(4, 8)),
                start_offset=durationtools.Offset(2, 1)
                )
        
        Return newly constructed start-positioned absolute expression.
        '''
        if not sequencetools.all_are_numbers(self.payload):
            payload = [mathtools.NonreducedFraction(x) for x in self.payload]
        else:
            paylad = self.payload
        payload = sequencetools.repeat_sequence_to_weight_exactly(payload, duration)
        result = type(self)(payload=payload, start_offset=self.start_offset)
        return result

    def repeat_to_length(self, length):
        '''Repeat payload to `length`:

            >>> payload = [(6, 8), (6, 8), (3, 4)]
            >>> expression = settingtools.StartPositionedAbsoluteExpression(payload, Offset(2))

        ::

            >>> result = expression.repeat_to_length(5)

        ::
    
            >>> z(result)
            settingtools.StartPositionedAbsoluteExpression(
                payload=((6, 8), (6, 8), (3, 4), (6, 8), (6, 8)),
                start_offset=durationtools.Offset(2, 1)
                )

        Return newly constructed start-positioned absolute expression.
        '''
        expression = AbsoluteExpression.repeat_to_length(self, length)
        result = type(self)(payload=expression.payload, start_offset=self.start_offset)
        return result

    def rotate(self, rotation):
        '''Rotate payload by `rotation`:

        ::

            >>> payload = [(6, 8), (6, 8), (3, 4)]
            >>> expression = settingtools.StartPositionedAbsoluteExpression(payload, Offset(2))

        ::

            >>> result = expression.rotate(-1)    

        
        Return newly constructed start-positioned absolute expression.
        '''
        expression = AbsoluteExpression.rotate(self, rotation)
        result = type(self)(payload=expression.payload, start_offset=self.start_offset)
        return result

    def translate(self, translation):
        '''Translate division region product by `translation`:
        
            >>> payload = [(6, 8), (6, 8), (3, 4)]
            >>> expression = settingtools.StartPositionedAbsoluteExpression(payload, Offset(2))

        ::

            >>> result = expression.translate(-1)

        ::
            >>> z(result)
            settingtools.StartPositionedAbsoluteExpression(
                payload=((6, 8), (6, 8), (3, 4)),
                start_offset=durationtools.Offset(1, 1)
                )

        Return newly constructed start-positioned absolute expression.
        '''
        new_start_offset = self.start_offset + translation
        result = type(self)(payload=self.payload, start_offset=new_start_offset)
        return result
