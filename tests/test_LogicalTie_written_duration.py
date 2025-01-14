import abjad


def test_LogicalTie_written_duration_01():

    staff = abjad.Staff("c' ~ c'16")

    assert abjad.inspect(
        staff[0]
    ).logical_tie().written_duration == abjad.Duration(5, 16)


def test_LogicalTie_written_duration_02():

    staff = abjad.Staff("c'")

    assert abjad.inspect(
        staff[0]
    ).logical_tie().written_duration == abjad.Duration(1, 4)
