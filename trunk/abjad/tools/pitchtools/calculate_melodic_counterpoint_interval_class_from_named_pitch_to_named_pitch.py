from abjad.tools.pitchtools.calculate_melodic_diatonic_interval_from_named_pitch_to_named_pitch import calculate_melodic_diatonic_interval_from_named_pitch_to_named_pitch


def calculate_melodic_counterpoint_interval_class_from_named_pitch_to_named_pitch(pitch_carrier_1, pitch_carrier_2):
   '''.. versionadded:: 1.1.2

   Return melodic counterpoint interval class from `pitch_carrier_1` to
   `pitch_carrier_2`. ::

      abjad> pitchtools.calculate_melodic_counterpoint_interval_class_from_named_pitch_to_named_pitch(NamedPitch(-2), NamedPitch(12))
      MelodicCounterpointIntervalClass(+2)

   ::

      abjad> pitchtools.calculate_melodic_counterpoint_interval_class_from_named_pitch_to_named_pitch(NamedPitch(12), NamedPitch(-2))
      MelodicCounterpointInterval(-2)

   .. versionchanged:: 1.1.2
      renamed ``pitchtools.melodic_counterpoint_interval_class_from_to( )`` to
      ``pitchtools.calculate_melodic_counterpoint_interval_class_from_named_pitch_to_named_pitch( )``.
   '''

   ## get melodic diatonic interval
   mdi = calculate_melodic_diatonic_interval_from_named_pitch_to_named_pitch(pitch_carrier_1, pitch_carrier_2)
  
   ## return melodic counterpoint interval class
   return mdi.melodic_counterpoint_interval.interval_class
