from abjad.tools import *
from abjad.tools.abctools.AbjadObject import AbjadObject
from experimental.specificationtools.AttributeNameEnumeration import AttributeNameEnumeration
from experimental.specificationtools.AttributeRetrievalIndicator import AttributeRetrievalIndicator
from experimental.specificationtools.ContextDictionary import ContextDictionary
from experimental.specificationtools.SettingInventory import SettingInventory
from experimental.specificationtools.ValueRetrievalIndicator import ValueRetrievalIndicator


class Specification(AbjadObject):

    ### CLASS ATTRIBUTES ###

    attribute_names = AttributeNameEnumeration()

    ### INITIALIZER ###

    def __init__(self, score_template):
        self._score_template = score_template
        self._context_names = []
        self._resolved_settings_context_dictionary = ContextDictionary(self.score_template())
        self._initialize_context_name_abbreviations()
        self._payload_context_dictionary = ContextDictionary(self.score_template())
        self._settings = SettingInventory()

    ### PRIVATE METHODS ###

    def _initialize_context_name_abbreviations(self):
        self.context_name_abbreviations = getattr(self.score_template, 'context_name_abbreviations', {})
        for context_name_abbreviation, context_name in self.context_name_abbreviations.iteritems():
            setattr(self, context_name_abbreviation, context_name)
            self._context_names.append(context_name)
        score = self.score_template()
        self._score_name = score.name

    ### READ-ONLY PUBLIC PROPERTIES ###

    @property
    def context_names(self):
        return self._context_names

    @property
    def payload_context_dictionary(self):
        return self._payload_context_dictionary

    @property
    def resolved_settings_context_dictionary(self):
        return self._resolved_settings_context_dictionary

    @property
    def score_name(self):
        return self._score_name

    @property
    def score_template(self):
        return self._score_template

    @property
    def settings(self):
        return self._settings

    ### PUBLIC METHODS ###

    def context_token_to_context_names(self, context_token):
        if isinstance(context_token, type(self)):
            context_names = [context_token.score_name]
        elif context_token in self.context_names:
            context_names = [context_token]
        elif isinstance(context_token, (tuple, list)) and all([x in self.context_names for x in context_token]):
            context_names = context_token
        elif isinstance(context_token, contexttools.Context):
            context_names = [context_token.name]
        elif contexttools.all_are_contexts(context_token):
            context_names = [context.name for context in context_token]
        else:
            raise ValueError('invalid context token: {!r}'.format(context_token))
        return context_names

    # TODO: change name to something more explicit
    def retrieve(self, attribute_name, segment_name, context_name=None, scope=None):
        return AttributeRetrievalIndicator(attribute_name, segment_name, context_name=context_name, scope=scope)

    def retrieve_resolved_value(self, attribute_name, segment_name, context_name=None, scope=None):
        return ValueRetrievalIndicator(attribute_name, segment_name, context_name=context_name, scope=scope)
