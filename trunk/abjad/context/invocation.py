class _Invocation(object):

   def __init__(self, client, type = None, name = None, modifications = [ ]):
      self._client = client
      self.type = type
      self.name = name
      self.modifications = [ ]
      self.modifications.extend(modifications)
      self.command = r'\new'

   ### REPR ###

   def __repr__(self):
      result = [ ]
      if self.type:
         result.append(self.type)
      if self.name:
         result.append(self.name)
      if self.modifications:
         result.append(self.modifications)
      result = [str(x) for x in result]
      if len(result) > 0:
         return '_Invocation(%s)' % ', '.join(result)
      else:
         return '_Invocation( )'

   ### FORMATTING ###

   @property
   def _opening(self):
      result = [ ]
      if self.type:
         cur = '%s %s' % (self.command, self.type)
         if self.name:
            cur += ' = %s' % self.name
         if len(self.modifications) > 0:
            cur += r' \with {'
            result.append(cur)
            result.extend(['\t' + x for x in self.modifications])
            result.append('} %s' % self._client.brackets.open)
         else:
            cur += ' %s' % self._client.brackets.open
            result.append(cur)
      else:
         result.append(self._client.brackets.open)
      return result

   @property
   def _closing(self):
      result = [ ]
      result.append(self._client.brackets.close)
      return result
