from abjad.Note import Note
from abjad.tools import componenttools
from abjad.tools import durtools
from abjad._Tuplet import FixedDurationTuplet


def _leaf_to_tuplet_with_n_notes_of_equal_written_duration(l, divisions, prolation):
   '''Divide written duration of `l` according to `divisions`
   and `prolation`.
   '''

   # find target duration of fixed-duration tuplet
   target_duration = l.duration.written

   # find prolated duration of each note in tuplet
   prolated_duration = target_duration / divisions

   # find written duration of each note in tuplet
   if prolation == 'diminution':
      written_duration = durtools.rational_to_equal_or_greater_assignable_rational(
         prolated_duration)
   elif prolation == 'augmentation':
      written_duration = durtools.rational_to_equal_or_lesser_assignable_rational(
         prolated_duration)
   else:
      raise ValueError('must be diminution or augmentation.')

   # make tuplet notes
   notes = Note(0, written_duration) * divisions

   # make tuplet
   tuplet = FixedDurationTuplet(target_duration, notes)

   # give leaf position in score structure to tuplet
   componenttools.move_parentage_and_spanners_from_components_to_components([l], [tuplet])

   # return tuplet
   return tuplet
