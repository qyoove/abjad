# -*- encoding: utf-8 -*-
from abjad import *
from abjad.tools import iotools


def test_iotools_IOManager_get_next_output_file_name_01():

    next_output_file_name = iotools.IOManager.get_next_output_file_name()

    assert isinstance(next_output_file_name, str)
    assert len(next_output_file_name) == 7
    assert next_output_file_name.endswith('.ly')
