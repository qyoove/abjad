from abjad.helpers.cumulative_sums import cumulative_sums

def diatonic_to_chromatic(num, transpose=0, phase=0):
   '''
   Map diatonic scale degree to chromatic scale degree.
   Defaults to the white keys on the piano, Ionian mode.
   Scale degrees are 0 based.
   0 --> 0
   1 --> 2
   2 --> 4
   3 --> 5
   4 --> 7
   etc..
   '''
   assert isinstance(num, int)
   assert isinstance(phase, int)
   assert phase >= 0
   assert phase < 7

#   dic = {0:0, 1:2, 2:4, 3:5, 4:7, 5:9, 6:11}
#   pclass = num % 7
#   octave = num // 7
#   return 12 * octave + dic[pclass]

   dia_intervals = [2,2,1,2,2,2,1] * 2
   diatonic = dict(zip([0,1,2,3,4,5,6], 
      cumulative_sums([0] + dia_intervals[phase:phase+7])))
   pclass = num % 7
   octave = num // 7
   return 12 * octave + diatonic[pclass] + transpose

   
