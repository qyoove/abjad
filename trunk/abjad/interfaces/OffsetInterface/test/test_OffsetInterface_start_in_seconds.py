from abjad import *
import py.test


def test_OffsetInterface_start_in_seconds_01( ):
   '''Offset seconds can not calculate without excplit tempo indication.'''

   t = Staff(macros.scale(4))
   
   r'''
   \new Staff {
      c'8
      d'8
      e'8
      f'8
   }
   '''

   assert py.test.raises(UndefinedTempoError, 't[0].offset.start_in_seconds')
   assert py.test.raises(UndefinedTempoError, 't[0].offset.stop_in_seconds')


def test_OffsetInterface_start_in_seconds_02( ):
   '''Offset seconds work with explicit tempo indication.'''

   t = Staff(macros.scale(4))
   #t.tempo.forced = tempotools.TempoIndication(Rational(1, 8), 48)
   marktools.TempoMark(Rational(1, 8), 48)(t)
   
   r'''
   \new Staff {
      \tempo 8=48
      c'8
      d'8
      e'8
      f'8
   }
   '''

   assert t[0].offset.start_in_seconds == Rational(0)
   assert t[1].offset.start_in_seconds == Rational(5, 4)
