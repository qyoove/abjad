import abjad
import os


def test_IOManager_save_last_ly_as_01():

    abjad_output_directory = abjad.abjad_configuration.abjad_output_directory
    lilypond_files = [
        x for x in os.listdir(abjad_output_directory) if x.endswith(".ly")
    ]
    if not lilypond_files:
        note = abjad.Note("c'4")
        abjad.persist(note).as_ly()

    abjad.IOManager.save_last_ly_as("tmp_foo.ly")
    assert os.path.exists("tmp_foo.ly")

    os.remove("tmp_foo.ly")
    assert not os.path.exists("tmp_foo.ly")
