from abjad.tools import *
from experimental import *
from experimental.specificationtools import library
from experimental.settingtools.MultipleContextSetting import MultipleContextSetting
from experimental.settingtools.MultipleContextSettingInventory import MultipleContextSettingInventory
from experimental.selectortools.SingleContextCounttimeComponentItemSelector import \
    SingleContextCounttimeComponentItemSelector
from experimental.specificationtools.ScoreSpecification import ScoreSpecification
from experimental.selectortools.MultipleContextTimespanSelector import MultipleContextTimespanSelector
from experimental.timespantools.Timepoint import Timepoint
from experimental.timespantools.SingleSourceTimespan import SingleSourceTimespan


def test_MultipleContextSettingInventory_storage_format_01():
    '''Storage format exists and is evaluable.
    '''

    score_template = scoretemplatetools.GroupedRhythmicStavesScoreTemplate(staff_count=1)
    score_specification = specificationtools.ScoreSpecification(score_template)

    segment = score_specification.append_segment('red')
    segment.set_time_signatures([(4, 8), (3, 8)])

    multiple_context_setting_inventory_1 = segment.multiple_context_settings

    storage_format = multiple_context_setting_inventory_1.storage_format

    r'''
    settingtools.MultipleContextSettingInventory([
        settingtools.MultipleContextSetting(
            'time_signatures',
            [(4, 8), (3, 8)],
            selectortools.MultipleContextTimespanSelector(
                timespantools.SingleSourceTimespan(
                    selector=selectortools.SegmentItemSelector(
                        index='red'
                        )
                    ),
                context_names=['Grouped Rhythmic Staves Score']
                ),
            persist=True,
            truncate=False
            )
        ])
    '''

    assert storage_format == "settingtools.MultipleContextSettingInventory([\n\tsettingtools.MultipleContextSetting(\n\t\t'time_signatures',\n\t\t[(4, 8), (3, 8)],\n\t\tselectortools.MultipleContextTimespanSelector(\n\t\t\ttimespantools.SingleSourceTimespan(\n\t\t\t\tselector=selectortools.SegmentItemSelector(\n\t\t\t\t\tindex='red'\n\t\t\t\t\t)\n\t\t\t\t),\n\t\t\tcontext_names=['Grouped Rhythmic Staves Score']\n\t\t\t),\n\t\tpersist=True,\n\t\ttruncate=False\n\t\t)\n\t])"

    multiple_context_setting_inventory_2 = eval(storage_format)

    assert isinstance(multiple_context_setting_inventory_1, MultipleContextSettingInventory)
    assert isinstance(multiple_context_setting_inventory_2, MultipleContextSettingInventory)
    assert not multiple_context_setting_inventory_1 is multiple_context_setting_inventory_2
    assert multiple_context_setting_inventory_1 == multiple_context_setting_inventory_2
