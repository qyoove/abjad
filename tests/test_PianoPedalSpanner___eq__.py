import abjad


def test_PianoPedalSpanner___eq___01():
    """
    Spanner is strict comparator.
    """

    spanner_1 = abjad.PianoPedalSpanner()
    spanner_2 = abjad.PianoPedalSpanner()

    assert not spanner_1 == spanner_2