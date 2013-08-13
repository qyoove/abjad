# -*- encoding: utf-8 -*-
from abjad.tools import durationtools
from abjad.tools import mathtools
from abjad.tools import sequencetools


def get_likely_multiplier_of_components(components):
    r'''Get likely multiplier of `components`:

    ::

        >>> staff = Staff("c'8.. d'8.. e'8.. f'8..")

    ..  doctest::

        >>> f(staff)
        \new Staff {
            c'8..
            d'8..
            e'8..
            f'8..
        }

    ::

        >>> measuretools.get_likely_multiplier_of_components(staff[:])
        Multiplier(7, 4)

    Return 1 when no multiplier is likely:

    ::

        >>> staff = Staff("c'8 d'8 e'8 f'8")

    ..  doctest::

        >>> f(staff)
        \new Staff {
            c'8
            d'8
            e'8
            f'8
        }

    ::

        >>> measuretools.get_likely_multiplier_of_components(staff[:])
        Multiplier(1, 1)

    Return none when more than one multiplier is likely:

    ::

        >>> staff = Staff(
        ...     notetools.make_notes([0, 2, 4, 5], [(3, 16), (7, 32)]))

    ..  doctest::

        >>> f(staff)
        \new Staff {
            c'8.
            d'8..
            e'8.
            f'8..
        }

    ::

        >>> measuretools.get_likely_multiplier_of_components(staff[:]) is None
        True

    Return multiplier or none.
    '''
    from abjad.tools import componenttools
    from abjad.tools import iterationtools
    from abjad.tools import leaftools
    from abjad.tools import selectiontools

    assert all(isinstance(x, componenttools.Component) for x in components)

    chain_duration_numerators = []
    for expr in \
        iterationtools.iterate_topmost_tie_chains_and_components_in_expr(
        components):
        if isinstance(expr, selectiontools.TieChain):
            chain_duration = expr._preprolated_duration
            chain_duration_numerators.append(chain_duration.numerator)

    if len(sequencetools.truncate_runs_in_sequence(
        chain_duration_numerators)) == 1:
        numerator = chain_duration_numerators[0]
        denominator = mathtools.greatest_power_of_two_less_equal(numerator)
        likely_multiplier = durationtools.Multiplier(numerator, denominator)
        return likely_multiplier
