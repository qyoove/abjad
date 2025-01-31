import abjad
import copy


def test_LilyPondSettingNameManager___eq___01():

    note_1 = abjad.Note("c'4")
    abjad.setting(note_1).voice.auto_beaming = False
    abjad.setting(note_1).staff.tuplet_full_length = True

    note_2 = abjad.Note("c'4")
    abjad.setting(note_2).voice.auto_beaming = False
    abjad.setting(note_2).staff.tuplet_full_length = True

    note_3 = abjad.Note("c'4")
    abjad.setting(note_3).voice.auto_beaming = True

    context_setting_component_plug_in_1 = abjad.setting(note_1)
    context_setting_component_plug_in_2 = abjad.setting(note_2)
    context_setting_component_plug_in_3 = abjad.setting(note_3)

    assert (
        context_setting_component_plug_in_1
        == context_setting_component_plug_in_1
    )
    assert (
        context_setting_component_plug_in_1
        == context_setting_component_plug_in_2
    )
    assert (
        not context_setting_component_plug_in_1
        == context_setting_component_plug_in_3
    )
    assert (
        context_setting_component_plug_in_2
        == context_setting_component_plug_in_1
    )
    assert (
        context_setting_component_plug_in_2
        == context_setting_component_plug_in_2
    )
    assert (
        not context_setting_component_plug_in_2
        == context_setting_component_plug_in_3
    )
    assert (
        not context_setting_component_plug_in_3
        == context_setting_component_plug_in_1
    )
    assert (
        not context_setting_component_plug_in_3
        == context_setting_component_plug_in_2
    )
    assert (
        context_setting_component_plug_in_3
        == context_setting_component_plug_in_3
    )
