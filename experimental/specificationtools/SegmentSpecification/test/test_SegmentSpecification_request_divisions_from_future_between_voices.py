from abjad import *
from experimental import *


def test_SegmentSpecification_request_divisions_from_future_between_voices_01():
    '''From-future division material request between voices.
    '''

    score_template = scoretemplatetools.GroupedRhythmicStavesScoreTemplate(staff_count=2)
    score_specification = specificationtools.ScoreSpecification(score_template)

    red_segment = score_specification.make_segment(name='red')
    blue_segment = score_specification.make_segment(name='blue')

    red_segment.set_time_signatures([(2, 8), (2, 8)])
    blue_voice_2_divisions = blue_segment.request_divisions('Voice 2')
    red_segment.set_divisions(blue_voice_2_divisions)
    red_segment.set_divisions([(2, 16), (5, 16)], contexts=['Voice 2'])
    red_segment.set_rhythm(library.sixteenths)

    blue_segment.set_time_signatures([(3, 8), (3, 8)])
    blue_segment.set_divisions([(2, 16), (3, 16)], contexts=['Voice 1'])

    score = score_specification.interpret()

    current_function_name = introspectiontools.get_current_function_name()
    helpertools.write_test_output(score, __file__, current_function_name)
    assert score.lilypond_format == helpertools.read_test_output(__file__, current_function_name)


def test_SegmentSpecification_request_divisions_from_future_between_voices_02():
    '''From-future division material request between voices with request-time reverse.
    '''

    score_template = scoretemplatetools.GroupedRhythmicStavesScoreTemplate(staff_count=2)
    score_specification = specificationtools.ScoreSpecification(score_template)

    red_segment = score_specification.make_segment(name='red')
    blue_segment = score_specification.make_segment(name='blue')

    red_segment.set_time_signatures([(2, 8), (2, 8)])
    blue_voice_2_divisions = blue_segment.request_divisions('Voice 2', reverse=True)
    red_segment.set_divisions(blue_voice_2_divisions)
    red_segment.set_divisions([(2, 16), (5, 16)], contexts=['Voice 2'])
    red_segment.set_rhythm(library.sixteenths)

    blue_segment.set_time_signatures([(3, 8), (3, 8)])
    blue_segment.set_divisions([(2, 16), (3, 16)], contexts=['Voice 1'])

    score = score_specification.interpret()

    current_function_name = introspectiontools.get_current_function_name()
    helpertools.write_test_output(score, __file__, current_function_name)
    assert score.lilypond_format == helpertools.read_test_output(__file__, current_function_name)


def test_SegmentSpecification_request_divisions_from_future_between_voices_03():
    '''From-future division material request between voices with set-time reverse.
    '''

    score_template = scoretemplatetools.GroupedRhythmicStavesScoreTemplate(staff_count=2)
    score_specification = specificationtools.ScoreSpecification(score_template)

    red_segment = score_specification.make_segment(name='red')
    blue_segment = score_specification.make_segment(name='blue')

    red_segment.set_time_signatures([(2, 8), (2, 8)])
    blue_voice_2_divisions = blue_segment.request_divisions('Voice 2')
    red_segment.set_divisions(blue_voice_2_divisions, reverse=True)
    red_segment.set_divisions([(2, 16), (5, 16)], contexts=['Voice 2'])
    red_segment.set_rhythm(library.sixteenths)

    blue_segment.set_time_signatures([(3, 8), (3, 8)])
    blue_segment.set_divisions([(2, 16), (3, 16)], contexts=['Voice 1'])

    score = score_specification.interpret()

    current_function_name = introspectiontools.get_current_function_name()
    helpertools.write_test_output(score, __file__, current_function_name)
    assert score.lilypond_format == helpertools.read_test_output(__file__, current_function_name)


def test_SegmentSpecification_request_divisions_from_future_between_voices_04():
    '''From-future division material request between voices with both request- and set-time reverse.
    '''

    score_template = scoretemplatetools.GroupedRhythmicStavesScoreTemplate(staff_count=2)
    score_specification = specificationtools.ScoreSpecification(score_template)

    red_segment = score_specification.make_segment(name='red')
    blue_segment = score_specification.make_segment(name='blue')

    red_segment.set_time_signatures([(2, 8), (2, 8)])
    blue_voice_2_divisions = blue_segment.request_divisions('Voice 2', reverse=True)
    red_segment.set_divisions(blue_voice_2_divisions, reverse=True)
    red_segment.set_divisions([(2, 16), (5, 16)], contexts=['Voice 2'])
    red_segment.set_rhythm(library.sixteenths)

    blue_segment.set_time_signatures([(3, 8), (3, 8)])
    blue_segment.set_divisions([(2, 16), (3, 16)], contexts=['Voice 1'])

    score = score_specification.interpret()

    current_function_name = introspectiontools.get_current_function_name()
    helpertools.write_test_output(score, __file__, current_function_name)
    assert score.lilypond_format == helpertools.read_test_output(__file__, current_function_name)
