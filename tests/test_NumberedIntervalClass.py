import pytest
from abjad import mathtools
from abjad.pitch import (
    NamedInterval,
    NamedIntervalClass,
    NumberedInterval,
    NumberedIntervalClass,
)


values = []

values.extend(
    (x, ((abs(x) % 12) or 12) * mathtools.sign(x)) for x in range(-48, 49)
)

values.extend(
    [
        ("-A1", -1),
        ("-A10", -5),
        ("-A11", -6),
        ("-A12", -8),
        ("-A13", -10),
        ("-A14", -12),
        ("-A2", -3),
        ("-A3", -5),
        ("-A4", -6),
        ("-A5", -8),
        ("-A6", -10),
        ("-A7", -12),
        ("-A8", -1),
        ("-A9", -3),
        ("-AA1", -2),
        ("-AA10", -6),
        ("-AA11", -7),
        ("-AA12", -9),
        ("-AA13", -11),
        ("-AA14", -1),
        ("-AA2", -4),
        ("-AA3", -6),
        ("-AA4", -7),
        ("-AA5", -9),
        ("-AA6", -11),
        ("-AA7", -1),
        ("-AA8", -2),
        ("-AA9", -4),
        ("-AAA1", -3),
        ("-AAA10", -7),
        ("-AAA11", -8),
        ("-AAA12", -10),
        ("-AAA13", -12),
        ("-AAA14", -2),
        ("-AAA2", -5),
        ("-AAA3", -7),
        ("-AAA4", -8),
        ("-AAA5", -10),
        ("-AAA6", -12),
        ("-AAA7", -2),
        ("-AAA8", -3),
        ("-AAA9", -5),
        ("-M10", -4),
        ("-M13", -9),
        ("-M2", -2),
        ("-M3", -4),
        ("-M6", -9),
        ("-M7", -11),
        ("-M9", -2),
        ("-P1", -0),
        ("-P11", -5),
        ("-P12", -7),
        ("-P15", -12),
        ("-P4", -5),
        ("-P5", -7),
        ("-P8", -12),
        ("-d1", -1),
        ("-d10", -2),
        ("-d11", -4),
        ("-d12", -6),
        ("-d13", -7),
        ("-d14", -9),
        ("-d2", -0),
        ("-d3", -2),
        ("-d4", -4),
        ("-d5", -6),
        ("-d6", -7),
        ("-d7", -9),
        ("-d8", 1),
        ("-d9", 0),
        ("-dd1", -2),
        ("-dd10", -1),
        ("-dd11", -3),
        ("-dd12", -5),
        ("-dd13", -6),
        ("-dd14", -8),
        ("-dd2", 1),
        ("-dd3", -1),
        ("-dd4", -3),
        ("-dd5", -5),
        ("-dd6", -6),
        ("-dd7", -8),
        ("-dd8", 2),
        ("-dd9", 1),
        ("-ddd1", -3),
        ("-ddd11", -2),
        ("-ddd12", -4),
        ("-ddd13", -5),
        ("-ddd14", -7),
        ("-ddd2", 2),
        ("-ddd3", 0),
        ("-ddd4", -2),
        ("-ddd5", -4),
        ("-ddd6", -5),
        ("-ddd7", -7),
        ("-ddd8", 3),
        ("-ddd9", 2),
        ("-m10", -3),
        ("-m13", -8),
        ("-m14", -10),
        ("-m2", -1),
        ("-m3", -3),
        ("-m6", -8),
        ("-m7", -10),
        ("-m9", -1),
        ("A1", 1),
        ("A10", 5),
        ("A11", 6),
        ("A12", 8),
        ("A13", 10),
        ("A14", 12),
        ("A2", 3),
        ("A3", 5),
        ("A4", 6),
        ("A5", 8),
        ("A6", 10),
        ("A7", 12),
        ("A8", 1),
        ("A9", 3),
        ("AA1", 2),
        ("AA10", 6),
        ("AA11", 7),
        ("AA12", 9),
        ("AA13", 11),
        ("AA14", 1),
        ("AA2", 4),
        ("AA3", 6),
        ("AA4", 7),
        ("AA5", 9),
        ("AA6", 11),
        ("AA7", 1),
        ("AA8", 2),
        ("AA9", 4),
        ("AAA1", 3),
        ("AAA10", 7),
        ("AAA11", 8),
        ("AAA12", 10),
        ("AAA13", 12),
        ("AAA14", 2),
        ("AAA2", 5),
        ("AAA3", 7),
        ("AAA4", 8),
        ("AAA5", 10),
        ("AAA6", 12),
        ("AAA7", 2),
        ("AAA8", 3),
        ("AAA9", 5),
        ("M10", 4),
        ("M13", 9),
        ("M14", 11),
        ("M2", 2),
        ("M3", 4),
        ("M6", 9),
        ("M7", 11),
        ("M9", 2),
        ("P1", 0),
        ("P11", 5),
        ("P12", 7),
        ("P15", 12),
        ("P4", 5),
        ("P5", 7),
        ("P8", 12),
        ("d1", 1),
        ("d10", 2),
        ("d11", 4),
        ("d12", 6),
        ("d13", 7),
        ("d14", 9),
        ("d2", 0),
        ("d3", 2),
        ("d4", 4),
        ("d5", 6),
        ("d6", 7),
        ("d7", 9),
        ("d8", -1),
        ("d9", 0),
        ("dd1", 2),
        ("dd10", 1),
        ("dd11", 3),
        ("dd12", 5),
        ("dd13", 6),
        ("dd14", 8),
        ("dd2", -1),
        ("dd3", 1),
        ("dd4", 3),
        ("dd5", 5),
        ("dd6", 6),
        ("dd7", 8),
        ("dd8", -2),
        ("dd9", -1),
        ("ddd1", 3),
        ("ddd10", 0),
        ("ddd11", 2),
        ("ddd12", 4),
        ("ddd13", 5),
        ("ddd14", 7),
        ("ddd2", -2),
        ("ddd3", 0),
        ("ddd4", 2),
        ("ddd5", 4),
        ("ddd6", 5),
        ("ddd7", 7),
        ("ddd8", -3),
        ("ddd9", -2),
        ("m10", 3),
        ("m13", 8),
        ("m14", 10),
        ("m2", 1),
        ("m3", 3),
        ("m6", 8),
        ("m7", 10),
        ("m9", 1),
    ]
)

values.extend(
    [
        (("M", 1), ValueError),
        (("M", 4), ValueError),
        (("M", 5), ValueError),
        (("P", 2), ValueError),
        (("P", 3), ValueError),
        (("P", 6), ValueError),
        (("P", 7), ValueError),
        (("m", 1), ValueError),
        (("m", 4), ValueError),
        (("m", 5), ValueError),
    ]
)


@pytest.mark.parametrize("input_, semitones", values)
def test_init(input_, semitones):
    class_ = NumberedIntervalClass
    if isinstance(semitones, type) and issubclass(semitones, Exception):
        with pytest.raises(semitones):
            class_(input_)
    else:
        instance = class_(input_)
        assert float(instance) == semitones
