import abjad


def test_Parentage_is_orphan_01():

    staff = abjad.Staff("c'8 d'8 e'8 f'8")

    assert abjad.inspect(staff).parentage().is_orphan
    for note in staff:
        assert not abjad.inspect(note).parentage().is_orphan
