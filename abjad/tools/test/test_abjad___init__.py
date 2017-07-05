# -*- coding: utf-8 -*-
import functools
import inspect
import pytest
#import sys
from abjad.tools import abjadbooktools
from abjad.tools import datastructuretools
from abjad.tools import documentationtools
from abjad.tools import durationtools
from abjad.tools import mathtools
from abjad.tools import systemtools
#from distutils.version import StrictVersion


ignored_classes = (
    abjadbooktools.AbjadDirective,
    abjadbooktools.CodeBlock,
    abjadbooktools.CodeOutputProxy,
    abjadbooktools.AbjadDoctestDirective,
    abjadbooktools.GraphvizOutputProxy,
    abjadbooktools.ImportDirective,
    abjadbooktools.LilyPondBlock,
    abjadbooktools.LilyPondOutputProxy,
    abjadbooktools.RawLilyPondOutputProxy,
    abjadbooktools.RevealDirective,
    abjadbooktools.ShellDirective,
    abjadbooktools.ThumbnailDirective,
    datastructuretools.Enumeration,
    systemtools.StorageFormatAgent,
    systemtools.FormatSpecification,
    systemtools.TestCase,
    )

classes = documentationtools.list_all_abjad_classes(
    ignored_classes=ignored_classes,
    )


@pytest.mark.parametrize('class_', classes)
def test_abjad___init___01(class_):
    r'''All concrete classes initialize from empty input.
    '''
    if inspect.isabstract(class_):
        return
    instance = class_()
    assert instance is not None


valid_types = (
    bool,
    datastructuretools.OrdinalConstant,
    durationtools.Duration,
    float,
    int,
    mathtools.Infinity,
    mathtools.NegativeInfinity,
    str,
    tuple,
    type(None),
    )


@pytest.mark.parametrize('obj', classes)
def test_abjad___init___02(obj):
    r'''Make sure class initializer keyword argument values are immutable.
    '''
    #version = StrictVersion('.'.join(str(x) for x in sys.version_info[:3]))
    #if StrictVersion('3.5.0') <= version:
    #    return
    for attr in inspect.classify_class_attrs(obj):
        if attr.defining_class is not obj:
            continue
        elif attr.kind != 'method':
            continue
        obj = attr.object
        if isinstance(obj, functools.partial):
            obj = obj.function
        argument_specification = inspect.getargspec(obj)
        keyword_argument_names = argument_specification.args[1:]
        keyword_argument_values = argument_specification.defaults
        if keyword_argument_values is None:
            continue
        for name, value in zip(
            keyword_argument_names, keyword_argument_values):
            if value is NotImplemented:
                continue
            assert isinstance(value, valid_types), (attr.name, name, value)
            if isinstance(value, tuple):
                assert all(isinstance(x, valid_types) for x in value)


functions = documentationtools.list_all_abjad_functions()


@pytest.mark.parametrize('obj', functions)
def test_abjad___init___03(obj):
    r'''Make sure function keyword argument values are immutable.
    '''
    if isinstance(obj, functools.partial):
        obj = obj.function
    argument_specification = inspect.getargspec(obj)
    keyword_argument_names = argument_specification.args[1:]
    keyword_argument_values = argument_specification.defaults
    if keyword_argument_values is None:
        return
    for name, value in zip(
        keyword_argument_names, keyword_argument_values):
        assert isinstance(value, valid_types), (name, value)
        if isinstance(value, tuple):
            assert all(isinstance(x, valid_types) for x in value)
