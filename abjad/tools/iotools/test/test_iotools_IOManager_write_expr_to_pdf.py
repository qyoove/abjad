# -*- encoding: utf-8 -*-
from abjad import *
from abjad.tools import iotools
import os


def test_iotools_IOManager_write_expr_to_pdf_01():

    staff = Staff("c'8 d'8 e'8 f'8")
    iotools.IOManager.write_expr_to_pdf(staff, 'tmp_staff.pdf')
    assert os.path.exists('tmp_staff.pdf')

    os.remove('tmp_staff.pdf')
    assert not os.path.exists('tmp_staff.pdf')
