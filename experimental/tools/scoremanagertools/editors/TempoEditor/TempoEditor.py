# -*- encoding: utf-8 -*-
from abjad.tools import marktools
from abjad.tools import durationtools
from experimental.tools.scoremanagertools.editors.InteractiveEditor \
    import InteractiveEditor
from experimental.tools.scoremanagertools.editors.TargetManifest \
    import TargetManifest
from experimental.tools.scoremanagertools import getters


class TempoEditor(InteractiveEditor):

    ### CLASS VARIABLES ###

    target_manifest = TargetManifest(
        marktools.Tempo,
        ('duration', 'd', getters.get_duration),
        ('units_per_minute', 'm', getters.get_integer),
        )