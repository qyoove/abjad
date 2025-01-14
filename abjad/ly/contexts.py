lilypond_version = "2.19.24"

contexts = {
    "ChoirStaff": {
        "accepts": set(
            [
                "ChoirStaff",
                "ChordNames",
                "DrumStaff",
                "FiguredBass",
                "GrandStaff",
                "Lyrics",
                "PianoStaff",
                "RhythmicStaff",
                "Staff",
                "StaffGroup",
            ]
        ),
        "aliases": set([]),
        "consists": set(
            [
                "Instrument_name_engraver",
                "System_start_delimiter_engraver",
                "Vertical_align_engraver",
            ]
        ),
        "default_child": "Staff",
    },
    "ChordNames": {
        "accepts": set([]),
        "aliases": set(["Staff"]),
        "consists": set(
            [
                "Axis_group_engraver",
                "Chord_name_engraver",
                "Output_property_engraver",
                "Separating_line_group_engraver",
            ]
        ),
    },
    "CueVoice": {
        "accepts": set([]),
        "aliases": set(["Voice"]),
        "consists": set(
            [
                "Arpeggio_engraver",
                "Auto_beam_engraver",
                "Beam_engraver",
                "Bend_engraver",
                "Breathing_sign_engraver",
                "Chord_tremolo_engraver",
                "Cluster_spanner_engraver",
                "Dots_engraver",
                "Double_percent_repeat_engraver",
                "Dynamic_align_engraver",
                "Dynamic_engraver",
                "Fingering_engraver",
                "Font_size_engraver",
                "Forbid_line_break_engraver",
                "Glissando_engraver",
                "Grace_auto_beam_engraver",
                "Grace_beam_engraver",
                "Grace_engraver",
                "Grob_pq_engraver",
                "Instrument_switch_engraver",
                "Laissez_vibrer_engraver",
                "Ligature_bracket_engraver",
                "Multi_measure_rest_engraver",
                "New_fingering_engraver",
                "Note_head_line_engraver",
                "Note_heads_engraver",
                "Note_spacing_engraver",
                "Output_property_engraver",
                "Part_combine_engraver",
                "Percent_repeat_engraver",
                "Phrasing_slur_engraver",
                "Pitched_trill_engraver",
                "Repeat_tie_engraver",
                "Rest_engraver",
                "Rhythmic_column_engraver",
                "Script_column_engraver",
                "Script_engraver",
                "Slash_repeat_engraver",
                "Slur_engraver",
                "Spanner_break_forbid_engraver",
                "Stem_engraver",
                "Text_engraver",
                "Text_spanner_engraver",
                "Tie_engraver",
                "Trill_spanner_engraver",
                "Tuplet_engraver",
            ]
        ),
    },
    "Devnull": {
        "accepts": set([]),
        "aliases": set(["Staff", "Voice"]),
        "consists": set([]),
    },
    "DrumStaff": {
        "accepts": set(["CueVoice", "DrumVoice", "NullVoice"]),
        "aliases": set(["Staff"]),
        "consists": set(
            [
                "Axis_group_engraver",
                "Bar_engraver",
                "Clef_engraver",
                "Collision_engraver",
                "Cue_clef_engraver",
                "Dot_column_engraver",
                "Figured_bass_engraver",
                "Figured_bass_position_engraver",
                "Fingering_column_engraver",
                "Font_size_engraver",
                "Grob_pq_engraver",
                "Instrument_name_engraver",
                "Ledger_line_engraver",
                "Output_property_engraver",
                "Piano_pedal_align_engraver",
                "Pure_from_neighbor_engraver",
                "Rest_collision_engraver",
                "Script_row_engraver",
                "Separating_line_group_engraver",
                "Staff_collecting_engraver",
                "Staff_symbol_engraver",
                "Time_signature_engraver",
            ]
        ),
        "default_child": "DrumVoice",
    },
    "DrumVoice": {
        "accepts": set([]),
        "aliases": set(["Voice"]),
        "consists": set(
            [
                "Auto_beam_engraver",
                "Beam_engraver",
                "Bend_engraver",
                "Breathing_sign_engraver",
                "Chord_tremolo_engraver",
                "Dots_engraver",
                "Double_percent_repeat_engraver",
                "Drum_notes_engraver",
                "Dynamic_align_engraver",
                "Dynamic_engraver",
                "Font_size_engraver",
                "Forbid_line_break_engraver",
                "Grace_auto_beam_engraver",
                "Grace_beam_engraver",
                "Grace_engraver",
                "Grob_pq_engraver",
                "Grob_pq_engraver",
                "Instrument_switch_engraver",
                "Laissez_vibrer_engraver",
                "Multi_measure_rest_engraver",
                "Note_spacing_engraver",
                "Output_property_engraver",
                "Part_combine_engraver",
                "Percent_repeat_engraver",
                "Phrasing_slur_engraver",
                "Pitched_trill_engraver",
                "Repeat_tie_engraver",
                "Rest_engraver",
                "Rhythmic_column_engraver",
                "Script_column_engraver",
                "Script_engraver",
                "Slash_repeat_engraver",
                "Slur_engraver",
                "Spanner_break_forbid_engraver",
                "Stem_engraver",
                "Text_engraver",
                "Text_spanner_engraver",
                "Tie_engraver",
                "Trill_spanner_engraver",
                "Tuplet_engraver",
            ]
        ),
    },
    "Dynamics": {
        "accepts": set([]),
        "aliases": set(["Voice"]),
        "consists": set(
            [
                "Axis_group_engraver",
                "Bar_engraver",
                "Dynamic_align_engraver",
                "Dynamic_engraver",
                "Font_size_engraver",
                "Output_property_engraver",
                "Piano_pedal_engraver",
                "Script_engraver",
                "Text_engraver",
                "Text_spanner_engraver",
            ]
        ),
    },
    "FiguredBass": {
        "accepts": set([]),
        "aliases": set([]),
        "consists": set(
            [
                "Axis_group_engraver",
                "Figured_bass_engraver",
                "Separating_line_group_engraver",
            ]
        ),
    },
    "FretBoards": {
        "accepts": set([]),
        "aliases": set(["Staff"]),
        "consists": set(
            [
                "Axis_group_engraver",
                "Font_size_engraver",
                "Fretboard_engraver",
                "Instrument_name_engraver",
                "Output_property_engraver",
                "Separating_line_group_engraver",
            ]
        ),
    },
    "Global": {
        "accepts": set(["Score"]),
        "aliases": set([]),
        "consists": set([]),
        "default_child": "Score",
    },
    "GrandStaff": {
        "accepts": set(
            [
                "ChordNames",
                "DrumStaff",
                "Dynamics",
                "FiguredBass",
                "Lyrics",
                "RhythmicStaff",
                "Staff",
                "TabStaff",
            ]
        ),
        "aliases": set([]),
        "consists": set(
            [
                "Instrument_name_engraver",
                "Span_arpeggio_engraver",
                "Span_bar_engraver",
                "Span_bar_stub_engraver",
                "System_start_delimiter_engraver",
                "Vertical_align_engraver",
            ]
        ),
        "default_child": "Staff",
    },
    "GregorianTranscriptionStaff": {
        "accepts": set(
            ["CueVoice", "GregorianTranscriptionVoice", "NullVoice"]
        ),
        "aliases": set(["Staff"]),
        "consists": set(
            [
                "Accidental_engraver",
                "Axis_group_engraver",
                "Bar_engraver",
                "Clef_engraver",
                "Collision_engraver",
                "Cue_clef_engraver",
                "Dot_column_engraver",
                "Figured_bass_engraver",
                "Figured_bass_position_engraver",
                "Fingering_column_engraver",
                "Font_size_engraver",
                "Grob_pq_engraver",
                "Instrument_name_engraver",
                "Key_engraver",
                "Ledger_line_engraver",
                "Ottava_spanner_engraver",
                "Output_property_engraver",
                "Piano_pedal_align_engraver",
                "Piano_pedal_engraver",
                "Pure_from_neighbor_engraver",
                "Rest_collision_engraver",
                "Script_row_engraver",
                "Separating_line_group_engraver",
                "Staff_collecting_engraver",
                "Staff_symbol_engraver",
                "Time_signature_engraver",
            ]
        ),
        "default_child": "GregorianTranscriptionVoice",
    },
    "GregorianTranscriptionVoice": {
        "accepts": set([]),
        "aliases": set(["Voice"]),
        "consists": set(
            [
                "Arpeggio_engraver",
                "Auto_beam_engraver",
                "Beam_engraver",
                "Bend_engraver",
                "Breathing_sign_engraver",
                "Chord_tremolo_engraver",
                "Cluster_spanner_engraver",
                "Dots_engraver",
                "Double_percent_repeat_engraver",
                "Dynamic_align_engraver",
                "Dynamic_engraver",
                "Episema_engraver",
                "Fingering_engraver",
                "Font_size_engraver",
                "Forbid_line_break_engraver",
                "Glissando_engraver",
                "Grace_auto_beam_engraver",
                "Grace_beam_engraver",
                "Grace_engraver",
                "Grob_pq_engraver",
                "Instrument_switch_engraver",
                "Laissez_vibrer_engraver",
                "Ligature_bracket_engraver",
                "Multi_measure_rest_engraver",
                "New_fingering_engraver",
                "Note_head_line_engraver",
                "Note_heads_engraver",
                "Note_spacing_engraver",
                "Output_property_engraver",
                "Part_combine_engraver",
                "Percent_repeat_engraver",
                "Phrasing_slur_engraver",
                "Pitched_trill_engraver",
                "Repeat_tie_engraver",
                "Rest_engraver",
                "Rhythmic_column_engraver",
                "Script_column_engraver",
                "Script_engraver",
                "Slash_repeat_engraver",
                "Slur_engraver",
                "Spanner_break_forbid_engraver",
                "Stem_engraver",
                "Text_engraver",
                "Text_spanner_engraver",
                "Tie_engraver",
                "Trill_spanner_engraver",
                "Tuplet_engraver",
            ]
        ),
    },
    "KievanStaff": {
        "accepts": set(["CueVoice", "KievanVoice", "NullVoice"]),
        "aliases": set(["Staff"]),
        "consists": set(
            [
                "Accidental_engraver",
                "Axis_group_engraver",
                "Bar_engraver",
                "Clef_engraver",
                "Collision_engraver",
                "Cue_clef_engraver",
                "Dot_column_engraver",
                "Figured_bass_engraver",
                "Figured_bass_position_engraver",
                "Fingering_column_engraver",
                "Font_size_engraver",
                "Grob_pq_engraver",
                "Instrument_name_engraver",
                "Key_engraver",
                "Ledger_line_engraver",
                "Ottava_spanner_engraver",
                "Output_property_engraver",
                "Piano_pedal_align_engraver",
                "Piano_pedal_engraver",
                "Pure_from_neighbor_engraver",
                "Rest_collision_engraver",
                "Script_row_engraver",
                "Separating_line_group_engraver",
                "Staff_collecting_engraver",
                "Staff_symbol_engraver",
            ]
        ),
        "default_child": "KievanVoice",
    },
    "KievanVoice": {
        "accepts": set([]),
        "aliases": set(["Voice"]),
        "consists": set(
            [
                "Arpeggio_engraver",
                "Auto_beam_engraver",
                "Beam_engraver",
                "Bend_engraver",
                "Breathing_sign_engraver",
                "Chord_tremolo_engraver",
                "Cluster_spanner_engraver",
                "Dots_engraver",
                "Double_percent_repeat_engraver",
                "Dynamic_align_engraver",
                "Dynamic_engraver",
                "Fingering_engraver",
                "Font_size_engraver",
                "Forbid_line_break_engraver",
                "Glissando_engraver",
                "Grace_auto_beam_engraver",
                "Grace_beam_engraver",
                "Grace_engraver",
                "Grob_pq_engraver",
                "Instrument_switch_engraver",
                "Kievan_ligature_engraver",
                "Laissez_vibrer_engraver",
                "Multi_measure_rest_engraver",
                "New_fingering_engraver",
                "Note_head_line_engraver",
                "Note_heads_engraver",
                "Note_spacing_engraver",
                "Output_property_engraver",
                "Part_combine_engraver",
                "Percent_repeat_engraver",
                "Phrasing_slur_engraver",
                "Pitched_trill_engraver",
                "Repeat_tie_engraver",
                "Rest_engraver",
                "Rhythmic_column_engraver",
                "Script_column_engraver",
                "Script_engraver",
                "Slash_repeat_engraver",
                "Slur_engraver",
                "Spanner_break_forbid_engraver",
                "Stem_engraver",
                "Text_engraver",
                "Text_spanner_engraver",
                "Tie_engraver",
                "Trill_spanner_engraver",
                "Tuplet_engraver",
            ]
        ),
    },
    "Lyrics": {
        "accepts": set([]),
        "aliases": set([]),
        "consists": set(
            [
                "Axis_group_engraver",
                "Extender_engraver",
                "Font_size_engraver",
                "Hyphen_engraver",
                "Instrument_name_engraver",
                "Lyric_engraver",
                "Pure_from_neighbor_engraver",
                "Stanza_number_engraver",
            ]
        ),
    },
    "MensuralStaff": {
        "accepts": set(["CueVoice", "MensuralVoice", "NullVoice"]),
        "aliases": set(["Staff"]),
        "consists": set(
            [
                "Accidental_engraver",
                "Axis_group_engraver",
                "Bar_engraver",
                "Clef_engraver",
                "Collision_engraver",
                "Cue_clef_engraver",
                "Custos_engraver",
                "Dot_column_engraver",
                "Figured_bass_engraver",
                "Figured_bass_position_engraver",
                "Fingering_column_engraver",
                "Font_size_engraver",
                "Grob_pq_engraver",
                "Instrument_name_engraver",
                "Key_engraver",
                "Ledger_line_engraver",
                "Ottava_spanner_engraver",
                "Output_property_engraver",
                "Piano_pedal_align_engraver",
                "Piano_pedal_engraver",
                "Pure_from_neighbor_engraver",
                "Rest_collision_engraver",
                "Script_row_engraver",
                "Separating_line_group_engraver",
                "Staff_collecting_engraver",
                "Staff_symbol_engraver",
                "Time_signature_engraver",
            ]
        ),
        "default_child": "MensuralVoice",
    },
    "MensuralVoice": {
        "accepts": set([]),
        "aliases": set(["Voice"]),
        "consists": set(
            [
                "Arpeggio_engraver",
                "Auto_beam_engraver",
                "Beam_engraver",
                "Bend_engraver",
                "Breathing_sign_engraver",
                "Chord_tremolo_engraver",
                "Cluster_spanner_engraver",
                "Dots_engraver",
                "Double_percent_repeat_engraver",
                "Dynamic_align_engraver",
                "Dynamic_engraver",
                "Fingering_engraver",
                "Font_size_engraver",
                "Forbid_line_break_engraver",
                "Glissando_engraver",
                "Grace_auto_beam_engraver",
                "Grace_beam_engraver",
                "Grace_engraver",
                "Grob_pq_engraver",
                "Instrument_switch_engraver",
                "Laissez_vibrer_engraver",
                "Mensural_ligature_engraver",
                "Multi_measure_rest_engraver",
                "New_fingering_engraver",
                "Note_head_line_engraver",
                "Note_heads_engraver",
                "Note_spacing_engraver",
                "Output_property_engraver",
                "Part_combine_engraver",
                "Percent_repeat_engraver",
                "Phrasing_slur_engraver",
                "Pitched_trill_engraver",
                "Repeat_tie_engraver",
                "Rest_engraver",
                "Rhythmic_column_engraver",
                "Script_column_engraver",
                "Script_engraver",
                "Slash_repeat_engraver",
                "Spanner_break_forbid_engraver",
                "Stem_engraver",
                "Text_engraver",
                "Text_spanner_engraver",
                "Tie_engraver",
                "Trill_spanner_engraver",
                "Tuplet_engraver",
            ]
        ),
    },
    "NoteNames": {
        "accepts": set([]),
        "aliases": set([]),
        "consists": set(
            [
                "Axis_group_engraver",
                "Note_name_engraver",
                "Separating_line_group_engraver",
                "Tie_engraver",
            ]
        ),
    },
    "NullVoice": {
        "accepts": set([]),
        "aliases": set(["Staff", "Voice"]),
        "consists": set(
            [
                "Beam_engraver",
                "Grob_pq_engraver",
                "Note_heads_engraver",
                "Pitch_squash_engraver",
                "Slur_engraver",
                "Tie_engraver",
            ]
        ),
    },
    "PetrucciStaff": {
        "accepts": set(["CueVoice", "NullVoice", "PetrucciVoice"]),
        "aliases": set(["Staff"]),
        "consists": set(
            [
                "Accidental_engraver",
                "Axis_group_engraver",
                "Bar_engraver",
                "Clef_engraver",
                "Collision_engraver",
                "Cue_clef_engraver",
                "Custos_engraver",
                "Dot_column_engraver",
                "Figured_bass_engraver",
                "Figured_bass_position_engraver",
                "Fingering_column_engraver",
                "Font_size_engraver",
                "Grob_pq_engraver",
                "Instrument_name_engraver",
                "Key_engraver",
                "Ledger_line_engraver",
                "Ottava_spanner_engraver",
                "Output_property_engraver",
                "Piano_pedal_align_engraver",
                "Piano_pedal_engraver",
                "Pure_from_neighbor_engraver",
                "Rest_collision_engraver",
                "Script_row_engraver",
                "Separating_line_group_engraver",
                "Staff_collecting_engraver",
                "Staff_symbol_engraver",
                "Time_signature_engraver",
            ]
        ),
        "default_child": "PetrucciVoice",
    },
    "PetrucciVoice": {
        "accepts": set([]),
        "aliases": set(["Voice"]),
        "consists": set(
            [
                "Arpeggio_engraver",
                "Auto_beam_engraver",
                "Beam_engraver",
                "Bend_engraver",
                "Breathing_sign_engraver",
                "Chord_tremolo_engraver",
                "Cluster_spanner_engraver",
                "Dots_engraver",
                "Double_percent_repeat_engraver",
                "Dynamic_align_engraver",
                "Dynamic_engraver",
                "Fingering_engraver",
                "Font_size_engraver",
                "Forbid_line_break_engraver",
                "Glissando_engraver",
                "Grace_auto_beam_engraver",
                "Grace_beam_engraver",
                "Grace_engraver",
                "Grob_pq_engraver",
                "Instrument_switch_engraver",
                "Laissez_vibrer_engraver",
                "Mensural_ligature_engraver",
                "Multi_measure_rest_engraver",
                "New_fingering_engraver",
                "Note_head_line_engraver",
                "Note_heads_engraver",
                "Note_spacing_engraver",
                "Output_property_engraver",
                "Part_combine_engraver",
                "Percent_repeat_engraver",
                "Phrasing_slur_engraver",
                "Pitched_trill_engraver",
                "Repeat_tie_engraver",
                "Rest_engraver",
                "Rhythmic_column_engraver",
                "Script_column_engraver",
                "Script_engraver",
                "Slash_repeat_engraver",
                "Slur_engraver",
                "Spanner_break_forbid_engraver",
                "Stem_engraver",
                "Text_engraver",
                "Text_spanner_engraver",
                "Tie_engraver",
                "Trill_spanner_engraver",
                "Tuplet_engraver",
            ]
        ),
    },
    "PianoStaff": {
        "accepts": set(
            [
                "ChordNames",
                "DrumStaff",
                "Dynamics",
                "FiguredBass",
                "Lyrics",
                "RhythmicStaff",
                "Staff",
                "TabStaff",
            ]
        ),
        "aliases": set(["GrandStaff"]),
        "consists": set(
            [
                "Instrument_name_engraver",
                "Keep_alive_together_engraver",
                "Span_arpeggio_engraver",
                "Span_bar_engraver",
                "Span_bar_stub_engraver",
                "System_start_delimiter_engraver",
                "Vertical_align_engraver",
                "Vertical_align_engraver",
            ]
        ),
        "default_child": "Staff",
    },
    "RhythmicStaff": {
        "accepts": set(["CueVoice", "NullVoice", "Voice"]),
        "aliases": set(["Staff"]),
        "consists": set(
            [
                "Axis_group_engraver",
                "Bar_engraver",
                "Dot_column_engraver",
                "Font_size_engraver",
                "Instrument_name_engraver",
                "Ledger_line_engraver",
                "Output_property_engraver",
                "Pitch_squash_engraver",
                "Separating_line_group_engraver",
                "Staff_symbol_engraver",
                "Time_signature_engraver",
            ]
        ),
        "default_child": "Voice",
    },
    "Score": {
        "accepts": set(
            [
                "ChoirStaff",
                "ChordNames",
                "Devnull",
                "DrumStaff",
                "FiguredBass",
                "FretBoards",
                "GrandStaff",
                "GregorianTranscriptionStaff",
                "KievanStaff",
                "Lyrics",
                "MensuralStaff",
                "NoteNames",
                "PetrucciStaff",
                "PianoStaff",
                "RhythmicStaff",
                "Staff",
                "StaffGroup",
                "TabStaff",
                "VaticanaStaff",
            ]
        ),
        "aliases": set(["Timing"]),
        "consists": set(
            [
                "Bar_number_engraver",
                "Beam_collision_engraver",
                "Break_align_engraver",
                "Concurrent_hairpin_engraver",
                "Default_bar_line_engraver",
                "Footnote_engraver",
                "Grace_spacing_engraver",
                "Mark_engraver",
                "Metronome_mark_engraver",
                "Output_property_engraver",
                "Paper_column_engraver",
                "Parenthesis_engraver",
                "Repeat_acknowledge_engraver",
                "Spacing_engraver",
                "Staff_collecting_engraver",
                "Stanza_number_align_engraver",
                "System_start_delimiter_engraver",
                "Timing_translator",
                "Tweak_engraver",
                "Vertical_align_engraver",
                "Volta_engraver",
            ]
        ),
        "default_child": "Staff",
    },
    "Staff": {
        "accepts": set(["CueVoice", "NullVoice", "Voice"]),
        "aliases": set([]),
        "consists": set(
            [
                "Accidental_engraver",
                "Axis_group_engraver",
                "Bar_engraver",
                "Clef_engraver",
                "Collision_engraver",
                "Cue_clef_engraver",
                "Dot_column_engraver",
                "Figured_bass_engraver",
                "Figured_bass_position_engraver",
                "Fingering_column_engraver",
                "Font_size_engraver",
                "Grob_pq_engraver",
                "Instrument_name_engraver",
                "Key_engraver",
                "Ledger_line_engraver",
                "Ottava_spanner_engraver",
                "Output_property_engraver",
                "Piano_pedal_align_engraver",
                "Piano_pedal_engraver",
                "Pure_from_neighbor_engraver",
                "Rest_collision_engraver",
                "Script_row_engraver",
                "Separating_line_group_engraver",
                "Staff_collecting_engraver",
                "Staff_symbol_engraver",
                "Time_signature_engraver",
            ]
        ),
        "default_child": "Voice",
    },
    "StaffGroup": {
        "accepts": set(
            [
                "ChoirStaff",
                "ChordNames",
                "DrumStaff",
                "FiguredBass",
                "FretBoards",
                "GrandStaff",
                "Lyrics",
                "PianoStaff",
                "RhythmicStaff",
                "Staff",
                "StaffGroup",
                "TabStaff",
            ]
        ),
        "aliases": set([]),
        "consists": set(
            [
                "Instrument_name_engraver",
                "Output_property_engraver",
                "Span_arpeggio_engraver",
                "Span_bar_engraver",
                "Span_bar_stub_engraver",
                "System_start_delimiter_engraver",
                "Vertical_align_engraver",
            ]
        ),
        "default_child": "Staff",
    },
    "TabStaff": {
        "accepts": set(["CueVoice", "NullVoice", "TabVoice"]),
        "aliases": set(["Staff"]),
        "consists": set(
            [
                "Axis_group_engraver",
                "Bar_engraver",
                "Clef_engraver",
                "Collision_engraver",
                "Cue_clef_engraver",
                "Dot_column_engraver",
                "Figured_bass_engraver",
                "Figured_bass_position_engraver",
                "Fingering_column_engraver",
                "Font_size_engraver",
                "Grob_pq_engraver",
                "Instrument_name_engraver",
                "Ledger_line_engraver",
                "Output_property_engraver",
                "Piano_pedal_align_engraver",
                "Piano_pedal_engraver",
                "Pure_from_neighbor_engraver",
                "Rest_collision_engraver",
                "Script_row_engraver",
                "Separating_line_group_engraver",
                "Staff_collecting_engraver",
                "Staff_symbol_engraver",
                "Tab_staff_symbol_engraver",
                "Time_signature_engraver",
            ]
        ),
        "default_child": "TabVoice",
    },
    "TabVoice": {
        "accepts": set([]),
        "aliases": set(["Voice"]),
        "consists": set(
            [
                "Arpeggio_engraver",
                "Auto_beam_engraver",
                "Beam_engraver",
                "Bend_engraver",
                "Breathing_sign_engraver",
                "Chord_tremolo_engraver",
                "Cluster_spanner_engraver",
                "Dots_engraver",
                "Double_percent_repeat_engraver",
                "Dynamic_align_engraver",
                "Dynamic_engraver",
                "Font_size_engraver",
                "Forbid_line_break_engraver",
                "Glissando_engraver",
                "Grace_auto_beam_engraver",
                "Grace_beam_engraver",
                "Grace_engraver",
                "Grob_pq_engraver",
                "Instrument_switch_engraver",
                "Laissez_vibrer_engraver",
                "Ligature_bracket_engraver",
                "Multi_measure_rest_engraver",
                "Note_head_line_engraver",
                "Note_spacing_engraver",
                "Output_property_engraver",
                "Part_combine_engraver",
                "Percent_repeat_engraver",
                "Phrasing_slur_engraver",
                "Repeat_tie_engraver",
                "Rest_engraver",
                "Rhythmic_column_engraver",
                "Script_column_engraver",
                "Script_engraver",
                "Slash_repeat_engraver",
                "Slur_engraver",
                "Spanner_break_forbid_engraver",
                "Stem_engraver",
                "Tab_note_heads_engraver",
                "Tab_tie_follow_engraver",
                "Text_engraver",
                "Text_spanner_engraver",
                "Tie_engraver",
                "Trill_spanner_engraver",
                "Tuplet_engraver",
            ]
        ),
    },
    "VaticanaStaff": {
        "accepts": set(["CueVoice", "NullVoice", "VaticanaVoice"]),
        "aliases": set(["Staff"]),
        "consists": set(
            [
                "Accidental_engraver",
                "Axis_group_engraver",
                "Bar_engraver",
                "Clef_engraver",
                "Collision_engraver",
                "Cue_clef_engraver",
                "Custos_engraver",
                "Dot_column_engraver",
                "Figured_bass_engraver",
                "Figured_bass_position_engraver",
                "Fingering_column_engraver",
                "Font_size_engraver",
                "Grob_pq_engraver",
                "Instrument_name_engraver",
                "Key_engraver",
                "Ledger_line_engraver",
                "Ottava_spanner_engraver",
                "Output_property_engraver",
                "Piano_pedal_align_engraver",
                "Piano_pedal_engraver",
                "Pure_from_neighbor_engraver",
                "Rest_collision_engraver",
                "Script_row_engraver",
                "Separating_line_group_engraver",
                "Staff_collecting_engraver",
                "Staff_symbol_engraver",
            ]
        ),
        "default_child": "VaticanaVoice",
    },
    "VaticanaVoice": {
        "accepts": set([]),
        "aliases": set(["Voice"]),
        "consists": set(
            [
                "Arpeggio_engraver",
                "Auto_beam_engraver",
                "Beam_engraver",
                "Bend_engraver",
                "Breathing_sign_engraver",
                "Chord_tremolo_engraver",
                "Cluster_spanner_engraver",
                "Dots_engraver",
                "Double_percent_repeat_engraver",
                "Dynamic_align_engraver",
                "Dynamic_engraver",
                "Episema_engraver",
                "Fingering_engraver",
                "Font_size_engraver",
                "Forbid_line_break_engraver",
                "Glissando_engraver",
                "Grace_auto_beam_engraver",
                "Grace_beam_engraver",
                "Grace_engraver",
                "Grob_pq_engraver",
                "Instrument_switch_engraver",
                "Laissez_vibrer_engraver",
                "Multi_measure_rest_engraver",
                "New_fingering_engraver",
                "Note_head_line_engraver",
                "Note_heads_engraver",
                "Note_spacing_engraver",
                "Output_property_engraver",
                "Part_combine_engraver",
                "Percent_repeat_engraver",
                "Phrasing_slur_engraver",
                "Pitched_trill_engraver",
                "Repeat_tie_engraver",
                "Rest_engraver",
                "Rhythmic_column_engraver",
                "Script_column_engraver",
                "Script_engraver",
                "Slash_repeat_engraver",
                "Spanner_break_forbid_engraver",
                "Text_engraver",
                "Tie_engraver",
                "Trill_spanner_engraver",
                "Tuplet_engraver",
                "Vaticana_ligature_engraver",
            ]
        ),
    },
    "Voice": {
        "accepts": set([]),
        "aliases": set([]),
        "consists": set(
            [
                "Arpeggio_engraver",
                "Auto_beam_engraver",
                "Beam_engraver",
                "Bend_engraver",
                "Breathing_sign_engraver",
                "Chord_tremolo_engraver",
                "Cluster_spanner_engraver",
                "Dots_engraver",
                "Double_percent_repeat_engraver",
                "Dynamic_align_engraver",
                "Dynamic_engraver",
                "Fingering_engraver",
                "Font_size_engraver",
                "Forbid_line_break_engraver",
                "Glissando_engraver",
                "Grace_auto_beam_engraver",
                "Grace_beam_engraver",
                "Grace_engraver",
                "Grob_pq_engraver",
                "Instrument_switch_engraver",
                "Laissez_vibrer_engraver",
                "Ligature_bracket_engraver",
                "Multi_measure_rest_engraver",
                "New_fingering_engraver",
                "Note_head_line_engraver",
                "Note_heads_engraver",
                "Note_spacing_engraver",
                "Output_property_engraver",
                "Part_combine_engraver",
                "Percent_repeat_engraver",
                "Phrasing_slur_engraver",
                "Pitched_trill_engraver",
                "Repeat_tie_engraver",
                "Rest_engraver",
                "Rhythmic_column_engraver",
                "Script_column_engraver",
                "Script_engraver",
                "Slash_repeat_engraver",
                "Slur_engraver",
                "Spanner_break_forbid_engraver",
                "Stem_engraver",
                "Text_engraver",
                "Text_spanner_engraver",
                "Tie_engraver",
                "Trill_spanner_engraver",
                "Tuplet_engraver",
            ]
        ),
    },
}
