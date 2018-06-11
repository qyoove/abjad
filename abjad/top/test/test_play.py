import abjad
import pytest



@pytest.mark.skip('unskip me before building 2.15')
def test_play_01():
    """
    A note can be played.
    """
    note = Note(1, (1, 2))
    play(note)


@pytest.mark.skip('unskip me before building 2.15')
def test_play_02():
    """
    A score can be played.
    """
    notes = [Note(i, (1, 64)) for i in range(10)]
    score = Score([Staff(notes)])
    play(score)