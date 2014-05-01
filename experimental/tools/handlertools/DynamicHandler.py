# -*- encoding: utf-8 -*-
import abc
from abjad.tools import durationtools
from experimental.tools.handlertools.Handler import Handler


class DynamicHandler(Handler):

    ### CLASS VARIABLES ###

    __metaclass__ = abc.ABCMeta

    ### INITIALIZER ###

    @abc.abstractmethod
    def __init__(self, minimum_duration=None):
        self.minimum_duration = minimum_duration

    ### PUBLIC PROPERTIES ###

    @property
    def minimum_duration(self):
        return self._minimum_duration

    @minimum_duration.setter
    def minimum_duration(self, minimum_duration):
        if minimum_duration is None:
            self._minimum_duration = minimum_duration
        else:
            self._minimum_duration = durationtools.Duration(minimum_duration)
