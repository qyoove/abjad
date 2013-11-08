# -*- encoding: utf-8 -*-
import pytest
from abjad import *


def test_Articulation_01():
    r'''Articulations can be initialized from zero, one or two arguments.
    '''

    articulation = Articulation()
    assert articulation.name == None
    assert articulation.direction is None
    articulation = Articulation('^\\marcato')
    assert articulation.name == 'marcato'
    assert articulation.direction is Up
    articulation = Articulation('legato', Down)
    assert articulation.name == 'legato'
    assert articulation.direction is Down


def test_Articulation_02():
    r'''Articulations have string and direction.
    '''

    note = Note("c'4")
    articulation = Articulation('staccato')
    attach(articulation, note)
    assert articulation.name == 'staccato'
    assert articulation.direction is None


def test_Articulation_03():
    r'''Articulation name can be set to none.
    '''

    note = Note("c'4")
    articulation = Articulation()
    attach(articulation, note)
    assert articulation.name is None
    assert str(articulation) == ''


def test_Articulation_04():
    r'''Direction can be set to None.
    '''

    note = Note("c'4")
    articulation = Articulation('staccato', None)
    attach(articulation, note)
    assert articulation.direction is None
    assert str(articulation) == r'-\staccato'


def test_Articulation_05():
    r'''Direction can be set to up.
    '''

    note = Note("c'4")
    articulation = Articulation('staccato', Up)
    attach(articulation, note)
    assert articulation.direction is Up
    assert str(articulation) == r'^\staccato'

    articulation = Articulation('staccato', '^')
    assert articulation.direction is Up
    assert str(articulation) == r'^\staccato'


def test_Articulation_06():
    r'''Direction can be set to down.
    '''

    note = Note("c'4")
    articulation = Articulation('staccato', Down)
    attach(articulation, note)
    assert articulation.direction is Down
    assert str(articulation) == r'_\staccato'

    articulation = Articulation('staccato', '_')
    assert articulation.direction is Down
    assert str(articulation) == r'_\staccato'


def test_Articulation_07():
    r'''Direction can be set to default.
    '''

    note = Note("c'4")
    articulation = Articulation('staccato')
    assert articulation.direction is None
    assert str(articulation) == r'-\staccato'

    articulation = Articulation('staccato', '-')
    assert articulation.direction is Center
    assert str(articulation) == r'-\staccato'



def test_Articulation_08():
    r'''Shortcut strings are replaced with full word.
    '''

    note = Note("c'4")
    articulation = Articulation('.')
    attach(articulation, note)
    assert articulation.name == '.'
    assert str(articulation) == r'-\staccato'

    articulation = Articulation('-')
    assert articulation.name == '-'
    assert str(articulation) == r'-\tenuto'

    articulation = Articulation('|')
    assert articulation.name == '|'
    assert str(articulation) == r'-\staccatissimo'
