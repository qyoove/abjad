import abjad


def test_Rest___init___01():
    """
    Initialize rest from LilyPond input string.
    """

    rest = abjad.Rest("r8.")

    assert rest.written_duration == abjad.Duration(3, 16)


def test_Rest___init___02():
    """
    Initialize rest from other rest.
    """

    rest_1 = abjad.Rest("r4", multiplier=(1, 2))
    abjad.override(rest_1).staff.note_head.color = "red"
    rest_2 = abjad.Rest(rest_1)

    assert isinstance(rest_1, abjad.Rest)
    assert isinstance(rest_2, abjad.Rest)
    assert format(rest_1) == format(rest_2)
    assert rest_1 is not rest_2


def test_Rest___init___03():
    """
    Initialize rest from chord.
    """

    chord = abjad.Chord([2, 3, 4], (1, 4))
    rest = abjad.Rest(chord)

    assert isinstance(rest, abjad.Rest)
    assert dir(chord) == dir(abjad.Chord([2, 3, 4], (1, 4)))
    assert dir(rest) == dir(abjad.Rest((1, 4)))
    assert rest.written_duration == chord.written_duration


def test_Rest___init___04():
    """
    Initialize rest from tupletized chord.
    """

    chord = abjad.Chord([2, 3, 4], abjad.Duration(1, 4))
    tuplet = abjad.Tuplet((2, 3), 3 * chord)
    rest = abjad.Rest(tuplet[0])

    assert format(rest) == abjad.String.normalize(
        r"""
        r4
        """
    )

    assert abjad.inspect(rest).wellformed()


def test_Rest___init___05():
    """
    Initialize rest from beamed chord.
    """

    chord = abjad.Chord([2, 3, 4], abjad.Duration(1, 8))
    staff = abjad.Staff(3 * chord)
    abjad.beam(staff[:])
    rest = abjad.Rest(staff[0])

    assert format(rest) == abjad.String.normalize(
        r"""
        r8
        [
        """
    )

    assert abjad.inspect(rest).wellformed()


def test_Rest___init___06():
    """
    Initialize rest from skip.
    """

    skip = abjad.Skip("s4")
    rest = abjad.Rest(skip)

    assert format(rest) == abjad.String.normalize(
        r"""
        r4
        """
    )

    assert abjad.inspect(rest).wellformed()


def test_Rest___init___07():
    """
    Initialize rest from tupletted skip.
    """

    skip = abjad.Skip("s4")
    tuplet = abjad.Tuplet((2, 3), 3 * skip)
    rest = abjad.Rest(tuplet[0])

    assert format(rest) == abjad.String.normalize(
        r"""
        r4
        """
    )

    assert abjad.inspect(rest).wellformed()


def test_Rest___init___08():
    """
    Initialize rest from beamed skip.
    """

    skip = abjad.Skip("s8")
    staff = abjad.Staff("c'8 [ s4 c'd ]")
    rest = abjad.Rest(staff[1])

    assert format(rest) == abjad.String.normalize(
        r"""
        r4
        """
    )

    assert abjad.inspect(rest).wellformed()


def test_Rest___init___09():
    """
    Initialize rest from note.
    """

    note = abjad.Note("c'4")
    rest = abjad.Rest(note)

    assert format(rest) == abjad.String.normalize(
        r"""
        r4
        """
    )

    assert abjad.inspect(rest).wellformed()


def test_Rest___init___10():
    """
    Initialize rest from tupletized note.
    """

    tuplet = abjad.Tuplet((2, 3), "c'4 d'4 e'4")
    rest = abjad.Rest(tuplet[0])

    assert format(rest) == abjad.String.normalize(
        r"""
        r4
        """
    )

    assert abjad.inspect(rest).wellformed()


def test_Rest___init___11():
    """
    Initialize rest from beamed note.
    """

    staff = abjad.Staff("c'8 [ d'8 e'8 ]")
    rest = abjad.Rest(staff[0])

    assert format(rest) == abjad.String.normalize(
        r"""
        r8
        [
        """
    )

    assert abjad.inspect(rest).wellformed()


def test_Rest___init___12():
    """
    Initialize multiple rests from spanned notes.
    """

    voice = abjad.Voice("c'8 ( d'8 e'8 f'8 )")
    for note in voice:
        rest = abjad.Rest(note)
        abjad.mutate(note).replace(rest)

    assert format(voice) == abjad.String.normalize(
        r"""
        \new Voice
        {
            r8
            (
            r8
            r8
            r8
            )
        }
        """
    )

    assert abjad.inspect(voice).wellformed()


def test_Rest___init___13():
    """
    Initializes rest from empty input.
    """

    rest = abjad.Rest()

    assert format(rest) == abjad.String.normalize(
        r"""
        r4
        """
    )

    assert abjad.inspect(rest).wellformed()
