# -*- encoding: utf-8 -*-
from abjad import *


def test_TempoMark_is_imprecise_01( ):
    r'''Tempo mark is imprecise if either duration or units_per_minute is None,
    or if units_per_minute is a tuple representing a tempo range.
    '''

    assert not TempoMark(Duration(1, 4), 60).is_imprecise
    assert not TempoMark('Langsam', 4, 60).is_imprecise
    assert TempoMark('Langsam').is_imprecise
    assert TempoMark('Langsam', 4, (35, 50)).is_imprecise
    assert TempoMark(Duration(1, 4), (35, 50)).is_imprecise
