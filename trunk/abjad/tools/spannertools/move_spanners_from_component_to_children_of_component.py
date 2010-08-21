def move_spanners_from_component_to_children_of_component(donor):
   '''Give spanners attaching directly to donor to recipients.
   Usual use is to give attached spanners from parent to children,
   which is a composer-safe operation.

   .. versionchanged:: 1.1.2
      renamed ``spannertools.give_attached_to_children( )`` to
      ``spannertools.move_spanners_from_component_to_children_of_component( )``.
   '''

   children = donor[:]

   #for spanner in list(donor.spanners.attached):
   #for spanner in list(donor.spanners._spanners):
   for spanner in donor.spanners:
      i = spanner.index(donor)
      spanner._components[i:i+1] = children
      for child in children:
         #child.spanners._add(spanner)
         child._spanners.add(spanner)
      #donor.spanners._spanners.discard(spanner)
      donor._spanners.discard(spanner)

   return donor
