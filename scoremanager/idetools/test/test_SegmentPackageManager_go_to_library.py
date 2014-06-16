# -*- encoding: utf-8 -*-
from abjad import *
import scoremanager
score_manager = scoremanager.idetools.AbjadIDE(is_test=True)


def test_SegmentPackageManager_go_to_library_01():
    r'''From score build files to library.
    '''

    input_ = 'red~example~score g A ** q'
    score_manager._run(input_=input_)
    titles = [
        'Abjad IDE - scores',
        'Red Example Score (2013)',
        'Red Example Score (2013) - segments',
        'Red Example Score (2013) - segments - A',
        'Abjad IDE',
        ]
    assert score_manager._transcript.titles == titles