from .AbjadObject import AbjadObject
import uqbar.objects


class AbjadValueObject(AbjadObject):
    r'''Abstract base class for classes which compare equally based on their
    storage format.
    '''

    ### CLASS VARIABLES ###

    __slots__ = ()

    ### SPECIAL METHODS ###

    def __copy__(self, *arguments):
        r'''Copies Abjad value object.

        Returns new Abjad value object.
        '''
        return uqbar.objects.new(self)

    def __eq__(self, argument):
        r'''Is true when all initialization values of Abjad value object equal
        the initialization values of `argument`.

        Returns true or false.
        '''
        return uqbar.objects.compare_objects(self, argument)

    def __hash__(self):
        r'''Hashes Abjad value object.

        Returns integer.
        '''
        return uqbar.objects.get_hash(self)
