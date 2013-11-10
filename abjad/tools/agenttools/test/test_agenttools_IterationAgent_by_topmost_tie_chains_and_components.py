# -*- encoding: utf-8 -*-
from abjad import *


def test_agenttools_IterationAgent_by_topmost_tie_chains_and_components_01():
    r'''Iterate toplevel contents with tie chains in place of leaves.
    '''

    staff = Staff(r"c'8 ~ c'32 g'8 ~ g'32 a'8 ~ a'32 b'8 ~ b'32")
    tuplet = scoretools.FixedDurationTuplet((2, 8), "c'8 d'8 e'8")
    staff.insert(4, tuplet)

    assert testtools.compare(
        staff,
        r'''
        \new Staff {
            c'8 ~
            c'32
            g'8 ~
            g'32
            \times 2/3 {
                c'8
                d'8
                e'8
            }
            a'8 ~
            a'32
            b'8 ~
            b'32
        }
        '''
        )

    chained_contents = iterate(staff).by_topmost_tie_chains_and_components()
    chained_contents = list(chained_contents)

    assert chained_contents[0] == inspect(staff[0]).get_tie_chain()
    assert chained_contents[1] == inspect(staff[2]).get_tie_chain()
    assert chained_contents[2] is staff[4]
    assert chained_contents[3] == inspect(staff[5]).get_tie_chain()
    assert chained_contents[4] == inspect(staff[7]).get_tie_chain()