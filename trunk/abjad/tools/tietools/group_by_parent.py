from abjad.tools.tietools.is_chain import is_chain
import itertools


def group_by_parent(tie_chain):
   r'''Group leaves in `tie_chain` by immediate parent::

      abjad> staff = Staff(RigidMeasure((2, 8), construct.run(2)) * 2)
      abjad> Tie(staff.leaves)
      abjad> f(staff)
      \new Staff {
         {
            \time 2/8
            c'8 ~
            c'8 ~
         }
         {
            \time 2/8
            c'8 ~
            c'8
         }
      }
      
   ::
      
      abjad> tietools.group_by_parent(staff.leaves[0].tie.chain) 
      [[Note(c', 8), Note(c', 8)], [Note(c', 8), Note(c', 8)]]

   Return list of leaf group lists.
   '''

   ## check input
   if not is_chain(tie_chain):
      raise TypeError('must be tie chain.')
   
   ## create partition with itertools
   result = [ ]
   pairs_generator = itertools.groupby(tie_chain, lambda x: x.parentage.parent)
   for key, values_generator in pairs_generator:
      result.append(list(values_generator))

   ## return result
   return result
