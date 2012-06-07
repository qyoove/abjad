from abjad.tools.abctools.AbjadObject import AbjadObject
from specificationtools.Selection import Selection
from specificationtools.Setting import Setting


class Directive(AbjadObject):

    ### INITIALIZER ###

    def __init__(self, *args, **kwargs):
        mandatory_argument_values, keyword_argument_values = self._get_input_argument_values(*args, **kwargs)
        target_selection, attribute_name, source = mandatory_argument_values
        persistent, truncate = keyword_argument_values
        self.target_selection = target_selection
        self.attribute_name = attribute_name
        self.source = source
        self.persistent = persistent
        self.truncate = truncate

    ### SPECIAL METHODS ###

    def __eq__(self, expr):
        if not isinstance(expr, type(self)):
            return False
        if not self._mandatory_argument_values == expr._mandatory_argument_values:
            return False
        return self._keyword_argument_values == expr._keyword_argument_values

    ### READ-ONLY PRIVATE PROPERTIES ###

    @property
    def _keyword_argument_names(self):
        return (
            'persistent',
            'truncate',
            )

    @property
    def _mandatory_argument_values(self):
        return (
            self.target_selection,
            self.attribute_name,
            self.source,
            )

    ### PRIVATE METHODS ###

    def _get_input_argument_values(self, *args, **kwargs):
        if len(args) == 1:
            assert isinstance(args[0], type(self)), repr(args[0])
            mandatory_argument_values = args[0]._mandatory_argument_values
            keyword_argument_values = args[0]._keyword_argument_values
            if kwargs.get('persistent') is not None:
                keyword_argment_values[0] = kwargs.get('persistent')
            if kwargs.get('truncate') is not None:
                keyword_argument_values[1] = kwargs.get('truncate')
        else:
            assert len(args) == 3, repr(args)
            mandatory_argument_values = args
            keyword_argument_values = []
            keyword_argument_values.append(kwargs.get('persistent', True))
            keyword_argument_values.append(kwargs.get('truncate', False))
        return mandatory_argument_values, keyword_argument_values
    
    ### PUBLIC METHODS ###

    def make_setting_with_context_name(self, context_name):
        args = []
        args.extend([self.target_selection.segment_name, context_name, self.target_selection.scope])
        args.extend([self.attribute_name, self.source, self.persistent, self.truncate])
        return Setting(*args)

    def unpack(self):
        assert isinstance(self.target_selection.context_names, (list, type(None)))
        settings = []
        if self.target_selection.context_names in (None, []):
            settings.append(self.make_setting_with_context_name(None))
        else:
            for context_name in self.target_selection.context_names:
                settings.append(self.make_setting_with_context_name(context_name))
        return settings
