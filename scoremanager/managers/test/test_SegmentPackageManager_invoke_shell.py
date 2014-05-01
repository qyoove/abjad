# -*- encoding: utf-8 -*-
import os
from abjad import *
import scoremanager
score_manager = scoremanager.core.ScoreManager(is_test=True)


def test_SegmentPackageManager_invoke_shell_01():

    input_ = 'red~example~score g segment~01 !pwd q'
    score_manager._run(pending_user_input=input_)

    path = os.path.join(
        score_manager._configuration.example_score_packages_directory_path,
        'red_example_score',
        'segments',
        'segment_01',
        )
    string = '\n{}\n'.format(path)
    assert string in score_manager._transcript.contents