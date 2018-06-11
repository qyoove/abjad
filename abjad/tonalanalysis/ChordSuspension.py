import re
from abjad import system
from abjad.abctools.AbjadValueObject import AbjadValueObject


class ChordSuspension(AbjadValueObject):
    """
    Chord suspension.

    ..  container:: example

        Initializes from numbers:

        >>> abjad.tonalanalysis.ChordSuspension('4-b3')
        ChordSuspension('4-b3')

    ..  container:: example

        Initializes from other suspension:

        >>> suspension = abjad.tonalanalysis.ChordSuspension('4-3')
        >>> abjad.tonalanalysis.ChordSuspension(suspension)
        ChordSuspension('4-3')

    9-8, 7-6, 4-3, 2-1 and other types of suspension typical of, for example,
    the Bach chorales.
    """

    ### CLASS VARIABLES ###

    __slots__ = (
        '_start',
        '_stop',
        )

    _symbol_regex = re.compile(r'([#|b]?\d+)-([#|b]?\d+)')

    ### INITIALIZER ###

    def __init__(self, figured_bass_string='4-3'):
        if isinstance(figured_bass_string, type(self)):
            figured_bass_string = figured_bass_string.figured_bass_string
        start, stop = self._initialize_by_symbol(figured_bass_string)
        self._start = start
        self._stop = stop

    ### SPECIAL METHODS ###

    def __eq__(self, argument):
        """
        Is true when ``argument`` is a chord suspension when start and stop
        equal to those of this chord suspension.

        ..  container:: example

            >>> suspension_1 = abjad.tonalanalysis.ChordSuspension('4-3')
            >>> suspension_2 = abjad.tonalanalysis.ChordSuspension('4-3')
            >>> suspension_3 = abjad.tonalanalysis.ChordSuspension('2-1')

            >>> suspension_1 == suspension_1
            True
            >>> suspension_1 == suspension_2
            True
            >>> suspension_1 == suspension_3
            False


            >>> suspension_2 == suspension_1
            True
            >>> suspension_2 == suspension_2
            True
            >>> suspension_2 == suspension_3
            False


            >>> suspension_3 == suspension_1
            False
            >>> suspension_3 == suspension_2
            False
            >>> suspension_3 == suspension_3
            True

        Returns true or false.
        """
        return super(ChordSuspension, self).__eq__(argument)

    def __hash__(self):
        """
        Hashes chord suspension.

        Required to be explicitly redefined on Python 3 if __eq__ changes.

        Returns integer.
        """
        return super(ChordSuspension, self).__hash__()

    def __str__(self):
        """
        Gets string representation of chord suspension.

        Returns string.
        """
        if self.start is not None and self.stop is not None:
            return '{!s}-{!s}'.format(self.start, self.stop)
        else:
            return ''

    ### PRIVATE METHODS ###

    def _get_format_specification(self):
        values = [self.figured_bass_string]
        return system.FormatSpecification(
            client=self,
            repr_is_indented=False,
            storage_format_is_indented=False,
            storage_format_args_values=values,
            )

    def _initialize_by_pair(self, pair):
        start, stop = pair
        return self._initialize_by_start_and_stop(start, stop)

    def _initialize_by_reference(self, chord_suspension):
        start, stop = chord_suspension.start, chord_suspension.stop
        return self._initialize_by_start_and_stop(start, stop)

    def _initialize_by_start_and_stop(self, start, stop):
        from abjad import tonalanalysis
        start = tonalanalysis.ScaleDegree(start)
        stop = tonalanalysis.ScaleDegree(stop)
        return start, stop

    def _initialize_by_symbol(self, symbol):
        from abjad import tonalanalysis
        groups = self._symbol_regex.match(symbol).groups()
        start, stop = groups
        start = tonalanalysis.ScaleDegree(start)
        stop = tonalanalysis.ScaleDegree(stop)
        return start, stop

    def _initialize_empty(self):
        return None, None

    ### PUBLIC PROPERTIES ###

    @property
    def chord_name(self):
        """
        Gets chord name.

        ..  container:: example

            >>> abjad.tonalanalysis.ChordSuspension('4-b3').chord_name
            'sus4'

            >>> abjad.tonalanalysis.ChordSuspension('b2-1').chord_name
            'susb2'

        Returns string.
        """
        return 'sus{!s}'.format(self.start)

    @property
    def figured_bass_pair(self):
        """
        Gets figured bass pair.

        ..  container:: example

            >>> abjad.tonalanalysis.ChordSuspension('4-b3').figured_bass_pair
            ('4', 'b3')

            >>> abjad.tonalanalysis.ChordSuspension('b2-1').figured_bass_pair
            ('b2', '1')

        Returns integer pair.
        """
        return str(self.start), str(self.stop)

    @property
    def figured_bass_string(self):
        """
        Gets figured bass string.

        ..  container:: example

            >>> abjad.tonalanalysis.ChordSuspension('4-b3').figured_bass_string
            '4-b3'

            >>> abjad.tonalanalysis.ChordSuspension('b2-1').figured_bass_string
            'b2-1'

        Returns string.
        """
        return '{!s}-{!s}'.format(self.start, self.stop)

    @property
    def start(self):
        """
        Gets start.


            >>> abjad.tonalanalysis.ChordSuspension('4-b3').start
            ScaleDegree('4')

            >>> abjad.tonalanalysis.ChordSuspension('b2-1').start
            ScaleDegree('b2')

        Returns scale degree.
        """
        return self._start

    @property
    def stop(self):
        """
        Gets stop.

        ..  container:: example

            >>> abjad.tonalanalysis.ChordSuspension('4-b3').stop
            ScaleDegree('b3')

            >>> abjad.tonalanalysis.ChordSuspension('b2-1').stop
            ScaleDegree('1')

        Returns scale degree.
        """
        return self._stop

    @property
    def title_string(self):
        """
        Gets title string.

        ..  container:: example

            >>> abjad.tonalanalysis.ChordSuspension('4-b3').title_string
            'FourFlatThreeSuspension'

            >>> abjad.tonalanalysis.ChordSuspension('b2-1').title_string
            'FlatTwoOneSuspension'

        Returns string.
        """
        start = self.start.title_string
        stop = self.stop.title_string
        return '{!s}{!s}Suspension'.format(start, stop)