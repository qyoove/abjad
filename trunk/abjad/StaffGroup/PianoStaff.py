from abjad.StaffGroup.StaffGroup import StaffGroup


#def PianoStaff(music):
#   result = StaffGroup(music)
#   result.context = 'PianoStaff'
#   return result

class PianoStaff(StaffGroup):

   def __init__(self, music):
      StaffGroup.__init__(self, music)
      self.context = 'PianoStaff'
